import streamlit as st
import pandas as pd
import numpy as np
import requests
import geojson
import plotly.express as px

# 1. 스트림릿 페이지 기본 설정
st.set_page_config(
    page_title="전국 시군구 고령화 지도",
    page_icon="👵",
    layout="wide"
)

st.title("👵 전국 시군구 고령화지도")
st.caption("2015~2026년 인구 데이터 중 가장 최신 연도를 기준으로 계산한 시군구별 65세 이상 인구 비율입니다.")

# 2. 데이터 불러오기 함수 (캐싱 적용으로 속도 향상)
@st.cache_data
def load_data():
    # --- A. GeoJSON 경계 데이터 불러오기 ---
    boundary_url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/boundaries/sigungu_kr.geojson"
    response = requests.get(boundary_url)
    geojson_data = geojson.loads(response.text)

    # --- B. 인구 데이터 불러오기 및 전처리 ---
    pop_url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/population_yearly.csv.gz"
    
    # '코드' 열은 문자열(str)로 읽어서 앞의 0이 떨어지지 않게 유지
    df = pd.read_csv(pop_url, compression='gzip', dtype={'코드': str})
    
    # 가장 최신 연도 데이터만 추출
    latest_year = df['연도'].max()
    df_latest = df[df['연도'] == latest_year].copy()
    
    # 행정동 코드(10자리)의 앞 5자리를 잘라 시군구 코드 생성
    df_latest['시군구코드'] = df_latest['코드'].str.slice(0, 5)
    
    # 65세 이상 인구 열 찾기 ('계_65세'부터 '계_100세 이상'까지)
    total_pop_col = '계_전체' if '계_전체' in df_latest.columns else None
    
    # '계_숫자세' 형식의 열 중 65세 이상 열 선별
    age_cols = [c for c in df_latest.columns if c.startswith('계_') and c != '계_전체']
    
    old_age_cols = []
    for col in age_cols:
        age_str = col.replace('계_', '').replace('세', '').replace(' 이상', '')
        if age_str.isdigit() and int(age_str) >= 65:
            old_age_cols.append(col)
        elif '100' in col: # '100세 이상' 처리
            old_age_cols.append(col)
            
    # 시군구별로 전체 인구 및 65세 이상 인구 합산
    # 만약 '계_전체' 열이 없다면 모든 '계_' 열의 합을 전체 인구로 사용
    if not total_pop_col:
        df_latest['전체인구_임시'] = df_latest[age_cols].sum(axis=1)
        total_pop_col = '전체인구_임시'

    df_latest['65세이상인구'] = df_latest[old_age_cols].sum(axis=1)
    
    # 시군구 코드로 그룹화하여 합계 계산 (시도, 시군구 이름도 함께 유지)
    grouped = df_latest.groupby('시군구코드').agg({
        '시도': 'first',
        '시군구': 'first',
        total_pop_col: 'sum',
        '65세이상인구': 'sum'
    }).reset_index()
    
    grouped.rename(columns={total_pop_col: '총인구수'}, inplace=True)
    
    # 고령화율(%) 계산 및 소수점 둘째 자리 반올림
    grouped['고령화율'] = (grouped['65세이상인구'] / grouped['총인구수']) * 100
    grouped['고령화율'] = grouped['고령화율'].round(2)
    
    # --- C. 요청받은 5단계 데이터 범주화 (19%, 23%, 28%, 38%) ---
    bins = [-np.inf, 19, 23, 28, 38, np.inf]
    labels = ['19% 미만', '19% 이상 ~ 23% 미만', '23% 이상 ~ 28% 미만', '28% 이상 ~ 38% 미만', '38% 이상']
    
    grouped['고령화율_구간'] = pd.cut(grouped['고령화율'], bins=bins, labels=labels, right=False)
    
    return grouped, geojson_data, latest_year

# 데이터 로딩 실행
with st.spinner("인구 데이터 및 지도 데이터를 불러오는 중입니다..."):
    df_sigungu, geojson_data, latest_year = load_data()

st.subheader(f"📅 기준 연도: {latest_year}년")

# 3. Plotly를 활용한 Choropleth(단계구분도) 지도 작성
# 지정된 5단계 구간에 맞춘 색상 매핑 (연한 색 -> 진한 색)
color_discrete_map = {
    '19% 미만': '#fef0d9',
    '19% 이상 ~ 23% 미만': '#fdcc8a',
    '23% 이상 ~ 28% 미만': '#fc8d59',
    '28% 이상 ~ 38% 미만': '#e34a33',
    '38% 이상': '#b30000'
}

fig = px.choropleth_mapbox(
    df_sigungu,
    geojson=geojson_data,
    locations='시군구코드',        # 데이터의 연결 키
    featureidkey='properties.코드', # GeoJSON의 연결 키
    color='고령화율_구간',         # 색상 기준 (범주형)
    color_discrete_map=color_discrete_map,
    category_orders={'고령화율_구간': ['19% 미만', '19% 이상 ~ 23% 미만', '23% 이상 ~ 28% 미만', '28% 이상 ~ 38% 미만', '38% 이상']},
    hover_name='시군구',
    hover_data={
        '시도': True,
        '시군구코드': False,
        '고령화율': ':.2f',
        '고령화율_구간': False
    },
    center={"lat": 35.8, "lon": 127.8}, # 대한민국 중심 위치
    zoom=6.2,
    mapbox_style="white-bg",            # 배경 지도 타일 제거
    labels={
        '고령화율_구간': '고령화율 구간',
        '고령화율': '고령화율(%)',
        '시도': '시도'
    }
)

# 지도 레이아웃 마감 및 여백 설정
fig.update_layout(
    margin={"r": 0, "t": 10, "l": 0, "b": 0},
    legend=dict(
        title=dict(text="고령화율 구간"),
        yanchor="top", y=0.98,
        xanchor="left", x=0.01,
        bgcolor="rgba(255, 255, 255, 0.8)"
    )
)

# 화면에 지도 출력
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# 4. 고령화율 상위/하위 10개 지역 표 출력
col1, col2 = st.columns(2)

# 고령화율 높음 Top 10
with col1:
    st.subheader("🔴 고령화율 가장 높은 지역 TOP 10")
    top10 = df_sigungu.sort_values(by='고령화율', ascending=False).head(10)
    top10_display = top10[['시도', '시군구', '고령화율', '총인구수']].reset_index(drop=True)
    top10_display.index += 1
    st.dataframe(
        top10_display.style.format({'고령화율': '{:.2f}%', '총인구수': '{:,}명'}),
        use_container_width=True
    )

# 고령화율 낮음 Top 10
with col2:
    st.subheader("🔵 고령화율 가장 낮은 지역 TOP 10")
    bottom10 = df_sigungu.sort_values(by='고령화율', ascending=True).head(10)
    bottom10_display = bottom10[['시도', '시군구', '고령화율', '총인구수']].reset_index(drop=True)
    bottom10_display.index += 1
    st.dataframe(
        bottom10_display.style.format({'고령화율': '{:.2f}%', '총인구수': '{:,}명'}),
        use_container_width=True
    )

import json
import numpy as np
import pandas as pd
import plotly.express as px
import requests
import streamlit as st

# 1. 스트림릿 페이지 기본 설정
st.set_page_config(
    page_title="전국 연령별 인구 지형도", page_icon="🗺️", layout="wide"
)

st.title("🗺️ 대한민국 시군구 연령별 인구 지형도")
st.caption(
    "2015~2026년 인구 데이터를 바탕으로 전국 시군구의 고령화율 및 유소년"
    " 비율 변화를 확인하세요."
)


# 2. 데이터 불러오기 및 전처리 함수
@st.cache_data
def load_base_data():
    # A. GeoJSON 경계 데이터 불러오기
    boundary_url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/boundaries/sigungu_kr.geojson"
    response = requests.get(boundary_url)
    geojson_data = json.loads(response.text)

    # B. 전체 인구 데이터 불러오기
    pop_url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/population_yearly.csv.gz"
    df = pd.read_csv(pop_url, compression="gzip", dtype={"코드": str})

    # 행정동 코드(10자리)의 앞 5자리를 잘라 시군구 코드 생성
    df["시군구코드"] = df["코드"].str.slice(0, 5)

    # 행정구역 개편 코드 보정 (42 -> 51 강원, 45 -> 52 전북, 47720 -> 27720 군위)
    df["시군구코드"] = df["시군구코드"].replace(
        {"47720": "27720"}
    )  # 군위군
    mask_42 = df["시군구코드"].str.startswith("42")
    df.loc[mask_42, "시군구코드"] = (
        "51" + df.loc[mask_42, "시군구코드"].str.slice(2)
    )

    mask_45 = df["시군구코드"].str.startswith("45")
    df.loc[mask_45, "시군구코드"] = (
        "52" + df.loc[mask_45, "시군구코드"].str.slice(2)
    )

    # 연령별 열 분리 (전체, 유소년: 0~14세, 고령: 65세 이상)
    total_pop_col = "계_전체" if "계_전체" in df.columns else None
    age_cols = [c for c in df.columns if c.startswith("계_") and c != "계_전체"]

    child_cols = []  # 0~14세
    old_cols = []  # 65세 이상

    for col in age_cols:
        age_str = (
            col.replace("계_", "").replace("세", "").replace(" 이상", "")
        )
        if age_str.isdigit():
            age_int = int(age_str)
            if age_int <= 14:
                child_cols.append(col)
            elif age_int >= 65:
                old_cols.append(col)
        elif "100" in col:
            old_cols.append(col)

    if not total_pop_col:
        df["총인구수"] = df[age_cols].sum(axis=1)
    else:
        df["총인구수"] = df[total_pop_col]

    df["유소년인구"] = df[child_cols].sum(axis=1)
    df["고령인구"] = df[old_cols].sum(axis=1)

    return df, geojson_data


# 데이터 로딩
with st.spinner("데이터를 분석하고 지도를 준비 중입니다..."):
    df_raw, geojson_data = load_base_data()

# 3. 사이드바 및 컨트롤러 설정
st.sidebar.header("⚙️ 지도 설정")

# 연도 선택 슬라이더
available_years = sorted(df_raw["연도"].unique())
min_year, max_year = min(available_years), max(available_years)
selected_year = st.sidebar.slider(
    "📅 연도 선택",
    min_value=int(min_year),
    max_value=int(max_year),
    value=int(max_year),
    step=1,
)

# 지표 선택
selected_metric = st.sidebar.radio(
    "📊 분석 지표 선택",
    options=["고령화율 (65세 이상)", "유소년 비율 (0~14세)"],
    index=0,
)

# 시도 필터
sido_list = ["전국"] + sorted(list(df_raw["시도"].dropna().unique()))
selected_sido = st.sidebar.selectbox("🗺️ 시도 선택", sido_list, index=0)

# 선택된 연도 데이터 필터링 및 집계
df_year = df_raw[df_raw["연도"] == selected_year].copy()

df_sigungu = (
    df_year.groupby("시군구코드")
    .agg(
        {
            "시도": "first",
            "시군구": "first",
            "총인구수": "sum",
            "유소년인구": "sum",
            "고령인구": "sum",
        }
    )
    .reset_index()
)

# 비율 계산 (%)
df_sigungu["고령화율"] = (
    df_sigungu["고령인구"] / df_sigungu["총인구수"] * 100
).round(2)
df_sigungu["유소년비율"] = (
    df_sigungu["유소년인구"] / df_sigungu["총인구수"] * 100
).round(2)

# 지표별 구간 및 매핑 설정
if selected_metric == "고령화율 (65세 이상)":
    target_col = "고령화율"
    bins = [-np.inf, 19, 23, 28, 38, np.inf]
    labels = [
        "19% 미만",
        "19% 이상 ~ 23% 미만",
        "23% 이상 ~ 28% 미만",
        "28% 이상 ~ 38% 미만",
        "38% 이상",
    ]
    color_map = {
        "19% 미만": "#fef0d9",
        "19% 이상 ~ 23% 미만": "#fdcc8a",
        "23% 이상 ~ 28% 미만": "#fc8d59",
        "28% 이상 ~ 38% 미만": "#e34a33",
        "38% 이상": "#b30000",
    }
else:
    target_col = "유소년비율"
    bins = [-np.inf, 8, 11, 14, 17, np.inf]
    labels = [
        "8% 미만",
        "8% 이상 ~ 11% 미만",
        "11% 이상 ~ 14% 미만",
        "14% 이상 ~ 17% 미만",
        "17% 이상",
    ]
    color_map = {
        "8% 미만": "#edf8fb",
        "8% 이상 ~ 11% 미만": "#b2e2e2",
        "11% 이상 ~ 14% 미만": "#66c2a4",
        "14% 이상 ~ 17% 미만": "#2ca25f",
        "17% 이상": "#006d2c",
    }

df_sigungu["비율_구간"] = pd.cut(
    df_sigungu[target_col], bins=bins, labels=labels, right=False
)

# 시도 필터링 적용
if selected_sido != "전국":
    df_display = df_sigungu[df_sigungu["시도"] == selected_sido].copy()
else:
    df_display = df_sigungu.copy()

# 4. 상단 지표 카드 세 장 출력
st.subheader(f"📌 {selected_year}년 {selected_sido} 핵심 지표 ({selected_metric})")

total_pop_sum = df_display["총인구수"].sum()
if selected_metric == "고령화율 (65세 이상)":
    avg_rate = (
        (df_display["고령인구"].sum() / total_pop_sum * 100)
        if total_pop_sum > 0
        else 0
    )
else:
    avg_rate = (
        (df_display["유소년인구"].sum() / total_pop_sum * 100)
        if total_pop_sum > 0
        else 0
    )

max_row = df_display.loc[df_display[target_col].idxmax()]
min_row = df_display.loc[df_display[target_col].idxmin()]

c1, c2, c3 = st.columns(3)
c1.metric(
    f"{selected_sido} 평균 {selected_metric.split()[0]}",
    f"{avg_rate:.2f}%",
)
c2.metric(
    f"가장 높은 지역",
    f"{max_row['시도']} {max_row['시군구']}",
    f"{max_row[target_col]:.2f}%",
)
c3.metric(
    f"가장 낮은 지역",
    f"{min_row['시도']} {min_row['시군구']}",
    f"{min_row[target_col]:.2f}%",
)

# 5. 지도 중심 좌표 계산 (시도 선택 시 자동 확대)
if selected_sido == "전국":
    center_lat, center_lon, zoom_level = 35.8, 127.8, 6.2
else:
    # 해당 시도의 GeoJSON 경계 좌표 추출하여 중심점 및 줌 레벨 결정
    sido_codes = df_display["시군구코드"].tolist()
    lats, lons = [], []
    for feature in geojson_data["features"]:
        if feature["properties"]["코드"] in sido_codes:
            geom = feature["geometry"]
            coords = (
                geom["coordinates"][0][0]
                if geom["type"] == "MultiPolygon"
                else geom["coordinates"][0]
            )
            for pt in coords:
                lons.append(pt[0])
                lats.append(pt[1])

    center_lat = (max(lats) + min(lats)) / 2 if lats else 35.8
    center_lon = (max(lons) + min(lons)) / 2 if lons else 127.8
    zoom_level = 8.2

# 6. Plotly 지도 출력
fig = px.choropleth_map(
    df_display,
    geojson=geojson_data,
    locations="시군구코드",
    featureidkey="properties.코드",
    color="비율_구간",
    color_discrete_map=color_map,
    category_orders={"비율_구간": labels},
    hover_name="시군구",
    hover_data={
        "시도": True,
        "시군구코드": False,
        target_col: ":.2f",
        "총인구수": ":,",
        "비율_구간": False,
    },
    center={"lat": center_lat, "lon": center_lon},
    zoom=zoom_level,
    map_style="open-street-map",
    labels={
        "비율_구간": f"{selected_metric.split()[0]} 구간",
        target_col: f"{selected_metric.split()[0]}(%)",
        "시도": "시도",
    },
)

fig.update_layout(
    margin={"r": 0, "t": 10, "l": 0, "b": 0},
    legend=dict(
        title=dict(text=f"{selected_metric.split()[0]} 구간"),
        yanchor="top",
        y=0.98,
        xanchor="left",
        x=0.01,
        bgcolor="rgba(255, 255, 255, 0.85)",
    ),
)

st.plotly_chart(fig, use_container_width=True)

# 데이터 미매칭 유의사항 안내
st.caption(
    "⚠️ 행정구역 개편 및 신설로 인해 과거 일부 연도 데이터 중 경계 지도와 일치하지"
    " 않는 지역은 회색으로 표시될 수 있습니다."
)

st.markdown("---")

# 7. 비율 상위 / 하위 10개 지역 표 출력
col1, col2 = st.columns(2)

with col1:
    st.subheader(f"🔴 {selected_metric.split()[0]} 가장 높은 지역 TOP 10")
    top10 = df_display.sort_values(by=target_col, ascending=False).head(10)
    top10_display = top10[
        ["시도", "시군구", target_col, "총인구수"]
    ].reset_index(drop=True)
    top10_display.index += 1
    st.dataframe(
        top10_display.style.format(
            {target_col: "{:.2f}%", "총인구수": "{:,}명"}
        ),
        use_container_width=True,
    )

with col2:
    st.subheader(f"🔵 {selected_metric.split()[0]} 가장 낮은 지역 TOP 10")
    bottom10 = df_display.sort_values(by=target_col, ascending=True).head(10)
    bottom10_display = bottom10[
        ["시도", "시군구", target_col, "총인구수"]
    ].reset_index(drop=True)
    bottom10_display.index += 1
    st.dataframe(
        bottom10_display.style.format(
            {target_col: "{:.2f}%", "총인구수": "{:,}명"}
        ),
        use_container_width=True,
    )

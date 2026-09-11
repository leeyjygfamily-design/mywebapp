import streamlit as st

# 페이지 기본 설정 (야구장 야간 경기 감성)
st.set_page_config(
    page_title="KBO x MBTI 운명의 구단 소환",
    page_icon="⚾",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 커스텀 CSS 디자인 (열정적인 레드/네이비 스포츠 테마 및 전광판 카드)
st.markdown("""
<style>
    /* 메인 배경 */
    .stApp {
        background-color: #0b132b;
        color: #ffffff;
    }
    /* 메인 타이틀 */
    .main-title {
        text-align: center;
        font-size: 2.6rem;
        font-weight: 900;
        color: #ff0055;
        text-shadow: 0px 0px 12px rgba(255, 0, 85, 0.6);
        margin-bottom: 5px;
    }
    .sub-title {
        text-align: center;
        font-size: 1.1rem;
        color: #4cc9f0;
        margin-bottom: 30px;
        font-weight: 600;
    }
    /* 야구 전광판 스타일 결과 카드 */
    .baseball-card {
        background: linear-gradient(135deg, #1c2541, #0b132b);
        border: 3px solid #ff0055;
        border-radius: 16px;
        padding: 25px;
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.7);
        margin-top: 20px;
        text-align: center;
    }
    .team-badge {
        font-size: 4.5rem;
        margin-bottom: 10px;
    }
    .team-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #f72585;
        margin-bottom: 8px;
    }
    .slogan-box {
        background-color: rgba(76, 201, 240, 0.15);
        border-left: 5px solid #4cc9f0;
        padding: 12px;
        margin: 18px 0;
        font-size: 1.15rem;
        color: #4cc9f0;
        font-weight: 700;
    }
    .description-text {
        font-size: 1.05rem;
        line-height: 1.7;
        color: #e0e1dd;
        text-align: justify;
    }
</style>
""", unsafe_allow_html=True)

# MBTI별 KBO 야구팀 매칭 데이터
mbti_kbo_teams = {
    "INTJ": {
        "team": "LG 트윈스",
        "badge": "⚾",
        "slogan": "“무적 LG! 치밀한 데이터와 철저한 빌드업으로 정상을 지배한다!”",
        "desc": "당신은 치밀한 승성 데이터 분석과 탄탄한 시스템을 바탕으로 경기를 지배하는 전략가입니다. 승리를 위한 완벽한 플랜 B까지 준비되어 있는 모습이 끈질기고 스마트한 LG 트윈스와 완벽하게 어우러집니다."
    },
    "INTP": {
        "team": "NC 다이노스",
        "badge": "🦖",
        "slogan": "“거침없이 가자! 데이터 야구의 최첨단에서 혁신을 집행한다!”",
        "desc": "당신은 세이버메트릭스와 창의적인 스탯 해석으로 새로운 판도를 짜는 호기심 많은 분석가입니다. 남들이 보지 못하는 선수들의 잠재력을 파헤치는 혁신적인 NC 다이노스의 DNA가 흐르고 있습니다."
    },
    "ENTJ": {
        "team": "SSG 랜더스",
        "badge": "🚀",
        "slogan": "“세상을 흔들 압도적 스케일! 우리는 승리하기 위해 투자를 아끼지 않는다!”",
        "desc": "당신은 거침없는 리더십과 과감한 스케일로 팀을 우승으로 끌어올리는 승부사입니다. 화려한 라인업과 인프라를 바탕으로 리그의 빅마켓을 주도하는 SSG 랜더스의 결단력과 꼭 닮았습니다."
    },
    "ENTP": {
        "team": "두산 베어스",
        "badge": "🐻",
        "slogan": "“Miracle Doosan! 위기일수록 더 거세게 몰아치는 예측 불가의 화력!”",
        "desc": "당신은 판이 뒤집히는 순간일수록 승부욕이 타오르는 본능적인 트릭스터입니다. 벼랑 끝에서도 상상을 초월하는 역전 드라마를 써 내려가는 '허슬두' 두산 베어스의 기적 같은 에너지와 통합니다."
    },
    "INFJ": {
        "team": "한화 이글스",
        "badge": "🦅",
        "slogan": "“최강 한화! 어떤 시련이 와도 꺾이지 않는 신념의 불꽃!”",
        "desc": "당신은 아무리 힘든 순간에도 쉽게 포기하지 않고 끝까지 믿음을 지켜내는 신념의 육성가입니다. 변함없는 열정으로 팀과 동료를 보살피며 묵묵히 낭만을 만들어가는 한화 이글스의 서사와 완벽히 겹칩니다."
    },
    "INFP": {
        "team": "키움 히어로즈",
        "badge": "🦸",
        "slogan": "“영웅은 만들어지는 것! 육성과 낭만으로 한계를 돌파한다!”",
        "desc": "당신은 가능성에 가치를 두고 원석을 보석으로 다듬어내는 이상가입니다. 거대한 자본에 굴하지 않고 오직 실력과 원석들의 성장 스토리로 영웅 신화를 써 내려가는 키움 히어로즈와 잘 어울립니다."
    },

    "ENFJ": {
        "team": "삼성 라이온즈",
        "badge": "🦁",
        "slogan": "“명가 재건! 뜨거운 뭉침과 자부심으로 푸른 피를 승리로 이끈다!”",
        "desc": "당신은 강력한 동기부여와 깊은 팀워크로 명가의 전통을 이어가는 열정적 카리스마의 소유자입니다. 선수단과 팬들을 하나로 묶어 푸른 전설을 만들어가는 삼성 라이온즈의 리더십을 갖추고 있습니다."
    },
    "ENFP": {
        "team": "롯데 자이언츠",
        "badge": "🌊",
        "slogan": "“마! 이것이 거인들의 야구다! 세상에서 가장 뜨거운 용광로 응원!”",
        "desc": "당신은 존재 자체만으로 주변의 사기를 최대로 끌어올리는 흥 부자이자 열정의 화신입니다. 구장 전체를 뜨거운 붉은 바다로 물들이며 세상에서 가장 정열적인 야구를 선보이는 롯데 자이언츠의 심장을 가졌습니다."
    },
    "ISTJ": {
        "team": "kt wiz",
        "badge": "🧙‍♂️",
        "slogan": "“마법 같은 반전은 철저한 기본기와 신뢰에서 시작된다!”",
        "desc": "당신은 흔들리지 않는 기본기와 철저한 멘탈 관리로 제 몫을 해내는 팀의 든든한 버팀목입니다. 소리 없이 강하며 단단한 마운드 운영과 꾸준함으로 포스트시즌 단골이 된 kt wiz의 내공과 닮았습니다."
    },
    "ISFJ": {
        "team": "KIA 타이거즈",
        "badge": "🐯",
        "slogan": "“검붉은 유니폼의 무게! 동료를 믿고 명가의 역사를 지켜낸다!”",
        "desc": "당신은 헌신적인 태도와 단단한 책임감으로 팀의 그늘진 곳까지 보살피는 수호자입니다. 수많은 우승 트로피 뒤에 숨은 선수들의 땀방울과 팬들을 향한 깊은 애정을 지닌 KIA 타이거즈의 품격을 가졌습니다."
    },
    "ESTJ": {
        "team": "LG 트윈스",
        "badge": "⚾",
        "slogan": "“원팀의 완성! 규율과 조직력으로 완벽한 승리를 집행한다!”",
        "desc": "당신은 명확한 시스템과 강력한 실행력으로 승리라는 목표를 달성해내는 원칙주의자입니다. 탄탄한 뎁스와 빈틈없는 조직력으로 정규시즌을 압도하는 LG 트윈스의 정석 야구와 맞닿아 있습니다."
    },
    "ESFJ": {
        "team": "KIA 타이거즈",
        "badge": "🐯",
        "slogan": "“최강 KIA! 모두가 하나 되는 열광의 홈구장을 만든다!”",
        "desc": "당신은 친화력과 협동심으로 선후배와 팬 커뮤니티를 오붓하게 연결하는 분위기 메이커입니다. 전국 어디서나 구장을 가득 메우며 패밀리십을 발휘하는 KIA 타이거즈의 매력과 부합합니다."
    },
    "ISTP": {
        "team": "NC 다이노스",
        "badge": "🦖",
        "slogan": "“냉철한 한 방! 불필요한 거품을 뺀 실전 위주의 타격전!”",
        "desc": "당신은 상황을 냉정하게 주시하다 단 한 번의 찬스에 치명적인 타점을 올려버리는 해결사입니다. 순간적인 순발력과 완벽한 메커니즘으로 상대를 기습하는 NC 다이노스의 도파민 야구와 잘 맞습니다."
    },
    "ISFP": {
        "team": "키움 히어로즈",
        "badge": "🦸",
        "slogan": "“자유로운 플레이 속에서 피어나는 개성과 예술적인 타격!”",
        "desc": "당신은 유연한 감각과 강요받지 않는 자유로움 속에서 최고 능력을 발휘하는 아티스트형 플레이어입니다. 선수 각자의 개성을 존중하며 그 안에서 스타 플레이어를 배출하는 키움 히어로즈의 기류를 공유합니다."
    },
    "ESTP": {
        "team": "두산 베어스",
        "badge": "🐻",
        "slogan": "“빠른 판단, 과감한 주루! 전장을 휘젓는 압도적 공격 태세!”",
        "desc": "당신은 리스크를 두려워하지 않고 과감하게 한 베이스를 더 파고드는 직진형 과감파입니다. 특유의 거친 공격 주루와 상대를 흔드는 파워풀한 베어스 특유의 플레이 스타일이 피 속부터 흐르고 있습니다."
    },
    "ESFP": {
        "team": "롯데 자이언츠",
        "badge": "🌊",
        "slogan": "“오늘 밤 전국의 스타는 나! 사직 노래방을 지배하는 환호성!”",
        "desc": "당신은 관중들의 환호성을 자양분 삼아 기량을 폭발시키는 타고난 엔터테이너입니다. 야구를 하나의 거대한 축제로 만들며 매 순간을 즐기는 롯데 자이언츠의 축제 무대가 당신을 부르고 있습니다."
    }
}

# 헤더 디자인
st.markdown("<div class='main-title'>⚡ KBO x MBTI ⚡</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>당신의 운명 속에 숨겨진 KBO 야구 팀을 소환하라!</div>", unsafe_allow_html=True)

# MBTI 선택 박스
mbti_list = list(mbti_kbo_teams.keys())
selected_mbti = st.selectbox("⚾ 당신의 MBTI를 선택하세요:", mbti_list, index=7)

# 실행 버튼
if st.button("🔥 내 운명의 KBO 팀 확인하기", use_container_width=True):
    result = mbti_kbo_teams[selected_mbti]
    
    # 세레머니 이펙트
    st.snow()
    
    # 카드 출력
    st.markdown(f"""
    <div class='baseball-card'>
        <div class='team-badge'>{result['badge']}</div>
        <div class='team-title'>[{selected_mbti}] {result['team']}</div>
        <div class='slogan-box'>{result['slogan']}</div>
        <div class='description-text'>{result['desc']}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><hr style='border-color: #1c2541;'><p style='text-align: center; color: #8d99ae;'>PLAY BALL! ALL IN FOR VICTORY!</p>", unsafe_allow_html=True)

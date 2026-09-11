import streamlit as st

# 페이지 기본 설정 (다크 모드 스타일 감성 및 레이아웃)
st.set_page_config(
    page_title="기사의 맹수 - MBTI 수호 동물",
    page_icon="⚔️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 커스텀 CSS 디자인 (검은색/금색 테마, 고급스럽고 강인한 기사 스타일)
st.markdown("""
<style>
    /* 메인 배경 및 기본 폰트 색상 */
    .stApp {
        background-color: #0e1117;
        color: #e0e0e0;
    }
    /* 타이틀 스타일 */
    .main-title {
        text-align: center;
        font-size: 2.8rem;
        font-weight: 800;
        color: #d4af37; /* Gold */
        text-shadow: 2px 2px 4px #000000;
        margin-bottom: 5px;
    }
    .sub-title {
        text-align: center;
        font-size: 1.1rem;
        color: #a0a0a0;
        margin-bottom: 30px;
        font-style: italic;
    }
    /* 결과 카드 스타일 */
    .knight-card {
        background: linear-gradient(145deg, #1f242d, #161920);
        border: 2px solid #d4af37;
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.6);
        margin-top: 20px;
        text-align: center;
    }
    .animal-icon {
        font-size: 5rem;
        margin-bottom: 10px;
    }
    .animal-title {
        font-size: 2rem;
        font-weight: bold;
        color: #ffffff;
        margin-bottom: 10px;
    }
    .motto-box {
        background-color: rgba(212, 175, 55, 0.1);
        border-left: 4px solid #d4af37;
        padding: 10px;
        margin: 15px 0;
        font-size: 1.1rem;
        color: #f1c40f;
        font-weight: 600;
    }
    .description-text {
        font-size: 1.05rem;
        line-height: 1.7;
        color: #cccccc;
        text-align: justify;
    }
</style>
""", unsafe_allow_html=True)

# MBTI별 강인한 기사풍 수호 동물 데이터
mbti_knights = {
    "INTJ": {
        "icon": "🦅",
        "title": "흑철의 매 (Black Iron Falcon)",
        "motto": "“높은 곳에서 전장을 내려다보며, 단 한 번의 날갯짓으로 승패를 결정짓는다.”",
        "desc": "당신은 냉철한 계산과 원거리 통찰력을 지닌 책사형 기사입니다. 혼란스러운 전장 속에서도 치밀한 전략으로 적의 허점을 파고드는 결단력을 가졌습니다."
    },
    "INTP": {
        "icon": "🦉",
        "title": "현자의 심연 부엉이 (Abyssal Owl)",
        "motto": "“어둠 속에서 진실을 탐구하고, 지혜로써 무형의 칼날을 다듬는다.”",
        "desc": "당신은 침묵 속에서 세상의 이치를 탐구하는 학자형 기사입니다. 깊은 통찰과 끝없는 지식으로 누구도 예상치 못한 정교한 해결책을 제시합니다."
    },
    "ENTJ": {
        "icon": "🦁",
        "title": "황금 갈기 사자 (Golden Mane Lion)",
        "motto": "“나를 따르라. 나의 깃발 아래 좌절이란 존재하지 않는다.”",
        "desc": "당신은 군단을 이끄는 사령관형 기사입니다. 압도적인 중압감과 강력한 리더십으로 전선의 맨 앞에서 기사단을 승리로 이끕니다."
    },
    "ENTP": {
        "icon": "🐉",
        "title": "화염의 붉은 용 (Red Flame Dragon)",
        "motto": "“고정관념을 잿더미로 만들고, 룰 자체를 재정의하리라.”",
        "desc": "당신은 판도를 뒤흔드는 변혁의 기사입니다. 번뜩이는 기지와 정체되지 않는 창의성으로 예측 불가능한 공격을 퍼부어 전장을 지배합니다."
    },

    "INFJ": {
        "icon": "🐺",
        "title": "달빛의 은늑대 (Silver Moon Wolf)",
        "motto": "“고독을 두려워하지 않으며, 신념을 위해 신묵히 길을 개척한다.”",
        "desc": "당신은 숭고한 신념을 가슴에 품은 수호 기사입니다. 강한 직관과 깊은 공감 능력으로 약자를 보호하며, 자신의 신념을 절대 굽히지 않습니다."
    },
    "INFP": {
        "icon": "🦄",
        "title": "고결한 유니콘 (Noble Unicorn)",
        "motto": "“아름다운 이상과 순수한 의지를 지키기 위해 검을 든다.”",
        "desc": "당신은 낭만과 이상을 품은 맹세의 기사입니다. 외유내강의 정석으로, 내면의 순수한 가치와 평화를 지키기 위해 목숨 바쳐 싸울 수 있는 강인함을 품고 있습니다."
    },
    "ENFJ": {
        "icon": "🦅",
        "title": "불사조 (Gilded Phoenix)",
        "motto": "“시련 속에서 더욱 뜨겁게 타올라, 모두에게 빛을 제시하리라.”",
        "desc": "당신은 동료들의 사기를 북돋우는 웅변가형 기사입니다. 헌신적인 카리스마와 타인을 살피는 포용력으로 절망에 빠진 이들에게 희망의 빛이 되어줍니다."
    },
    "ENFP": {
        "icon": "뺴", # 그리폰을 상징
        "title": "폭풍의 그리폰 (Storm Gryphon)",
        "motto": "“새로운 지평선을 향해 바람을 가르고 한계 없이 도약한다.”",
        "desc": "당신은 자유로운 영혼의 모험가 기사입니다. 뜨거운 열정과 사기 진작 능력으로 어두운 전장에 활력을 불어넣고 불가능을 가능으로 바꿉니다."
    },

    "ISTJ": {
        "icon": "🐻",
        "title": "강철 가슴 요새 곰 (Ironheart Bear)",
        "motto": "“어떠한 폭풍이 불어와도 나의 방패는 뚫리지 않는다.”",
        "desc": "당신은 절대 무너지지 않는 성벽 같은 파수꾼 기사입니다. 묵묵하고 철저하게 자신의 책무를 다하며, 흔들리지 않는 신뢰감을 바탕으로 진영을 지켜냅니다."
    },
    "ISFJ": {
        "icon": "🦌",
        "title": "성스러운 뿔 백사슴 (Holy Horn Deer)",
        "motto": "“나의 무기는 아군을 지키는 헌신이며, 나의 굳건함은 사랑에서 나온다.”",
        "desc": "당신은 묵묵히 아군을 보살피는 헌신의 기사입니다. 세심한 배려와 강인한 상냥함으로 기사단의 뒤를 든든하게 받쳐주는 성스러운 존재입니다."
    },
    "ESTJ": {
        "icon": "🐅",
        "title": "군주 호랑이 (Sovereign Tiger)",
        "motto": "“규율과 질서가 승리를 가져온다. 단 한 치의 오차도 허용치 않는다.”",
        "desc": "당신은 철저한 질서를 집행하는 원칙주의 기사입니다. 타협 없는 결단력과 강력한 통제력으로 전투의 규칙을 정립하고 조직을 확실하게 지휘합니다."
    },

    "ESFJ": {
        "icon": "🐬",
        "title": "바다의 수호 돌고래 (Ocean Guardian)",
        "motto": "“함께일 때 우리는 가장 강하다. 동료를 위해 내 모든 것을 바치리.”",
        "desc": "당신은 연대와 결속을 중시하는 결의의 기사입니다. 뛰어난 친화력과 협동심으로 개별의 기사들을 하나의 강력한 단체로 묶어내는 핵심 역할을 합니다."
    },

    "ISTP": {
        "icon": "🐆",
        "title": "그림자 표범 (Shadow Panther)",
        "motto": "“조용히 숨을 죽이고, 정적 속에서 단 한 번의 치명타를 날린다.”",
        "desc": "당신은 온갖 도구를 완벽히 다루는 냉철한 암살 기사입니다. 뛰어난 상황 판단력과 대담함으로 도사리는 위험을 냉정하게 해결해 나갑니다."
    },
    "ISFP": {
        "icon": "🦅",
        "title": "바람의 붉은 매 (Crimson Falcon)",
        "motto": "“내 눈이 향하는 곳이 곧 나의 길이요, 조용하지만 맹렬하게 비상한다.”",
        "desc": "당신은 유연하고 예술적인 감각을 지닌 맹장 기사입니다. 과묵하지만 순간의 폭발적인 집중력과 감각적인 유연함으로 상대를 제압합니다."
    },

    "ESTP": {
        "icon": "상어",
        "title": "심해의 은빛 상어 (Silver Apex Shark)",
        "motto": "“망설임은 죽음뿐. 망설이지 않고 최전선으로 돌진한다.”",
        "desc": "당신은 스릴을 즐기는 본능적인 돌격대장 기사입니다. 뛰어난 신체 감각과 순간 대처 능력으로 위험천만한 최전방을 가장 마음에 들어 하며 유유히 헤쳐 나갑니다."
    },
    "ESFP": {
        "icon": "🦚",
        "title": "화려한 태양 공작 (Solar Peacock)",
        "motto": "“전장은 나의 무대! 가장 눈부신 빛으로 모두의 시선을 사로잡으리.”",
        "desc": "당신은 분위기를 압도하는 스타 기사입니다. 타고난 스타성과 거침없는 에너지를 발산하여 싸움의 열기를 최고조로 끌어올리는 존재입니다."
    }
}

# 그리폰, 상어 이모지 보정
mbti_knights["ENFP"]["icon"] = "🦅"
mbti_knights["ESTP"]["icon"] = "🦈"

# UI 헤더
st.markdown("<div class='main-title'>⚔️ 기사의 맹수 ⚔️</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>당신의 영혼에 잠들어 있는 강인한 수호 동물을 소환하라</div>", unsafe_allow_html=True)

# MBTI 선택 드롭다운
mbti_list = list(mbti_knights.keys())
selected_mbti = st.selectbox("당신의 MBTI 성향을 선택하십시오:", mbti_list, index=2)

# 소환 버튼
if st.button("🛡️ 수호 동물 소환하기", use_container_width=True):
    knight = mbti_knights[selected_mbti]
    
    # 축하 이펙트
    st.balloons()
    
    # 결과 출력 카드
    st.markdown(f"""
    <div class='knight-card'>
        <div class='animal-icon'>{knight['icon']}</div>
        <div class='animal-title'>[{selected_mbti}] {knight['title']}</div>
        <div class='motto-box'>{knight['motto']}</div>
        <div class='description-text'>{knight['desc']}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><hr style='border-color: #333;'><p style='text-align: center; color: #666;'>May the Honor and Strength be with you.</p>", unsafe_allow_html=True)

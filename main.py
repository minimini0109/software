# app.py
import streamlit as st
from datetime import datetime
import random

st.set_page_config(page_title="어퓨 🌿", page_icon="💧", layout="wide")

# --- CSS: 예쁜 글씨체 + 색감 + 스타일링 ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;500;700&display=swap');
    .stApp {
        background-color: #f0fbff;
        font-family: 'Montserrat', sans-serif;
        color: #033f63;
    }
    .header-title {
        font-size: 64px;
        font-weight: 700;
        color: #0278ae;
        margin: 0;
    }
    .header-subtitle {
        font-size: 24px;
        color: #56cfe1;
        margin: 0;
    }
    .menu-button > button {
        background-color: #a8d8ea !important;
        color: white !important;
        font-weight: bold;
    }
    .stTextInput>div>input, .stDateInput>div>input {
        background-color: #f4fcff !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 상단 헤더 + 슬로건 + 파랑새 이모지 (캐릭터 대신) ---
st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <p class="header-title">어퓨</p>
        <p class="header-subtitle">A few, just for you 💙</p>
        <p style="font-size: 80px; margin: 10px 0;">🐦</p>
    </div>
    <hr style="border:1px solid #cceafc"/>
""", unsafe_allow_html=True)

# --- 전역: 사용자 피부 정보, 내 화장품 서랍, 제품 DB 등 ---
if 'user_skin' not in st.session_state:
    st.session_state.user_skin = {
        "피부타입": None,
        "민감도": 0,
        "트러블정도": 0,
        "피부톤": None
    }

if 'my_drawer' not in st.session_state:
    st.session_state.my_drawer = []

if 'cosmetic_db' not in st.session_state:
    # --- 100개 샘플 화장품 생성 함수 ---
    skin_types = ["건성","지성","복합성","수부지"]
    skin_tones = ["가을웜톤","봄웜톤","여름쿨톤","겨울쿨톤"]
    categories = ["토너","로션","크림","세럼","립스틱","틴트","아이브로우","아이라이너","팩","선크림"]
    base_ingredients = ["히알루론산","글리세린","세라마이드","판테놀","마데카소사이드","레티놀","비타민C","콜라겐","알로에베라","향료","에탄올","자외선차단제성분"]
    cosmetic_list = []
    for i in range(100):
        prod = {}
        prod["이름"] = f"Product_{i+1}"
        prod["종류"] = random.choice(categories)
        prod["가격"] = random.randint(8000, 50000)
        # 이 제품이 잘 맞는 피부 조건 (예: 민감도 낮거나 높거나)
        prod["추천_피부타입"] = random.choice(skin_types)
        prod["추천_피부톤"] = random.choice(skin_tones)
        prod["권장_민감도_max"] = random.randint(2, 8)  # 이 이하 민감도 사용자에 적합
        prod["권장_트러블_max"] = random.randint(2, 8)
        # 성분 무작위 3~5개 선택
        prod["성분"] = random.sample(base_ingredients, random.randint(3,5))
        cosmetic_list.append(prod)
    st.session_state.cosmetic_db = cosmetic_list

ingredient_desc = {
    "히알루론산": "강력한 보습 성분으로 수분 유지에 도움을 줍니다.",
    "글리세린": "피부에 수분을 공급하고 장벽을 보호합니다.",
    "세라마이드": "피부 장벽을 강화해주는 지질 성분입니다.",
    "판테놀": "피부 진정 + 보습을 도와줍니다.",
    "마데카소사이드": "손상된 피부 회복에 도움을 줍니다.",
    "레티놀": "피부 재생 및 노화 방지, 하지만 자극 가능성이 있습니다.",
    "비타민C": "미백 및 항산화 효과가 있으나, 민감성 피부일 땐 자극 주의.",
    "콜라겐": "탄력 개선, 보습 보조 성분.",
    "알로에베라": "진정 + 보습 효과, 민감성 피부에 무난.",
    "향료": "향을 위한 성분 — 민감/트러블 피부에는 자극이 될 수 있어요.",
    "에탄올": "보존 · 흡수 속도 향상 — 자극 가능성 있음.",
    "자외선차단제성분": "SPF/UVB 차단 성분 — 외출용화장품 필수."
}

# --- 메뉴: 서랍 스타일로 ---
menu = ["🗄️ 서랍", "📷 제품 촬영", "🔎 검색", "💧 내 정보"]
choice = st.selectbox("🔹 메뉴 선택", menu, index=0)

# --- 각 기능 구현 ---
if choice == "💧 내 정보":
    st.header("🧬 내 피부 정보 입력")
    st.session_state.user_skin["피부타입"] = st.selectbox("피부 타입", ["건성","지성","복합성","수부지"])
    st.session_state.user_skin["민감도"] = st.slider("피부 민감도 (0 = 낮음, 10 = 높음)", 0, 10, 5)
    st.session_state.user_skin["트러블정도"] = st.slider("피부 트러블 정도 (0 = 낮음, 10 = 높음)", 0, 10, 5)
    st.session_state.user_skin["피부톤"] = st.selectbox("피부 톤", ["가을웜톤","봄웜톤","여름쿨톤","겨울쿨톤"])
    st.success("✅ 정보 저장 완료!")

elif choice == "🗄️ 서랍":
    st.header("💄 나의 화장품 서랍")
    with st.expander("➕ 새 화장품 추가"):
        name = st.text_input("제품 이름")
        exp_date = st.date_input("유통기한")
        if st.button("추가하기"):
            if name:
                st.session_state.my_drawer.append({
                    "이름": name,
                    "유통기한": exp_date,
                    "성분": []
                })
                st.success(f"✅ '{name}' 추가됨")

    if st.session_state.my_drawer:
        for idx, item in enumerate(st.session_state.my_drawer):
            st.subheader(f"{item['이름']} 🧴")
            days_left = (item['유통기한'] - datetime.today().date()).days
            st.write(f"남은 사용 가능 기간: {days_left}일")
            if st.button(f"성분 보기 / 수정", key=f"drawer_{idx}"):
                st.write("성분:", item["성분"])

elif choice == "📷 제품 촬영":
    st.header("📷 제품 촬영 / 스캔")
    st.write("📸 제품 사진을 업로드하면, 어퓨가 분석해줘요.")
    uploaded_file = st.file_uploader("제품 이미지 업로드", type=["jpg","jpeg","png"])
    if uploaded_file:
        st.image(uploaded_file, caption="📦 업로드된 제품 이미지", use_column_width=True)
        st.write("🔎 (예시) 이미지 인식 + 제품 매칭 중… — 현재는 무작위 제품 사용")
        # 예시: DB에서 랜덤 제품 선택
        cosmetic = random.choice(st.session_state.cosmetic_db)
        st.subheader(f"제품 이름: {cosmetic['이름']}")
        st.write("종류:", cosmetic["종류"])
        st.write("성분:", cosmetic["성분"])

        # 적합도 점수 계산 (예시 로직)
        user = st.session_state.user_skin
        score = 100
        # 피부 타입 미스매치 penalize
        if user["피부타입"] != cosmetic["추천_피부타입"]:
            score -= 20
        # 피부톤 미스매치 penalize
        if user["피부톤"] != cosmetic["추천_피부톤"]:
            score -= 10
        # 민감도/트러블 정도가 높으면 자극 성분 있는 제품 penalize
        if user["민감도"] >= 7 or user["트러블정도"] >= 7:
            if any(ing in ["향료","에탄올","레티놀"] for ing in cosmetic["성분"]):
                score -= 30

        score = max(score, 0)
        st.metric("✨ 적합도 점수", f"{score}/100")

        ing_choice = st.selectbox("성분 상세 보기 🔍", cosmetic["성분"])
        if ing_choice:
            st.info(ingredient_desc.get(ing_choice, "설명 없음"))

        st.write("⚠ 실제 이미지 인식 + 제품 데이터베이스 연동은 추후 구현 필요합니다.")

elif choice == "🔎 검색":
    st.header("🔍 제품 검색 & 추천")
    query = st.text_input("예: '민감성 피부용 토너', '수분 크림', '틴트' 등")
    if st.button("검색 / 추천"):
        results = []
        q = query.lower()
        for prod in st.session_state.cosmetic_db:
            # 키워드 + 사용자 피부 조건 기반 추천
            match = False
            # 제품 종류 필터
            if any(cat in q for cat in [prod["종류"]]):
                match = True
            # 민감성/보습/트러블 완화 등 단어 필터 예시
            if "민감" in q or "진정" in q or "보습" in q:
                if any(ing in ["세라마이드","판테놀","마데카소사이드","알로에베라"] for ing in prod["성분"]):
                    match = True
            if "톤" in q or "톤업" in q or "미백" in q:
                if "비타민C" in prod["성분"]:
                    match = True
            if match:
                # 피부 조건과의 적합성 체크
                user = st.session_state.user_skin
                if user["피부타입"] == prod["추천_피부타입"] and \
                   user["피부톤"] == prod["추천_피부톤"] and \
                   user["민감도"] <= prod["권장_민감도_max"] and \
                   user["트러블정도"] <= prod["권장_트러블_max"]:
                    results.append((prod, "🟢 조건에 잘 맞는 제품"))
                else:
                    results.append((prod, "⚪ 조건에 대체로 맞는 제품"))

        if not results:
            st.write("❌ 조건에 맞는 제품을 찾지 못했어요.")
        else:
            st.write(f"✅ {len(results)}개 제품을 추천합니다:")
            for prod, reason in results:
                with st.container():
                    st.subheader(f"{prod['이름']}  —  {prod['종류']} {reason}")
                    st.write(f"💵 가격: {prod['가격']}원")
                    st.write("🧴 성분:", prod["성분"])
                    st.write(f"추천된 이유: {reason}")
                    ing_choice = st.selectbox("성분 상세 보기 🔍", prod["성분"], key=f"search_{prod['이름']}")
                    if ing_choice:
                        st.info(ingredient_desc.get(ing_choice, "설명 없음"))

# --- 하단 슬로건 ---
st.markdown("""
    <div style="text-align: center; margin-top: 40px; color: #56cfe1;">
        <p>“A few, just for you” — 당신만을 위한 어퓨 💙</p>
    </div>
""", unsafe_allow_html=True)

# app.py
import streamlit as st
from datetime import datetime
import random

st.set_page_config(page_title="어퓨 🌿", page_icon="💧", layout="wide")

# --- CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;500;700&display=swap');
    .stApp {
        background-color: #f0fbff;
        font-family: 'Montserrat', sans-serif;
        color: #033f63;
    }
    .header-title { font-size: 64px; font-weight: 700; color: #0278ae; margin: 0; }
    .header-subtitle { font-size: 24px; color: #56cfe1; margin: 0; }
    </style>
""", unsafe_allow_html=True)

# --- 상단 헤더 + 슬로건 + 파랑새 캐릭터 ---
st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <p class="header-title">어퓨</p>
        <p class="header-subtitle">A few, just for you 💙</p>
        <p style="font-size: 80px; margin: 10px 0;">🐦</p>
    </div>
    <hr style="border:1px solid #cceafc"/>
""", unsafe_allow_html=True)

# --- 초기 세션 상태 ---
if 'user_skin' not in st.session_state:
    st.session_state.user_skin = {
        "피부타입": None,
        "민감도": 0,
        "트러블정도": 0,
        "피부톤": None
    }

if 'my_drawer' not in st.session_state:
    st.session_state.my_drawer = []

ingredient_desc = {
    "히알루론산": "강력한 보습 성분으로 수분 유지에 도움을 줍니다.",
    "글리세린": "피부에 수분을 공급하고 장벽을 보호합니다.",
    "세라마이드": "피부 장벽을 강화해주는 지질 성분입니다.",
    "판테놀": "피부 진정 + 보습을 도와줍니다.",
    "마데카소사이드": "손상된 피부 회복에 도움을 줍니다.",
    "레티놀": "피부 재생 및 노화 방지, 하지만 자극 가능성이 있습니다.",
    "비타민C": "미백 및 항산화 효과, 민감성 피부일 땐 자극 주의.",
    "알로에베라": "진정 + 보습 효과, 민감성 피부에 무난.",
    "향료": "향을 위한 성분 — 민감/트러블 피부에는 자극이 될 수 있어요."
}

# --- 100개 가상 화장품 데이터 생성 ---
types = ["립스틱","틴트","토너","로션","크림","세럼","아이브로우","아이라이너","팩","선크림"]
tones = ["봄웜톤","가을웜톤","여름쿨톤","겨울쿨톤"]
skin_types = ["건성","지성","복합성","수부지"]

cosmetic_db = []
for i in range(1, 101):
    cosmetic_db.append({
        "이름": f"제품{i}",
        "종류": random.choice(types),
        "가격": random.randint(8000, 50000),
        "성분": random.sample(list(ingredient_desc.keys()), k=3),
        "추천_피부타입": random.choice(skin_types),
        "추천_피부톤": random.choice(tones),
        "권장_민감도_max": random.randint(3, 10),
        "권장_트러블_max": random.randint(3, 10)
    })

# --- 메뉴 ---
menu = ["🗄️ 서랍", "📷 제품 촬영", "🔎 검색", "💧 내 정보"]
choice = st.selectbox("🔹 메뉴 선택", menu, index=0)

# --- 추천 함수 ---
def recommend_products_for_user(query=None, category=None):
    user = st.session_state.user_skin
    results = []
    q = query.lower() if query else ""
    for prod in cosmetic_db:
        # 필터: 피부톤/타입/민감도/트러블
        if user["피부톤"] and prod["추천_피부톤"] != user["피부톤"]:
            continue
        if user["피부타입"] and prod["추천_피부타입"] != user["피부타입"]:
            continue
        if user["민감도"] >= prod.get("권장_민감도_max", 10):
            continue
        if user["트러블정도"] >= prod.get("권장_트러블_max", 10):
            continue
        match = False
        if category and prod["종류"] == category:
            match = True
        if query and any(k in q for k in [prod["종류"].lower(), prod["이름"].lower()]):
            match = True
        if match:
            results.append(prod)
    return results

# --- 렌즈 이미지 인식 플레이스홀더 ---
def recognize_product_from_image(image):
    # 랜덤 제품 선택
    prod = random.choice(cosmetic_db)
    reasons = []
    user = st.session_state.user_skin
    score = 100
    # 점수 감점 이유 기록
    if user["피부톤"] != prod["추천_피부톤"]:
        score -= 20
        reasons.append(f"사용자 피부톤({user['피부톤']})과 맞지 않음")
    if user["피부타입"] != prod["추천_피부타입"]:
        score -= 20
        reasons.append(f"사용자 피부타입({user['피부타입']})과 맞지 않음")
    if user["민감도"] >= prod["권장_민감도_max"]:
        score -= 20
        reasons.append(f"민감도가 높아 성분 일부가 자극 가능")
    if user["트러블정도"] >= prod["권장_트러블_max"]:
        score -= 20
        reasons.append(f"트러블 정도가 높아 일부 성분 자극 가능")
    score = max(score, 0)
    return prod, score, reasons

# --- 기능별 UI ---
if choice == "💧 내 정보":
    st.header("🧬 내 피부 정보 입력")
    st.session_state.user_skin["피부타입"] = st.selectbox("피부 타입", skin_types)
    st.session_state.user_skin["민감도"] = st.slider("피부 민감도 (0~10)", 0, 10, 5)
    st.session_state.user_skin["트러블정도"] = st.slider("피부 트러블 정도 (0~10)", 0, 10, 5)
    st.session_state.user_skin["피부톤"] = st.selectbox("피부 톤", tones)
    st.success("✅ 정보 저장 완료!")

elif choice == "🗄️ 서랍":
    st.header("💄 나의 화장품 서랍")
    with st.expander("➕ 새 화장품 추가"):
        name = st.text_input("제품 이름")
        exp_date = st.date_input("유통기한")
        if st.button("추가하기"):
            if name:
                st.session_state.my_drawer.append({"이름": name, "유통기한": exp_date, "성분":[]})
                st.success(f"'{name}' 추가됨")
    for idx, item in enumerate(st.session_state.my_drawer):
        st.subheader(f"{item['이름']} 🧴")
        days_left = (item['유통기한'] - datetime.today().date()).days
        st.write(f"남은 사용 가능 기간: {days_left}일")
        if st.button(f"성분 보기 / 수정", key=f"drawer_{idx}"):
            st.write("성분:", item["성분"])

elif choice == "📷 제품 촬영":
    st.header("📷 제품 촬영 / 스캔")
    uploaded_file = st.file_uploader("제품 이미지 업로드", type=["jpg","jpeg","png"])
    if uploaded_file:
        st.image(uploaded_file, caption="📦 업로드된 제품 이미지", use_column_width=True)
        prod, score, reasons = recognize_product_from_image(uploaded_file)
        st.subheader(f"제품 이름: {prod['이름']}")
        st.write("종류:", prod["종류"])
        st.write("성분:", prod["성분"])
        st.metric("✨ 적합도 점수", f"{score}/100")
        st.write("점수 이유:")
        for r in reasons:
            st.write(f"- {r}")
        ing_choice = st.selectbox("성분 자세히 보기 🔍", prod["성분"])
        if ing_choice:
            st.info(ingredient_desc.get(ing_choice, "설명 없음"))

elif choice == "🔎 검색":
    st.header("🔍 제품 검색 & 추천")
    query = st.text_input("예: '틴트', '립스틱', '민감성 피부용 토너'")
    if st.button("검색 / 추천"):
        category = None
        for cat in types:
            if cat in query:
                category = cat
                break
        results = recommend_products_for_user(query=query, category=category)
        if not results:
            st.write("❌ 조건에 맞는 제품을 찾지 못했어요.")
        else:
            st.write(f"✅ {len(results)}개 제품을 추천해요:")
            for prod in results[:10]:  # 상위 10개만 표시
                st.subheader(f"{prod['이름']}  —  {prod['종류']}")
                st.write(f"💵 가격: {prod['가격']}원")
                st.write("🧴 성분:", prod["성분"])
                st.write(f"추천 이유: 피부톤={prod['추천_피부톤']}, 피부타입={prod['추천_피부타입']}")
                ing_choice = st.selectbox("성분 상세 보기 🔍", prod["성분"], key=f"search_{prod['이름']}")
                if ing_choice:
                    st.info(ingredient_desc.get(ing_choice, "설명 없음"))

# --- 하단 슬로건 ---
st.markdown("""
    <div style="text-align: center; margin-top: 40px; color: #56cfe1;">
        <p>“A few, just for you” — 당신만을 위한 어퓨 💙</p>
    </div>
""", unsafe_allow_html=True)

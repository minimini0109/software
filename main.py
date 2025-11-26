import streamlit as st
from datetime import datetime
import random

st.set_page_config(page_title="어퓨 🌿", page_icon="💧", layout="wide")

# --- CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;500;700&display=swap');
    .stApp { background-color: #f0fbff; font-family: 'Montserrat', sans-serif; color: #033f63; }
    .header-title { font-size: 64px; font-weight: 700; color: #0278ae; margin: 0; }
    .header-subtitle { font-size: 24px; color: #56cfe1; margin: 0; }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
<div style="text-align: center; padding: 20px;">
    <p class="header-title">어퓨</p>
    <p class="header-subtitle">A few, just for you 💙</p>
    <p style="font-size: 80px; color:#1E90FF; margin: 10px 0;">🐦</p>
</div>
<hr style="border:1px solid #cceafc"/>
""", unsafe_allow_html=True)

# --- Session 초기화 ---
if 'user_skin' not in st.session_state:
    st.session_state.user_skin = {
        "피부타입": "건성",
        "민감도": 0,
        "트러블정도": 0,
        "피부톤": "봄웜톤"
    }

if 'my_drawer' not in st.session_state:
    st.session_state.my_drawer = []

# --- 제품 종류/성분 ---
types = ["립스틱","틴트","토너","로션","크림","세럼","아이브로우","아이라이너","팩","선크림"]
tones = ["봄웜톤","가을웜톤","여름쿨톤","겨울쿨톤"]
skin_types = ["건성","지성","복합성","수부지"]
ingredient_desc = {
    "립스틱": ["비타민E","코코아버터","시어버터"],
    "틴트": ["비타민E","알로에베라","호호바오일"],
    "토너": ["히알루론산","글리세린","판테놀"],
    "로션": ["세라마이드","판테놀","알로에베라"],
    "크림": ["세라마이드","마데카소사이드","판테놀"],
    "세럼": ["비타민C","레티놀","히알루론산"],
    "아이브로우": ["카카오씨드오일","쉐어버터","비타민E"],
    "아이라이너": ["호호바오일","비타민E","판테놀"],
    "팩": ["히알루론산","알로에베라","세라마이드"],
    "선크림": ["세라마이드","비타민E","판테놀"]
}

price_range = {
    "립스틱": (12000, 25000),
    "틴트": (10000, 22000),
    "토너": (12000, 30000),
    "로션": (15000, 28000),
    "크림": (20000, 35000),
    "세럼": (25000, 45000),
    "아이브로우": (12000, 20000),
    "아이라이너": (10000, 22000),
    "팩": (15000, 30000),
    "선크림": (18000, 35000)
}

# --- 가상의 제품 100개 생성 ---
cosmetic_db = []
user = st.session_state.user_skin
for i in range(1, 101):
    typ = random.choice(types)
    # 색조: 톤만 고려, 피부화장품: 피부타입, 민감도, 트러블까지 고려
    if typ in ["립스틱","틴트","아이브로우","아이라이너"]:
        cosmetic_db.append({
            "이름": f"{typ} 제품{i}",
            "종류": typ,
            "가격": random.randint(price_range[typ][0], price_range[typ][1]),
            "성분": random.sample(ingredient_desc[typ], k=2),
            "추천_피부톤": user["피부톤"],
            "추천_피부타입": None,
            "권장_민감도_max": 10,
            "권장_트러블_max": 10
        })
    else:
        cosmetic_db.append({
            "이름": f"{typ} 제품{i}",
            "종류": typ,
            "가격": random.randint(price_range[typ][0], price_range[typ][1]),
            "성분": random.sample(ingredient_desc[typ], k=2),
            "추천_피부톤": user["피부톤"],
            "추천_피부타입": user["피부타입"],
            "권장_민감도_max": max(user["민감도"],3),
            "권장_트러블_max": max(user["트러블정도"],3)
        })

# --- 메뉴 ---
menu = ["🗄️ 서랍", "📷 제품 촬영", "🔎 검색", "💧 내 정보"]
choice = st.selectbox("🔹 메뉴 선택", menu, index=0)

# --- 추천 함수 ---
def recommend_products_for_user(query=None, category=None):
    results = []
    q = query.lower() if query else ""
    for prod in cosmetic_db:
        # 피부톤/타입 필터
        if prod["추천_피부톤"] and prod["추천_피부톤"] != user["피부톤"]:
            continue
        if prod["추천_피부타입"] and prod["추천_피부타입"] != user["피부타입"]:
            continue
        if user["민감도"] > prod["권장_민감도_max"]:
            continue
        if user["트러블정도"] > prod["권장_트러블_max"]:
            continue
        # 검색어/카테고리 필터
        match = False
        if category and prod["종류"] == category:
            match = True
        if query and any(k in q for k in [prod["종류"].lower(), prod["이름"].lower()]):
            match = True
        if match:
            results.append(prod)
    return results

# --- UI ---
if choice == "💧 내 정보":
    st.header("💙 내 피부 정보 입력")
    st.session_state.user_skin["피부타입"] = st.selectbox("피부 타입", skin_types, index=skin_types.index(user["피부타입"]))
    st.session_state.user_skin["민감도"] = st.slider("피부 민감도 (0~10)", 0, 10, user["민감도"])
    st.session_state.user_skin["트러블정도"] = st.slider("피부 트러블 정도 (0~10)", 0, 10, user["트러블정도"])
    st.session_state.user_skin["피부톤"] = st.selectbox("피부 톤", tones, index=tones.index(user["피부톤"]))
    st.success("✅ 정보 저장 완료!")

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
            st.warning("❌ 현재 조건에 맞는 제품이 없습니다.")
        else:
            st.success(f"✅ {len(results)}개 제품을 추천해요:")
            for prod in results[:10]:
                st.subheader(f"{prod['이름']} — {prod['종류']}")
                st.write(f"💵 가격: {prod['가격']}원")
                st.write("🧴 성분:", prod["성분"])
                st.write(f"추천 이유: 피부톤={prod['추천_피부톤']}, 피부타입={prod['추천_피부타입']}")

# --- 하단 슬로건 ---
st.markdown("""
<div style="text-align: center; margin-top: 40px; color: #56cfe1;">
<p>“A few, just for you” — 당신만을 위한 어퓨 💙</p>
</div>
""", unsafe_allow_html=True)

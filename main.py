# app.py
import streamlit as st
from datetime import datetime
from PIL import Image
import json

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

# --- 상단 헤더 + 슬로건 + 파랑새 이모지 캐릭터 ---
st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <p class="header-title">어퓨</p>
        <p class="header-subtitle">A few, just for you 💙</p>
        <p style="font-size: 80px; margin: 10px 0;">🐦</p>
    </div>
    <hr style="border:1px solid #cceafc"/>
""", unsafe_allow_html=True)


# --- Load or init data in session state ---
if 'user_skin' not in st.session_state:
    st.session_state.user_skin = {
        "피부타입": None,
        "민감도": 0,
        "트러블정도": 0,
        "피부톤": None
    }

if 'my_drawer' not in st.session_state:
    st.session_state.my_drawer = []

def load_cosmetic_db():
    """
    실제 화장품 데이터베이스 로드용 함수.
    cosmetics.json 파일에는 다음과 같은 형태의 리스트가 있어야 함:
    [
      {
        "이름": "...",
        "종류": "...",
        "가격": 12000,
        "성분": ["히알루론산", "세라마이드", ...],
        "추천_피부타입": "건성" / "지성" / ...,
        "추천_피부톤": "봄웜톤" / "여름쿨톤" / ...,
        "권장_민감도_max": 5,
        "권장_트러블_max": 5
      },
      ...
    ]
    """
    try:
        with open("cosmetics.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

if 'cosmetic_db' not in st.session_state:
    st.session_state.cosmetic_db = load_cosmetic_db()


ingredient_desc = {
    # 실제로는 더 많은 성분+설명 필요
    "히알루론산": "강력한 보습 성분으로 수분 유지에 도움을 줍니다.",
    "글리세린": "피부에 수분을 공급하고 장벽을 보호합니다.",
    "세라마이드": "피부 장벽을 강화해주는 지질 성분입니다.",
    "판테놀": "피부 진정 + 보습을 도와줍니다.",
    "마데카소사이드": "손상된 피부 회복에 도움을 줍니다.",
    "레티놀": "피부 재생 및 노화 방지, 하지만 자극 가능성이 있습니다.",
    "비타민C": "미백 및 항산화 효과가 있으나, 민감성 피부일 땐 자극 주의.",
    "알로에베라": "진정 + 보습 효과, 민감성 피부에 무난.",
    "향료": "향을 위한 성분 — 민감/트러블 피부에는 자극이 될 수 있어요.",
    # ...
}


# --- 메뉴: 서랍 스타일로 ---
menu = ["🗄️ 서랍", "📷 제품 촬영", "🔎 검색", "💧 내 정보"]
choice = st.selectbox("🔹 메뉴 선택", menu, index=0)


def recommend_products_for_user(query=None, category=None):
    """
    사용자 피부 정보 + 검색 조건(query 또는 category) 바탕으로
    추천 제품 리스트 반환
    """
    user = st.session_state.user_skin
    db = st.session_state.cosmetic_db
    results = []
    q = query.lower() if query else ""
    for prod in db:
        # 1) 조건 맞는지 필터: 피부톤 / 타입 / 민감도 / 트러블
        if user["피부톤"] and prod.get("추천_피부톤") and user["피부톤"] != prod["추천_피부톤"]:
            continue
        if user["피부타입"] and prod.get("추천_피부타입") and user["피부타입"] != prod["추천_피부타입"]:
            continue
        if user["민감도"] >= prod.get("권장_민감도_max", 10):
            continue
        if user["트러블정도"] >= prod.get("권장_트러블_max", 10):
            continue

        # 2) 검색어 / 카테고리 필터
        match = False
        if category and prod["종류"] == category:
            match = True
        if query:
            # 예: 립스틱, 토너, 보습, 민감성, etc.
            if any(keyword in q for keyword in [prod["종류"].lower(), prod["이름"].lower()]):
                match = True
            if "민감" in q or "진정" in q or "보습" in q:
                if any(ing in ["세라마이드","판테놀","마데카소사이드","알로에베라"] for ing in prod["성분"]):
                    match = True
            if "톤업" in q or "미백" in q or "쿨톤" in q or "웜톤" in q:
                if prod.get("추천_피부톤") == user.get("피부톤"):
                    match = True

        if match:
            results.append(prod)
    return results


def recognize_product_from_image(image) -> dict:
    """
    이미지 인식 + 제품 매칭 함수 (플레이스홀더).
    현실에선 이미지 분류 / OCR + 화장품 DB 검색 + 크롤링 or API 필요.
    우선은 None 반환 → 검색 실패 메시지.
    """
    # TODO: 실제 이미지 인식 + 제품명 추출 로직 구현
    return None


# --- 기능별 UI 구현 ---
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
        # 실제 인식 시도
        recognized = recognize_product_from_image(uploaded_file)
        if recognized:
            prod = recognized
            st.subheader(f"제품 이름: {prod['이름']}")
            st.write("종류:", prod["종류"])
            st.write("성분:", prod["성분"])
            # 적합도 점수 계산
            user = st.session_state.user_skin
            score = 100
            if user["피부톤"] and prod.get("추천_피부톤") and user["피肤톤"] != prod["추천_피부톤"]:
                score -= 20
            if user["피부타입"] and prod.get("추천_피부타입") and user["피부타입"] != prod["추천_피부타입"]:
                score -= 20
            if user["민감도"] >= prod.get("권장_민감도_max", 10):
                score -= 20
            if user["트러블정도"] >= prod.get("권장_트러블_max", 10):
                score -= 20
            score = max(score, 0)
            st.metric("✨ 적합도 점수", f"{score}/100")

            ing_choice = st.selectbox("성분 자세히 보기 🔍", prod["성분"])
            if ing_choice:
                st.info(ingredient_desc.get(ing_choice, "설명 없음"))
        else:
            st.warning("⚠️ 제품을 인식하지 못했어요. 다른 사진을 시도하거나 수동 검색을 이용해보세요.")

elif choice == "🔎 검색":
    st.header("🔍 제품 검색 & 추천")
    user = st.session_state.user_skin
    query = st.text_input("예: '틴트', '립스틱', '민감성 피부용 토너' 등")
    if st.button("검색 / 추천"):
        # 먼저 query 기반 추천
        # 만약 query가 '립스틱'이라면 category = '립스틱' 으로 추천
        category = None
        # 단순한 키워드 mapping (필요시 확장)
        for cat in ["립스틱","틴트","토너","로션","크림","세럼","아이브로우","아이라이너","팩","선크림"]:
            if cat in query:
                category = cat
                break

        recommendations = recommend_products_for_user(query=query, category=category)

        if not recommendations:
            st.write("❌ 조건에 맞는 제품을 찾지 못했어요.")
        else:
            st.write(f"✅ {len(recommendations)}개 제품을 추천해요:")
            for prod in recommendations:
                with st.container():
                    st.subheader(f"{prod['이름']}  —  {prod['종류']}")
                    st.write(f"💵 가격: {prod.get('가격', '정보 없음')}원")
                    st.write("🧴 성분:", prod["성분"])
                    st.write(f"추천 이유: 피부톤 = {prod.get('추천_피부톤')} / 피부타입 = {prod.get('추천_피부타입')}")
                    ing_choice = st.selectbox("성분 상세 보기 🔍", prod["성분"], key=f"search_{prod['이름']}")
                    if ing_choice:
                        st.info(ingredient_desc.get(ing_choice, "설명 없음"))

# --- 하단 슬로건 ---
st.markdown("""
    <div style="text-align: center; margin-top: 40px; color: #56cfe1;">
        <p>“A few, just for you” — 당신만을 위한 어퓨 💙</p>
    </div>
""", unsafe_allow_html=True)

# app.py
import streamlit as st
from datetime import datetime, timedelta
import requests  # 나중에 인터넷 검색/이미지 인식 API 연동 시 사용
from PIL import Image

# --- 앱 설정 ---
st.set_page_config(
    page_title="어퓨 🌿", 
    page_icon="💧", 
    layout="wide"
)

# --- CSS 스타일링 & 기본 디자인 ---
st.markdown("""
    <style>
    .stApp {
        background-color: #f0faff;
    }
    .sidebar .sidebar-content {
        background-color: #e6f0ff;
    }
    .stButton>button {
        background-color: #a8d8ea;
        color: white;
        font-weight: bold;
    }
    .stTextInput>div>input, .stDateInput>div>input {
        background-color: #f4fcff;
    }
    .block-container {
        padding-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- 상단 헤더 + 캐릭터 + 슬로건 ---
st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <h1 style="color: #2a9df4; font-size: 48px; margin-bottom: 5px;">어퓨</h1>
        <h4 style="color: #56cfe1; margin-top: 0;">A few, just for you 💙</h4>
        <!-- 캐릭터 이미지 삽입 -->
        <img src="https://i.imgur.com/your_puriri_image.png" alt="퓨리리" style="width:150px;" />
    </div>
    <hr>
""", unsafe_allow_html=True)

# --- 전역 데이터 ---
user_skin = {
    "피부타입": None,
    "민감도": 0,
    "트러블정도": 0,
    "피부톤": None
}

my_drawer = []

cosmetic_db = [
    {"이름": "수분토너", "종류": "토너", "가격": 15000, "성분": ["히알루론산", "글리세린", "향료"]},
    {"이름": "레티놀 크림", "종류": "크림", "가격": 35000, "성분": ["레티놀", "세라마이드", "향료"]},
    {"이름": "진정 세럼", "종류": "세럼", "가격": 28000, "성분": ["판테놀", "마데카소사이드", "향료"]},
    {"이름": "산뜻 토너", "종류": "토너", "가격": 18000, "성분": ["글리세린", "판테놀"]},
    {"이름": "민감성 크림", "종류": "크림", "가격": 24000, "성분": ["세라마이드", "판테놀"]},
]

ingredient_desc = {
    "히알루론산": "강력한 보습 성분으로 수분 유지에 도움을 줍니다.",
    "글리세린": "피부에 수분을 공급하고 장벽을 보호합니다.",
    "향료": "제품 향을 내는 성분으로 민감성 피부에는 자극이 될 수 있습니다.",
    "레티놀": "피부 재생과 노화 방지에 효과적이나 자극 가능성이 있습니다.",
    "세라마이드": "피부 장벽 강화 성분입니다.",
    "판테놀": "피부 진정과 보습에 도움을 줍니다.",
    "마데카소사이드": "손상된 피부 회복과 진정에 도움을 줍니다."
}

# --- 사용자 인터페이스: 서랍처럼 메뉴 보여주기 ---
menu = ["💾 서랍", "📸 제품 촬영", "🔍 검색", "🧬 내 정보"]
choice = st.selectbox("🔹 메뉴를 선택하세요", menu, index=0)

if choice == "💾 서랍":
    st.header("💾 나의 화장품 서랍")
    with st.expander("➕ 새 화장품 추가"):
        name = st.text_input("제품 이름")
        exp_date = st.date_input("유통기한")
        if st.button("서랍에 추가"):
            if name:
                # 초기 성분은 빈 리스트. 나중에 성분 수동 입력 추가 가능
                my_drawer.append({"이름": name, "유통기한": exp_date, "성분": []})
                st.success(f"✅ '{name}' 이(가) 서랍에 추가되었습니다.")

    if my_drawer:
        for idx, item in enumerate(my_drawer):
            st.subheader(f"{item['이름']} 🧴")
            days_left = (item['유통기한'] - datetime.today().date()).days
            st.write(f"유통기한까지 약 **{days_left}일** 남음")
            if st.button(f"성분 보기 / 정보 수정", key=f"drawer_{idx}"):
                st.write("성분:", item["성분"])
                # (선택) 성분을 수동으로 추가할 수 있게 할 수도 있음

elif choice == "📸 제품 촬영":
    st.header("📸 제품 촬영 / 스캔")
    st.write("📷 제품 사진을 업로드하거나 촬영하면, 당신의 피부 상태에 맞는지 평가해줘요.")
    uploaded_file = st.file_uploader("제품 사진 선택", type=["jpg","jpeg","png"])
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="촬영된 제품", use_column_width=True)
        st.write("🔎 제품을 인식 중입니다... (예시로 첫 번째 DB 제품 사용)")

        # 실제: 여기서 OCR 또는 이미지 분류 + DB 혹은 웹 검색 연동
        cosmetic = cosmetic_db[0]
        st.subheader(f"제품 이름: {cosmetic['이름']}")
        st.write("성분:", cosmetic["성분"])

        # 예시 간단 점수 로직
        base_score = 100
        penalty = user_skin["민감도"] * 4 + user_skin["트러블정도"] * 3
        score = max(base_score - penalty, 0)
        st.metric("✨ 적합도 점수", f"{score}/100")

        ing_choice = st.selectbox("성분 자세히 보기", cosmetic["성분"])
        if ing_choice:
            st.info(ingredient_desc.get(ing_choice, "설명 없음"))

        st.write("⚠️ 현재는 예시 DB만 사용 중이에요. 실제 제품 인식 + 웹 검색 연동은 추후 API 필요.")

elif choice == "🔍 검색":
    st.header("🔍 제품 검색 & 추천")
    query = st.text_input("찾고 싶은 화장품 또는 조건을 입력하세요 (예: 민감성 피부용 토너)")
    if st.button("검색 / 추천"):
        # 예시: 아주 단순한 키워드 기반 필터 + 추천 다수
        results = []
        q = query.lower()
        for prod in cosmetic_db:
            if ("토너" in q and prod["종류"] == "토너") or ("크림" in q and prod["종류"] == "크림") or ("세럼" in q and prod["종류"] == "세럼"):
                results.append(prod)
            # 민감성, 보습, 진정 등의 키워드로 필터
            if "민감" in q or "진정" in q:
                if any(ing in ["판테놀", "세라마이드", "마데카소사이드"] for ing in prod["성분"]):
                    results.append(prod)
            if "보습" in q or "수분" in q:
                if any(ing in ["히알루론산", "글리세린"] for ing in prod["성분"]):
                    results.append(prod)

        # 중복 제거
        unique = {p["이름"]: p for p in results}.values()
        if not unique:
            st.write("❌ 조건에 맞는 제품을 찾지 못했어요.")
        else:
            st.write(f"✅ {len(unique)}개 제품을 추천합니다:")
            for prod in unique:
                with st.container():
                    st.subheader(f"{prod['이름']}  —  {prod['종류']}")
                    st.write(f"💵 가격: {prod['가격']}원")
                    st.write("🧴 성분:", prod["성분"])
                    reason = []
                    # 왜 추천되었는지 간단 설명
                    if user_skin["민감도"] >= 7 or user_skin["트러블정도"] >= 7:
                        if any(ing in ["판테놀", "세라마이드", "마데카소사이드"] for ing in prod["성분"]):
                            reason.append("민감성 / 트러블 피부에 진정 + 장벽 강화 성분 포함")
                    if "토너" in query and prod["종류"] == "토너":
                        reason.append("토너 요청 조건에 부합")
                    if "보습" in query and any(ing in ["히알루론산", "글리세린"] for ing in prod["성분"]):
                        reason.append("보습 성분 포함")

                    if not reason:
                        reason.append("일반적인 추천 기준 충족")

                    st.write("✅ 추천 이유: " + "; ".join(reason))
                    ing_choice = st.selectbox("성분 상세 보기 🔍", prod["성분"], key=f"search_{prod['이름']}")
                    if ing_choice:
                        st.info(ingredient_desc.get(ing_choice, "설명 없음"))

elif choice == "🧬 내 정보":
    st.header("🧬 내 피부 정보 입력")
    st.write("💙 내 피부에 딱 맞춘 추천을 위해 정보를 입력해줘요.")
    user_skin["피부타입"] = st.selectbox("피부 타입", ["건성", "지성", "복합성", "수부지"])
    user_skin["민감도"] = st.slider("피부 민감도 (낮음 ⇢ 높음)", 0, 10, 5)
    user_skin["트러블정도"] = st.slider("피부 트러블 정도 (낮음 ⇢ 높음)", 0, 10, 5)
    user_skin["피부톤"] = st.selectbox("피부 톤", ["가을웜톤", "봄웜톤", "여름쿨톤", "겨울쿨톤"])
    st.success("✅ 내 정보가 저장되었어요!")

# --- 하단 슬로건 / 캐릭터 안내 ---
st.markdown("""
    <div style="text-align: center; margin-top: 40px; color: #56cfe1;">
        <p>“A few, just for you” — 당신만을 위한 어퓨 💙</p>
    </div>
""", unsafe_allow_html=True)

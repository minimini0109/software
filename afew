# app.py
import streamlit as st
from datetime import datetime, timedelta

# --- 앱 설정 ---
st.set_page_config(
    page_title="어퓨 🌿", 
    page_icon="💧", 
    layout="wide"
)

# --- CSS 스타일링 ---
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
    .stTextInput>div>input {
        background-color: #f4fcff;
    }
    </style>
""", unsafe_allow_html=True)

# --- 전역 데이터 ---
# 피부 정보 기본값
user_skin = {
    "피부타입": None,
    "민감도": 0,
    "트러블정도": 0,
    "피부톤": None
}

# 화장품 서랍 예시 데이터
my_drawer = []

# 화장품 DB 예시
cosmetic_db = [
    {"이름": "수분토너", "종류": "토너", "가격": 15000, "성분": ["히알루론산", "글리세린", "향료"]},
    {"이름": "레티놀 크림", "종류": "크림", "가격": 35000, "성분": ["레티놀", "세라마이드", "향료"]},
    {"이름": "진정 세럼", "종류": "세럼", "가격": 28000, "성분": ["판테놀", "마데카소사이드", "향료"]},
]

# 성분 설명 예시
ingredient_desc = {
    "히알루론산": "강력한 보습 성분으로 수분 유지에 도움을 줍니다.",
    "글리세린": "피부에 수분을 공급하고 장벽을 보호합니다.",
    "향료": "제품 향을 내는 성분으로 민감성 피부에는 자극이 될 수 있습니다.",
    "레티놀": "피부 재생과 노화 방지에 효과적이나 자극 가능성이 있습니다.",
    "세라마이드": "피부 장벽 강화 성분입니다.",
    "판테놀": "피부 진정과 보습에 도움을 줍니다.",
    "마데카소사이드": "손상된 피부 회복과 진정에 도움을 줍니다."
}

# --- 사이드바 메뉴 ---
menu = ["💄 나의 화장품 서랍", "👁️ 렌즈", "🔍 검색", "🧬 내 정보"]
choice = st.sidebar.selectbox("메뉴 선택", menu)

# --- 내 정보 ---
if choice == "🧬 내 정보":
    st.header("🧬 내 피부 정보 입력")
    st.write("우리 퓨어리리와 함께 너만을 위한 맞춤 화장품 추천 💙")
    user_skin["피부타입"] = st.selectbox("피부 타입", ["건성", "지성", "복합성", "수부지"])
    user_skin["민감도"] = st.slider("피부 민감도", 0, 10, 5)
    user_skin["트러블정도"] = st.slider("피부 트러블 정도", 0, 10, 5)
    user_skin["피부톤"] = st.selectbox("피부 톤", ["가을웜톤", "봄웜톤", "여름쿨톤", "겨울쿨톤"])
    st.success("✅ 정보 저장 완료!")

# --- 나의 화장품 서랍 ---
elif choice == "💄 나의 화장품 서랍":
    st.header("💄 나의 화장품 서랍")
    
    # 새 화장품 추가
    with st.expander("➕ 화장품 추가"):
        name = st.text_input("제품 이름")
        exp_date = st.date_input("유통기한")
        if st.button("서랍에 추가"):
            if name:
                my_drawer.append({"이름": name, "유통기한": exp_date, "성분": ["히알루론산", "글리세린"]})
                st.success(f"{name} 추가 완료!")

    # 화장품 목록
    if my_drawer:
        for idx, item in enumerate(my_drawer):
            st.subheader(f"{item['이름']} 🗃️")
            days_left = (item['유통기한'] - datetime.today().date()).days
            st.write(f"유통기한까지 {days_left}일 남음")
            if st.button(f"성분 보기 🔎", key=f"drawer_{idx}"):
                st.write(item['성분'])

# --- 렌즈 ---
elif choice == "👁️ 렌즈":
    st.header("👁️ 화장품 렌즈")
    st.write("카메라로 화장품을 찍으면 적합도 점수를 알려줘요 💙")
    
    # 파일 업로드(카메라 대신)
    uploaded_file = st.file_uploader("제품 사진 선택")
    if uploaded_file:
        # 예시: 사진에서 제품 이름 추출(간단하게 DB 첫 제품으로 대체)
        cosmetic = cosmetic_db[0]
        st.image(uploaded_file, caption="촬영된 제품", use_column_width=True)
        st.subheader(f"제품 이름: {cosmetic['이름']}")
        st.write("성분:", cosmetic["성분"])
        
        # 간단 점수 계산 예시
        score = 100 - user_skin["민감도"]*3 - user_skin["트러블정도"]*2
        score = max(min(score, 100), 0)
        st.metric("적합도 점수 💧", f"{score}/100")
        
        # 성분 클릭 설명
        ing_choice = st.selectbox("성분 상세 보기 🔍", cosmetic["성분"])
        if ing_choice:
            st.info(ingredient_desc.get(ing_choice, "설명 없음"))

# --- 검색 ---
elif choice == "🔍 검색":
    st.header("🔍 화장품 검색 & 추천")
    query = st.text_input("궁금한 제품이나 질문을 입력하세요 예) 내 피부에 맞는 토너 추천")
    if st.button("검색"):
        # 간단 추천: DB 첫 제품 반환
        recommended = cosmetic_db[0]
        st.subheader(f"추천 제품: {recommended['이름']} 💙")
        st.write(f"가격: {recommended['가격']}원")
        st.write("성분:", recommended["성분"])
        ing_choice = st.selectbox("성분 상세 보기 🔍", recommended["성분"], key="search_ing")
        if ing_choice:
            st.info(ingredient_desc.get(ing_choice, "설명 없음"))

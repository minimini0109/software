import streamlit as st
from datetime import datetime
import random
import re

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
</div>
<hr style="border:1px solid #cceafc"/>
""", unsafe_allow_html=True)

# --- Session 초기화 ---
if 'user_skin' not in st.session_state:
    st.session_state.user_skin = {
        "피부타입": None,
        "민감도": 0,
        "트러블정도": 0,
        "피부톤": None
    }

if 'my_drawer' not in st.session_state:
    st.session_state.my_drawer = []

# --- 데이터 정의 ---
types = ["립스틱","틴트","토너","로션","크림","세럼","아이브로우","아이라이너","팩","선크림"]
skin_types = ["건성","지성","복합성","수부지"]
tones = ["봄웜톤","가을웜톤","여름쿨톤","겨울쿨톤"]
cosmetic_categories = ["피부화장품", "색조화장품"]

ingredient_desc = {
    "비타민E": ["항산화, 피부보호", "고농도 사용 시 트러블 가능"],
    "코코아버터": ["보습, 피부유연화", "민감성 피부 주의"],
    "시어버터": ["보습, 진정", "지성 피부 과다 사용 주의"],
    "알로에베라": ["진정, 수분공급", "알레르기 가능성 있음"],
    "호호바오일": ["유수분 밸런스, 보습", "모든 피부 안전"],
    "히알루론산": ["보습, 탄력", "저민감성 피부 안전"],
    "글리세린": ["보습, 수분 유지", "극건성 피부 안전"],
    "판테놀": ["진정, 재생", "저자극"],
    "세라마이드": ["보습, 장벽 강화", "민감성 피부 안전"],
    "마데카소사이드": ["진정, 재생", "과다 사용 시 민감 피부 주의"],
    "비타민C": ["미백, 항산화", "자극 가능성"],
    "레티놀": ["재생, 노화방지", "민감 피부 자극 가능"],
    "카카오씨드오일": ["영양공급, 윤기", "지성 피부 주의"]
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

# --- 헬퍼: 안전한 key 생성 ---
def make_safe_key(*parts):
    joined = "_".join([str(p) for p in parts if p is not None])
    safe = re.sub(r'[^0-9a-zA-Zㄱ-힣_]', '_', joined)
    return safe[:200]

# --- 제품명 생성 ---
def generate_product_name(prod_type):
    if prod_type in ["토너","로션","크림","세럼","팩","선크림"]:
        prefix = random.choice(["피부촉촉탱","촉촉촉","수분가득","진정쫀쫀"])
    else:
        prefix = random.choice(["글로우","립밤","틴트러버","아이펀"])
    return f"{prefix} {prod_type} #{random.randint(100,999)}"

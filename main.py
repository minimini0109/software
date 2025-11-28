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
joined = "*".join([str(p) for p in parts if p is not None])
safe = re.sub(r'[^0-9a-zA-Zㄱ-힣*]', '_', joined)
return safe[:200]

# --- 제품명 생성 ---

def generate_product_name(prod_type):
if prod_type in ["토너","로션","크림","세럼","팩","선크림"]:
prefix = random.choice(["피부촉촉탱","촉촉촉","수분가득","진정쫀쫀"])
else:
prefix = random.choice(["글로우","립밤","틴트러버","아이펀"])
return f"{prefix} {prod_type} #{random.randint(100,999)}"

# --- 가상 제품 생성 ---

cosmetic_db = []
user = st.session_state.user_skin
for i in range(1, 101):
typ = random.choice(types)
name = generate_product_name(typ)
ingredients = random.sample(list(ingredient_desc.keys()), k=2)
if typ in ["립스틱","틴트","아이브로우","아이라이너"]:
cosmetic_db.append({
"이름": name,
"종류": typ,
"가격": random.randint(price_range[typ][0], price_range[typ][1]),
"성분": ingredients,
"추천_피부톤": user["피부톤"],
"추천_피부타입": None,
"권장_민감도_max": 10,
"권장_트러블_max": 10
})
else:
cosmetic_db.append({
"이름": name,
"종류": typ,
"가격": random.randint(price_range[typ][0], price_range[typ][1]),
"성분": ingredients,
"추천_피부톤": None,
"추천_피부타입": user["피부타입"],
"권장_민감도_max": max(user["민감도"],3),
"권장_트러블_max": max(user["트러블정도"],3)
})

# --- 추천 함수 ---

def recommend_products_for_user(query=None, category=None, min_rating=0):
results = []
q = query.lower() if query else ""
for prod in cosmetic_db:
# 필터: 사용자 정보 기반
if prod["추천_피부타입"] and prod["추천_피부타입"] != user["피부타입"]:
continue
if user["민감도"] > prod["권장_민감도_max"]:
continue
if user["트러블정도"] > prod["권장_트러블_max"]:
continue
# 카테고리/검색 키워드 필터
match = False
if category and prod["종류"] == category:
match = True
if query and (query.lower() in prod["종류"].lower() or query.lower() in prod["이름"].lower()):
match = True
if not query and not category:
match = True
# 서랍에서 만족도 기반 추천
if min_rating > 0:
match = match and (prod.get("rating",5) >= min_rating)
if match:
results.append(prod)
return results

# --- 제품 촬영 ---

def recognize_product_from_image(image):
prod = random.choice(cosmetic_db)
reasons = []
score = 100
if prod.get("추천_피부톤") and user.get("피부톤") and user["피부톤"] != prod["추천_피부톤"]:
score -= 20
reasons.append(f"사용자 피부톤({user['피부톤']})과 맞지 않음")
if prod.get("추천_피부타입") and user.get("피부타입") and user["피부타입"] != prod["추천_피부타입"]:
score -= 20
reasons.append(f"사용자 피부타입({user['피부타입']})과 맞지 않음")
if user["민감도"] >= prod["권장_민감도_max"]:
score -= 20
reasons.append(f"민감도가 높아 성분 일부가 자극 가능")
if user["트러블정도"] >= prod["권장_트러블_max"]:
score -= 20
reasons.append(f"트러블 정도가 높아 일부 성분 자극 가능")
score = max(score,0)
return prod, score, reasons

# --- 메뉴 ---

menu = ["🗄️ 서랍", "📷 제품 촬영", "🔎 검색", "💧 내 정보", "💡 루틴 추천"]
choice = st.selectbox("🔹 메뉴 선택", menu, index=0)

# --- UI ---

if choice == "💧 내 정보":
st.header("💙 내 피부 정보 입력")
current_type = user["피부타입"] if user["피부타입"] in skin_types else skin_types[0]
current_tone = user["피부톤"] if user["피부톤"] in tones else tones[0]
st.session_state.user_skin["피부타입"] = st.selectbox("피부 타입", skin_types, index=skin_types.index(current_type))
st.session_state.user_skin["민감도"] = st.slider("피부 민감도 (0~10)", 0, 10, user["민감도"])
st.session_state.user_skin["트러블정도"] = st.slider("피부 트러블 정도 (0~10)", 0, 10, user["트러블정도"])
st.session_state.user_skin["피부톤"] = st.selectbox("피부 톤", tones, index=tones.index(current_tone))
st.success("✅ 정보 저장 완료!")

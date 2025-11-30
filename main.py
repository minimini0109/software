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

# 검색·성분 보기 상태 저장용
if 'selected_search_product' not in st.session_state:
    st.session_state.selected_search_product = None
if 'selected_search_ingredient' not in st.session_state:
    st.session_state.selected_search_ingredient = None

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

user = st.session_state.user_skin

# --- 가상 제품 생성 ---
cosmetic_db = []
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

# --- 추천 이유 생성 ---
def explain_recommendation(prod, user_skin):
    reasons = []
    if prod["종류"] in ["토너","로션","크림","세럼","팩","선크림"]:
        if prod.get("추천_피부타입") and user_skin.get("피부타입"):
            if prod["추천_피부타입"] == user_skin["피부타입"]:
                reasons.append(f"사용자 피부타입({user_skin['피부타입']})에 맞게 설계된 제품이에요.")
            else:
                reasons.append(f"사용자 피부타입({user_skin['피부타입']})와는 조금 다르지만, 전반적으로 사용할 수 있는 제품이에요.")
        if user_skin["민감도"] <= prod["권장_민감도_max"]:
            reasons.append(f"사용자 민감도({user_skin['민감도']})가 이 제품 권장 민감도 범위 이내라 자극 가능성이 비교적 낮아요.")
        if user_skin["트러블정도"] <= prod["권장_트러블_max"]:
            reasons.append(f"트러블 정도({user_skin['트러블정도']})를 고려했을 때 과도한 자극 없이 사용할 수 있는 제품이에요.")
    else:
        if prod.get("추천_피부톤") and user_skin.get("피부톤"):
            if prod["추천_피부톤"] == user_skin["피부톤"]:
                reasons.append(f"사용자 피부톤({user_skin['피부톤']})에 잘 어울리도록 추천된 색조 제품이에요.")
            else:
                reasons.append(f"현재 피부톤({user_skin['피부톤']})과는 살짝 다를 수 있지만, 다양한 연출에 활용 가능한 색조 제품이에요.")
        else:
            reasons.append("피부톤 정보가 부족하지만, 전반적으로 다양한 톤에 무난하게 사용할 수 있는 색조 제품이에요.")
    return reasons

# --- 추천 함수 ---
def recommend_products_for_user(query=None, category=None):
    results = []
    q = query.lower() if query else ""
    for prod in cosmetic_db:
        if prod["추천_피부타입"] and prod["추천_피부타입"] != user["피부타입"]:
            continue
        if user["민감도"] > prod["권장_민감도_max"]:
            continue
        if user["트러블정도"] > prod["권장_트러블_max"]:
            continue
        match = False
        if category and prod["종류"] == category:
            match = True
        if query and (q in prod["종류"].lower() or q in prod["이름"].lower()):
            match = True
        if not query and not category:
            match = True
        if match:
            results.append(prod)
    return results

# --- 제품 촬영: 에뛰드 글로우 픽싱 틴트 모브먼트 + 톤별 점수 ---
def recognize_product_from_image(image):
    prod = {
        "이름": "에뛰드 글로우 픽싱 틴트 모브먼트",
        "종류": "틴트",
        "성분": ["비타민E", "글리세린"],
    }

    tone = user.get("피부톤")
    if tone == "봄웜톤":
        score = 90
        reasons = ["봄웜톤에 잘 어울리는 차분한 모브 계열 컬러예요."]
    elif tone == "가을웜톤":
        score = 90
        reasons = ["가을웜톤에도 어울리는 웜 기가 섞인 로즈-모브 컬러예요."]
    elif tone == "겨울쿨톤":
        score = 50
        reasons = ["채도와 명도가 살짝 안 맞을 수 있어, 겨울쿨톤에선 호불호가 갈릴 수 있어요."]
    elif tone == "여름쿨톤":
        score = 75
        reasons = ["여름쿨톤에게는 무난하게 어울리지만, 완전 찰떡 컬러는 아닐 수 있어요."]
    else:
        score = 70
        reasons = ["피부톤 정보가 없어 중간 점수로 추천해요. 실사용 시 발색 테스트를 권장해요."]

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

elif choice == "🗄️ 서랍":
    st.header("💄 나의 화장품 서랍")
    with st.expander("➕ 새 화장품 추가"):
        name = st.text_input("제품 이름")
        exp_date = st.date_input("유통기한")
        cat = st.selectbox("화장품 종류", cosmetic_categories)
        rating = st.slider("만족도 (1~5)", 1, 5, 3)
        if st.button("추가하기", key=make_safe_key("add_drawer", name)):
            if name:
                st.session_state.my_drawer.append({"이름": name, "유통기한": exp_date, "별점": rating, "카테고리": cat})
                st.success(f"'{name}' 추가됨")
                st.rerun()

    for idx, item in enumerate(list(st.session_state.my_drawer)):
        st.subheader(f"{item['이름']} 🧴")
        days_left = (item['유통기한'] - datetime.today().date()).days
        if days_left < 0:
            st.warning("⚠️ 유통기한이 지났습니다!")
        else:
            st.write(f"남은 사용 가능 기간: {days_left}일")
        st.write(f"⭐ 만족도: {item['별점']}")
        del_key = make_safe_key("del", idx, item['이름'])
        if st.button("삭제", key=del_key):
            st.session_state.my_drawer.pop(idx)
            st.rerun()

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
        if reasons:
            st.write("점수 이유:")
            for r in reasons:
                st.write(f"- {r}")
        ing_choice = st.selectbox("성분 자세히 보기 🔍", prod["성분"], key=make_safe_key("scan_ing_select", prod["이름"]))
        if ing_choice:
            info = ingredient_desc.get(ing_choice, ["정보 없음",""])
            st.info(f"{ing_choice} → 장점: {info[0]}, 주의: {info[1]}")
        add_key = make_safe_key("scan_add_drawer", prod["이름"])
        if st.button("서랍에 추가하기", key=add_key):
            cat_guess = "색조화장품"
            st.session_state.my_drawer.append({"이름": prod["이름"], "유통기한": datetime.today().date(), "별점": 3, "카테고리": cat_guess})
            st.success(f"'{prod['이름']}'이 서랍에 추가되었습니다.")
            st.rerun()

elif choice == "🔎 검색":
    st.header("🔍 제품 검색 & 추천")
    query = st.text_input("예: '민감성 피부용 토너'")
    if st.button("검색 / 추천", key=make_safe_key("search_button", query or "noquery")):
        category = None
        for cat in types:
            if cat in (query or ""):
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
                st.write("🧴 성분:")
                cols = st.columns(len(prod["성분"]))
                for i, ing in enumerate(prod["성분"]):
                    btn_key = make_safe_key("search_ing", prod['이름'], ing)
                    if cols[i].button(ing, key=btn_key):
                        st.session_state.selected_search_product = prod['이름']
                        st.session_state.selected_search_ingredient = ing

                reasons = explain_recommendation(prod, st.session_state.user_skin)
                if reasons:
                    st.write("🤔 이 제품을 추천한 이유:")
                    for r in reasons:
                        st.write(f"- {r}")

                # 이 제품에서 선택된 성분이면 바로 아래에 설명
                if (
                    st.session_state.selected_search_product == prod['이름']
                    and st.session_state.selected_search_ingredient in prod["성분"]
                ):
                    ing = st.session_state.selected_search_ingredient
                    info = ingredient_desc.get(ing, ["정보 없음",""])
                    st.info(f"🔍 {ing} → 장점: {info[0]}, 주의: {info[1]}")

elif choice == "💡 루틴 추천":
    st.header("💡 고민을 말하면 맞춤 루틴 추천")
    concern = st.text_area("피부 고민을 입력하세요 (예: 건조, 트러블, 민감)")
    if st.button("루틴 추천", key=make_safe_key("routine_reco", concern or "no_concern")):
        today = datetime.today().date()
        skin_products = [
            p for p in st.session_state.my_drawer
            if p.get("카테고리") == "피부화장품" and p.get("유통기한") and p["유통기한"] >= today
        ]
        if not skin_products:
            st.warning("서랍에 사용 가능한 피부화장품이 없습니다. 먼저 추가하거나 유통기한을 확인해주세요.")
        else:
            st.success("💧 추천 루틴:")
            morning_order = ["토너","세럼","로션","크림","선크림"]
            evening_order = ["토너","세럼","로션","크림","팩"]

            def routine_for_order(order, products_list):
                routine = []
                used_indices = set()
                for step in order:
                    matched = False
                    for idx, p in enumerate(products_list):
                        if idx in used_indices:
                            continue
                        if step.lower() in p["이름"].lower():
                            routine.append(f"{step}: {p['이름']}")
                            used_indices.add(idx)
                            matched = True
                            break
                    if matched:
                        continue
                    for idx, p in enumerate(products_list):
                        if idx in used_indices:
                            continue
                        routine.append(f"{step}: {p['이름']}")
                        used_indices.add(idx)
                        matched = True
                        break
                return routine

            st.write("🌞 아침 루틴:")
            for r in routine_for_order(morning_order, skin_products):
                st.write(f"- {r}")
            st.write("🌙 저녁 루틴:")
            for r in routine_for_order(evening_order, skin_products):
                st.write(f"- {r}")

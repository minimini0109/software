import streamlit as st
from PIL import Image
import imagehash

# ------------------------------
# 데이터베이스 (예시)
# ------------------------------
cosmetic_db = [
    {"이름": "톤업 선크림 A", "종류": "선크림", "가격": 15000},
    {"이름": "수분크림 B", "종류": "크림", "가격": 20000},
    {"이름": "립밤 C", "종류": "립밤", "가격": 9000},
    {"이름": "틴트 D", "종류": "틴트", "가격": 12000},
]

# ------------------------------
# 기본 세션 상태 설정
# ------------------------------
if "drawer" not in st.session_state:
    st.session_state.drawer = []  # 사용자가 저장한 제품들

if "user_skin" not in st.session_state:
    st.session_state.user_skin = {"피부톤": "봄웜톤"}  # 기본값

# ------------------------------
# 기준 이미지 해시 계산
# ------------------------------
base_img = Image.open("/mnt/data/211110000062839.jpg")
base_hash = imagehash.average_hash(base_img)


def is_allowed_image(uploaded_img):
    """업로드된 이미지가 지정된 이미지(쥬쥬브)와 같은지 판별"""
    try:
        img = Image.open(uploaded_img)
        uploaded_hash = imagehash.average_hash(img)
        diff = base_hash - uploaded_hash
        return diff < 5
    except:
        return False


# ------------------------------
# 이미지 기반 제품 인식 함수
# ------------------------------
def recognize_product_from_image(image):
    if not is_allowed_image(image):
        st.error("⚠️ 죄송합니다. 아직 지원되지 않는 서비스입니다.")
        return None, None, None

    fixed_name = "쥬시 래스팅 틴트 07 쥬쥬브 5.5g - 롬앤"
    fixed_ingredients = ["비타민E", "호호바오일"]

    tone_score = {
        "봄웜톤": 80,
        "가을웜톤": 95,
        "겨울쿨톤": 75,
        "여름쿨톤": 60,
    }

    user_tone = st.session_state.user_skin["피부톤"]
    score = tone_score.get(user_tone, 70)
    reasons = ["웜톤에게 잘어울리는 색깔입니다!"]

    product = {
        "이름": fixed_name,
        "종류": "틴트",
        "성분": fixed_ingredients,
    }

    return product, score, reasons


# ------------------------------
# Streamlit UI 시작
# ------------------------------
st.title("💄 AI 화장품 분석기")

menu = st.sidebar.selectbox("메뉴", ["제품 촬영", "서랍"])

# ---------------------------------
# 1. 제품 촬영
# ---------------------------------
if menu == "제품 촬영":
    st.header("📷 제품 촬영")

    uploaded = st.file_uploader("제품 사진을 업로드하세요", type=["jpg", "png", "jpeg"])

    if uploaded:
        st.image(uploaded, width=250)

        product, score, reasons = recognize_product_from_image(uploaded)

        if product is not None:
            st.success(f"제품명: {product['이름']}")
            st.write(f"종류: {product['종류']}")
            st.write(f"피부톤 점수: {score}점")
            st.write("이유:")
            for r in reasons:
                st.write("- " + r)

            if st.button("서랍에 저장"):
                st.session_state.drawer.append({
                    "이름": product["이름"],
                    "카테고리": [product["종류"]],
                    "별점": 5  # 임시 기본값
                })
                st.success("서랍에 저장되었습니다!")

# ---------------------------------
# 2. 서랍
# ---------------------------------
if menu == "서랍":
    st.header("🗄️ 내 서랍")

    if len(st.session_state.drawer) == 0:
        st.info("아직 저장된 제품이 없습니다.")
    else:
        for idx, item in enumerate(st.session_state.drawer):
            st.subheader(f"▪ {item['이름']}")
            st.write(f"카테고리: {', '.join(item['카테고리'])}")
            st.write(f"만족도: ⭐ {item['별점']}")

            # ---- 유사 제품 추천 기능 ----
            if item['별점'] == 5:
                st.info("✨ 이 제품을 좋아하신다면 이런 제품도 좋아하실 수 있어요!")
                similar = [p for p in cosmetic_db if item['카테고리'][0] in p["종류"]][:3]
                for s in similar:
                    st.write(f"- {s['이름']} ({s['종류']}, {s['가격']}원)")

            # 삭제 버튼
            if st.button(f"삭제 {idx}"):
                st.session_state.drawer.pop(idx)
                st.experimental_rerun()

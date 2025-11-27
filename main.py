import streamlit as st
from PIL import Image
import numpy as np

# ------------------------------------------------
# 기준 이미지 로드
# ------------------------------------------------
try:
    base_img = Image.open("/mnt/data/211110000062839.jpg").convert("RGB")
    base_img_arr = np.array(base_img)
    BASE_LOADED = True
except:
    BASE_LOADED = False
    st.error("⚠️ 기준 이미지 로드 실패 — 모든 이미지는 지원되지 않음으로 처리됩니다.")


# ------------------------------------------------
# 기준 이미지 특징 추출 함수
# ------------------------------------------------
def extract_features(img):
    """8x8 블록 샘플링 + 평균 RGB 추출"""
    img = img.resize((64, 64))  # 빠른 비교용 축소
    arr = np.array(img)

    # 평균 RGB
    mean_rgb = arr.mean(axis=(0, 1))

    # 8x8 블록 평균값
    blocks = []
    for i in range(0, 64, 8):
        for j in range(0, 64, 8):
            block = arr[i:i+8, j:j+8]
            blocks.append(block.mean())

    return np.array([*mean_rgb, *blocks])


# 기준 이미지 특징 생성
if BASE_LOADED:
    base_features = extract_features(base_img)


# ------------------------------------------------
# 업로드 이미지가 기준과 동일한지 판단
# ------------------------------------------------
def is_allowed_image(uploaded_img):

    if not BASE_LOADED:
        return False

    try:
        img = Image.open(uploaded_img).convert("RGB")

        # 1) 크기 비교 (너무 다르면 바로 실격)
        if abs(img.size[0] - base_img.size[0]) > 10:
            return False
        if abs(img.size[1] - base_img.size[1]) > 10:
            return False

        # 2) 특징값 추출
        feat = extract_features(img)

        # 3) 차이 계산
        diff = np.linalg.norm(base_features - feat)

        # 기준(임계값): 300 이하 → 동일 이미지로 간주
        return diff < 300

    except:
        return False


# ------------------------------------------------
# 제품 인식 함수
# ------------------------------------------------
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
    reasons = ["웜톤에게 특히 잘 어울리는 색감입니다!"]

    product = {
        "이름": fixed_name,
        "종류": "틴트",
        "성분": fixed_ingredients,
    }

    return product, score, reasons


# ------------------------------------------------
# Streamlit 세션 초기화
# ------------------------------------------------
if "drawer" not in st.session_state:
    st.session_state.drawer = []

if "user_skin" not in st.session_state:
    st.session_state.user_skin = {"피부톤": "봄웜톤"}


# ------------------------------------------------
# UI
# ------------------------------------------------
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
            st.write("추천 이유:")
            for r in reasons:
                st.write("- " + r)

            if st.button("서랍에 저장"):
                st.session_state.drawer.append({
                    "이름": product["이름"],
                    "카테고리": [product["종류"]],
                    "별점": 5
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

            if item['별점'] == 5:
                st.info("✨ 이 제품을 좋아하신다면 이런 제품도 추천드려요!")
                for s in cosmetic_db:
                    if item['카테고리'][0] in s["종류"]:
                        st.write(f"- {s['이름']} ({s['종류']}, {s['가격']}원)")

            if st.button(f"삭제 {idx}"):
                st.session_state.drawer.pop(idx)
                st.experimental_rerun()

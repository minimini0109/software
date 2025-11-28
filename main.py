{"id":"90012","variant":"standard","title":"화장품 추천 코드 수정"}
<content>
# --- 서랍 추가/삭제 부분 수정 ---
for idx, item in enumerate(list(st.session_state.my_drawer)):
    st.subheader(f"{item['이름']} 🧴")
    days_left = (item['유통기한'] - datetime.today().date()).days
    if days_left < 0:
        st.warning("⚠️ 유통기한이 지났습니다!")
    else:
        st.write(f"남은 사용 가능 기간: {days_left}일")
    st.write(f"⭐ 만족도: {item['별점']}")
    # 삭제 버튼 key 고유화
    del_key = make_safe_key("del", idx, item['이름'], item['유통기한'])
    if st.button("삭제", key=del_key):
        st.session_state.my_drawer.pop(idx)
        st.experimental_rerun()

# --- 서랍 기반 추천 추가 ---
if choice == "🔎 검색":
    st.header("🔍 제품 검색 & 추천")
    query = st.text_input("예: '민감성 피부용 토너'")
    if st.button("검색 / 추천", key=make_safe_key("search_button", query or "noquery")):
        category = None
        # 질의에 타입 이름 포함 여부 체크
        for cat in types:
            if cat in (query or ""):
                category = cat
                break
        results = recommend_products_for_user(query=query, category=category)

        # 추천 이유 표시
        st.subheader("추천 이유")
        if results:
            st.write("- 사용자 피부타입/민감도/트러블 정도 기반 필터 적용")
            st.write("- 검색 키워드 매칭")
            # 서랍에서 만족도 5 제품과 성분 유사 제품 추천
            top_drawer = [p for p in st.session_state.my_drawer if p['별점'] == 5]
            if top_drawer:
                st.write(f"- 서랍 만족도 5 제품과 유사한 제품 포함: {', '.join([p['이름'] for p in top_drawer])}")

        if not results:
            st.warning("❌ 현재 조건에 맞는 제품이 없습니다.")
        else:
            st.success(f"✅ {len(results)}개 제품을 추천해요:")
            for prod in results[:10]:
                st.subheader(f"{prod['이름']} — {prod['종류']}")
                st.write(f"💵 가격: {prod['가격']}원")
                st.write("🧴 성분:")
                for ing in prod["성분"]:
                    btn_key = make_safe_key("search_ing", prod['이름'], ing)
                    # 성분 클릭 시 설명 표시
                    if st.button(ing, key=btn_key):
                        info = ingredient_desc.get(ing, ["정보 없음",""])
                        st.info(f"{ing} → 장점: {info[0]}, 주의: {info[1]}")

# --- 루틴 추천에서 유통기한 지난 제품 제외 ---
if choice == "💡 루틴 추천":
    st.header("💡 고민을 말하면 맞춤 루틴 추천")
    concern = st.text_area("피부 고민을 입력하세요 (예: 건조, 트러블, 민감)")
    if st.button("루틴 추천", key=make_safe_key("routine_reco", concern or "no_concern")):
        # 서랍에서 피부화장품만 골라내고 유통기한 지난 제품 제외
        today = datetime.today().date()
        skin_products = [p for p in st.session_state.my_drawer if p.get("카테고리") == "피부화장품" and p['유통기한'] >= today]
        if not skin_products:
            st.warning("서랍에 사용 가능한 피부화장품이 없습니다. 먼저 추가해주세요.")
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

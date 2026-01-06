import streamlit as st

st.set_page_config(page_title="세션 상태", page_icon="💾")

st.title("💾 세션 상태 관리 (Session State)")
st.write("Streamlit의 핵심 기능인 Session State를 학습합니다.")

st.info("""
**Session State**는 페이지가 다시 실행되어도 데이터를 유지하는 Streamlit의 핵심 기능입니다.
사용자의 상호작용, 대화 히스토리, 설정 등을 저장할 수 있습니다.
""")

st.divider()

# 카운터 예제
st.header("1. 기본 예제: 카운터")

# Session State 초기화
# YOUR CODE HERE - Session State에 "counter" 변수 초기화 (값 0)
# if "counter" not in st.session_state:
#     st.session_state.counter = 0

col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    if st.button("➕ 증가", use_container_width=True):
        # YOUR CODE HERE - Session State의 counter 값 1 증가
        # st.session_state.counter += 1
        pass

with col2:
    st.metric("현재 값", st.session_state.counter)

with col3:
    if st.button("➖ 감소", use_container_width=True):
        st.session_state.counter -= 1

if st.button("🔄 초기화"):
    st.session_state.counter = 0
    # YOUR CODE HERE - st.rerun()을 호출하여 페이지 새로고침
    # st.rerun()

st.caption("페이지를 새로고침해도 카운터 값이 유지됩니다!")

st.divider()

# 메시지 히스토리 예제
st.header("2. 메시지 히스토리")

# YOUR CODE HERE - Session State에 "messages" 리스트 초기화
# if "messages" not in st.session_state:
#     st.session_state.messages = []

message_input = st.text_input("메시지를 입력하세요", key="msg_input")

col1, col2 = st.columns([1, 4])

with col1:
    if st.button("📝 추가", use_container_width=True):
        if message_input:
            # YOUR CODE HERE - Session State의 messages 리스트에 message_input 추가
            # st.session_state.messages.append(message_input)
            st.rerun()

with col2:
    if st.button("🗑️ 전체 삭제", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

if st.session_state.messages:
    st.subheader(f"저장된 메시지 ({len(st.session_state.messages)}개)")
    for idx, msg in enumerate(st.session_state.messages, 1):
        st.write(f"{idx}. {msg}")
else:
    st.info("아직 저장된 메시지가 없습니다.")

st.divider()

# 사용자 설정 예제
st.header("3. 사용자 설정 저장")

# YOUR CODE HERE - Session State에 "user_settings" 딕셔너리 초기화
# if "user_settings" not in st.session_state:
#     st.session_state.user_settings = {
#         "theme": "밝음",
#         "language": "한국어",
#         "notifications": True
#     }

col1, col2 = st.columns(2)

with col1:
    st.subheader("설정 변경")
    
    theme = st.radio(
        "테마",
        ["밝음", "어두움"],
        index=0 if st.session_state.user_settings["theme"] == "밝음" else 1
    )
    
    language = st.selectbox(
        "언어",
        ["한국어", "English", "日本語"],
        index=["한국어", "English", "日本語"].index(st.session_state.user_settings["language"])
    )
    
    notifications = st.checkbox(
        "알림 받기",
        value=st.session_state.user_settings["notifications"]
    )
    
    if st.button("💾 설정 저장", type="primary", use_container_width=True):
        # YOUR CODE HERE - Session State의 user_settings 업데이트
        # st.session_state.user_settings = {
        #     "theme": theme,
        #     "language": language,
        #     "notifications": notifications
        # }
        st.success("✅ 설정이 저장되었습니다!")

with col2:
    st.subheader("현재 설정")
    st.json(st.session_state.user_settings)

st.divider()

# st.rerun() 설명
st.header("4. st.rerun() - 페이지 강제 새로고침")

st.write("""
**st.rerun()**은 현재 스크립트를 처음부터 다시 실행합니다.
Session State의 값을 변경한 후 즉시 UI를 업데이트하고 싶을 때 사용합니다.
""")

if "click_count" not in st.session_state:
    st.session_state.click_count = 0

st.write(f"버튼 클릭 횟수: **{st.session_state.click_count}**")

col1, col2 = st.columns(2)

with col1:
    if st.button("🔄 Rerun 사용", use_container_width=True):
        st.session_state.click_count += 1
        st.rerun()  # 즉시 페이지 새로고침

with col2:
    if st.button("⏸️ Rerun 미사용", use_container_width=True):
        st.session_state.click_count += 1
        # rerun()을 호출하지 않으면 다음 interaction에서 업데이트됨

st.caption("'Rerun 사용' 버튼은 클릭하면 즉시 카운트가 업데이트되지만, 'Rerun 미사용'은 다음 interaction에서 업데이트됩니다.")

st.divider()

# 모든 Session State 보기
st.header("5. 전체 Session State 확인")

if st.checkbox("🔍 모든 Session State 보기"):
    st.write("현재 저장된 모든 Session State 변수:")
    
    # Streamlit 내부 변수 제외
    user_states = {k: v for k, v in st.session_state.items() 
                   if not k.startswith('_') and not k.startswith('FormSubmitter')}
    
    st.json(user_states)
    
    st.caption(f"총 {len(user_states)}개의 변수가 저장되어 있습니다.")


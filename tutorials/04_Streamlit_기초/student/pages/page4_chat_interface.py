import streamlit as st
import time

st.set_page_config(page_title="채팅 인터페이스", page_icon="💬", layout="wide")

st.title("💬 채팅 인터페이스 구축")
st.write("Streamlit의 채팅 UI 컴포넌트를 학습합니다.")

st.info("""
**채팅 UI**는 대화형 AI 애플리케이션을 만드는 핵심 요소입니다.
- `st.chat_message()`: 채팅 메시지 컨테이너
- `st.chat_input()`: 채팅 입력창
- `st.empty()`: 동적 업데이트를 위한 빈 컨테이너
""")

st.divider()

# 기본 채팅 메시지
st.header("1. st.chat_message() - 기본 메시지")

# YOUR CODE HERE - st.chat_message("user")를 사용하여 사용자 메시지 표시
# with st.chat_message("user"):
#     st.write("안녕하세요! 이것은 사용자 메시지입니다.")

# YOUR CODE HERE - st.chat_message("assistant")를 사용하여 AI 메시지 표시
# with st.chat_message("assistant"):
#     st.write("안녕하세요! 저는 AI 어시스턴트입니다.")

with st.chat_message("user", avatar="🧑‍💻"):
    st.write("커스텀 아바타도 사용할 수 있습니다.")

with st.chat_message("assistant", avatar="🤖"):
    st.write("다양한 이모지를 아바타로 사용할 수 있습니다!")

st.divider()

# 실제 채팅 앱 예제
st.header("2. 실제 채팅 앱 구현 (st.chat_input + Session State)")

# Session State 초기화
# YOUR CODE HERE - Session State에 "chat_messages" 리스트 초기화
# if "chat_messages" not in st.session_state:
#     st.session_state.chat_messages = []

# 이전 메시지 표시
for message in st.session_state.chat_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 새 메시지 입력
if user_input := st.chat_input("메시지를 입력하세요..."):
    # 사용자 메시지 추가
    st.session_state.chat_messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # AI 응답 (간단한 에코)
    response = f"'{user_input}'에 대한 응답입니다. (실제로는 LLM이 응답을 생성합니다)"
    
    with st.chat_message("assistant"):
        st.markdown(response)
    
    st.session_state.chat_messages.append({"role": "assistant", "content": response})

if st.button("🗑️ 대화 초기화"):
    st.session_state.chat_messages = []
    st.rerun()

st.divider()

# 스트리밍 효과
st.header("3. st.empty() - 스트리밍 효과")

st.write("""
**st.empty()**를 사용하면 동일한 위치에 내용을 계속 업데이트할 수 있습니다.
이는 LLM의 스트리밍 응답을 구현하는데 핵심적인 기능입니다.
""")

if st.button("▶️ 스트리밍 효과 시연", type="primary"):
    with st.chat_message("assistant"):
        # YOUR CODE HERE - st.empty()를 사용하여 빈 placeholder 생성
        # message_placeholder = st.empty()
        full_response = ""
        
        sample_text = "안녕하세요! 이것은 스트리밍 효과의 시연입니다. 실제 LLM 응답처럼 텍스트가 점진적으로 나타납니다."
        
        # YOUR CODE HERE - 반복문으로 글자를 하나씩 추가하며 placeholder 업데이트
        # for char in sample_text:
        #     full_response += char
        #     message_placeholder.markdown(full_response + "▌")
        #     time.sleep(0.03)
        
        message_placeholder.markdown(full_response)

st.divider()

# 메시지에 다양한 컨텐츠 포함
st.header("4. 메시지 내 다양한 컨텐츠")

with st.chat_message("user"):
    st.write("**사용자**: 데이터를 분석해주세요.")

with st.chat_message("assistant"):
    st.write("**AI**: 분석 결과입니다:")
    
    # 표
    import pandas as pd
    import numpy as np
    
    data = pd.DataFrame({
        '항목': ['A', 'B', 'C'],
        '값': [10, 20, 30]
    })
    st.dataframe(data, use_container_width=True)
    
    # 차트
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['a', 'b', 'c']
    )
    st.line_chart(chart_data)
    
    # 코드
    st.code('''def analyze_data(df):
    return df.describe()''', language='python')

st.caption("채팅 메시지 내부에 텍스트뿐만 아니라 표, 차트, 코드 등 다양한 요소를 포함할 수 있습니다.")

st.divider()

# 통계 정보
st.header("5. 채팅 통계")

if st.session_state.chat_messages:
    user_msgs = len([m for m in st.session_state.chat_messages if m["role"] == "user"])
    ai_msgs = len([m for m in st.session_state.chat_messages if m["role"] == "assistant"])
    
    col1, col2, col3 = st.columns(3)
    col1.metric("전체 메시지", len(st.session_state.chat_messages))
    col2.metric("사용자 메시지", user_msgs)
    col3.metric("AI 응답", ai_msgs)
else:
    st.info("아직 대화가 없습니다. 위에서 메시지를 입력해보세요!")


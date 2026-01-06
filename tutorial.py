"""
LangChain Chat 앱 개발 튜토리얼
각 섹션을 순서대로 실행하면서 학습할 수 있습니다.
"""

# =============================================================================
# 1. 기본 설정
# =============================================================================

"""
## Streamlit 기본 구조

Streamlit은 Python 스크립트를 웹 앱으로 변환하는 프레임워크입니다.
"""

import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="튜토리얼",
    page_icon="📚",
    layout="wide"
)

# 제목과 설명
st.title("📚 LangChain + Streamlit 튜토리얼")
st.markdown("이 튜토리얼은 LangChain Chat 앱을 만들기 위한 핵심 개념을 설명합니다.")

st.divider()

# =============================================================================
# 2. Session State - 상태 관리
# =============================================================================

st.header("1️⃣ Session State - 상태 관리")

st.markdown("""
Streamlit은 사용자가 상호작용할 때마다 스크립트를 처음부터 다시 실행합니다.
`st.session_state`를 사용하면 재실행 간에 데이터를 유지할 수 있습니다.
""")

# Session State 초기화
if "counter" not in st.session_state:
    st.session_state.counter = 0

if "message_history" not in st.session_state:
    st.session_state.message_history = []

# 버튼과 카운터
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("카운터 증가"):
        st.session_state.counter += 1

with col2:
    if st.button("카운터 초기화"):
        st.session_state.counter = 0

with col3:
    st.metric("현재 카운터", st.session_state.counter)

st.code("""
# Session State 사용 예시
if "counter" not in st.session_state:
    st.session_state.counter = 0

if st.button("증가"):
    st.session_state.counter += 1
    
st.write(f"현재 값: {st.session_state.counter}")
""", language="python")

st.divider()

# =============================================================================
# 3. 레이아웃
# =============================================================================

st.header("2️⃣ 레이아웃 구성")

st.markdown("Streamlit은 다양한 레이아웃 옵션을 제공합니다.")

# 컬럼
st.subheader("컬럼 (Columns)")
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    st.info("넓은 컬럼 (2)")
with col2:
    st.success("컬럼 (1)")
with col3:
    st.warning("컬럼 (1)")

st.code("""
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    st.write("첫 번째 컬럼")
""", language="python")

# 사이드바
st.subheader("사이드바 (Sidebar)")
with st.sidebar:
    st.header("사이드바 예시")
    sidebar_option = st.selectbox(
        "옵션 선택",
        ["옵션 1", "옵션 2", "옵션 3"]
    )
    st.write(f"선택됨: {sidebar_option}")

st.code("""
with st.sidebar:
    st.header("설정")
    option = st.selectbox("선택", ["A", "B", "C"])
""", language="python")

# Expander
st.subheader("펼침/접힘 (Expander)")
with st.expander("코드 보기"):
    st.code("""
with st.expander("자세히 보기"):
    st.write("숨겨진 내용")
    """, language="python")

st.divider()

# =============================================================================
# 4. 입력 위젯
# =============================================================================

st.header("3️⃣ 입력 위젯")

col1, col2 = st.columns(2)

with col1:
    st.subheader("텍스트 입력")
    text_input = st.text_input("한 줄 입력", placeholder="여기에 입력하세요")
    text_area = st.text_area("여러 줄 입력", height=100)
    
    st.subheader("선택")
    selectbox = st.selectbox("드롭다운", ["선택 1", "선택 2", "선택 3"])

with col2:
    st.subheader("버튼")
    if st.button("일반 버튼"):
        st.success("클릭됨!")
    
    if st.button("Primary 버튼", type="primary"):
        st.info("Primary 클릭!")
    
    if st.button("Secondary 버튼", type="secondary"):
        st.warning("Secondary 클릭!")

st.code("""
# 입력 위젯 예시
text = st.text_input("이름", placeholder="이름 입력")
choice = st.selectbox("선택", ["A", "B", "C"])

if st.button("확인", type="primary"):
    st.write(f"{text}님이 {choice}를 선택했습니다.")
""", language="python")

st.divider()

# =============================================================================
# 5. 채팅 UI
# =============================================================================

st.header("4️⃣ 채팅 인터페이스")

st.markdown("Streamlit의 채팅 전용 UI 컴포넌트를 사용합니다.")

# 채팅 히스토리 표시
if st.session_state.message_history:
    for msg in st.session_state.message_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# 채팅 입력
if chat_input := st.chat_input("메시지를 입력하세요..."):
    # 사용자 메시지 추가
    st.session_state.message_history.append({
        "role": "user",
        "content": chat_input
    })
    
    with st.chat_message("user"):
        st.markdown(chat_input)
    
    # AI 응답 (시뮬레이션)
    response = f"당신이 말한 '{chat_input}'에 대한 응답입니다."
    
    st.session_state.message_history.append({
        "role": "assistant",
        "content": response
    })
    
    with st.chat_message("assistant"):
        st.markdown(response)
    
    st.rerun()

st.code("""
# 채팅 UI 예시
if prompt := st.chat_input("메시지 입력"):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        st.markdown(f"응답: {prompt}")
""", language="python")

st.divider()

# =============================================================================
# 6. LangChain 통합 (이론)
# =============================================================================

st.header("5️⃣ LangChain 통합")

st.markdown("""
LangChain은 LLM 애플리케이션을 쉽게 만들 수 있는 프레임워크입니다.
""")

st.subheader("핵심 개념")

st.markdown("""
**1. Messages (메시지 타입)**
- `HumanMessage`: 사용자가 보낸 메시지
- `AIMessage`: AI가 생성한 응답
- `SystemMessage`: 시스템 프롬프트 (AI의 역할 정의)

**2. Chat Models (챗 모델)**
- `ChatOpenAI`: OpenAI의 GPT 모델 사용
- `stream()`: 실시간 스트리밍 응답
- `invoke()`: 전체 응답을 한 번에 생성

**3. Message Flow (메시지 흐름)**
""")

st.code("""
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# 1. 모델 초기화
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7,
    streaming=True,
    api_key="your-api-key"
)

# 2. 메시지 구성
messages = [
    SystemMessage(content="당신은 친절한 AI입니다."),
    HumanMessage(content="안녕하세요!"),
    AIMessage(content="안녕하세요! 무엇을 도와드릴까요?"),
    HumanMessage(content="파이썬에 대해 알려주세요.")
]

# 3. 스트리밍 응답
for chunk in llm.stream(messages):
    print(chunk.content, end="")
""", language="python")

st.divider()

# =============================================================================
# 7. 검색 통합 (이론)
# =============================================================================

st.header("6️⃣ 웹 검색 통합")

st.markdown("""
최신 정보나 외부 지식이 필요한 경우 검색 엔진을 통합할 수 있습니다.
""")

st.subheader("검색 통합 패턴")

st.code("""
# 1. 검색 수행
from langchain_community.tools.tavily_search import TavilySearchResults

search_tool = TavilySearchResults(max_results=5, api_key="...")
search_results = search_tool.invoke("파이썬이란?")

# 2. 검색 결과를 프롬프트에 포함
augmented_prompt = f'''
사용자 질문: 파이썬이란?

검색 결과:
{search_results}

위 검색 결과를 참고하여 답변해주세요.
'''

# 3. LLM에게 전달
messages = [HumanMessage(content=augmented_prompt)]
response = llm.invoke(messages)
""", language="python")

st.divider()

# =============================================================================
# 8. 종합 예제
# =============================================================================

st.header("7️⃣ 종합 예제 구조")

st.markdown("""
완전한 채팅 앱의 구조를 살펴봅니다.
""")

st.code("""
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage

# 1. 설정
st.set_page_config(page_title="Chat App")

# 2. Session State 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

if "llm" not in st.session_state:
    st.session_state.llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        streaming=True
    )

# 3. UI
st.title("💬 Chat App")

# 4. 히스토리 표시
for message in st.session_state.messages:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(message.content)

# 5. 입력 처리
if prompt := st.chat_input("메시지 입력"):
    # 사용자 메시지 추가
    st.session_state.messages.append(HumanMessage(content=prompt))
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # AI 응답 생성
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        for chunk in st.session_state.llm.stream(st.session_state.messages):
            full_response += chunk.content
            placeholder.markdown(full_response + "▌")
        
        placeholder.markdown(full_response)
    
    # AI 메시지 추가
    st.session_state.messages.append(AIMessage(content=full_response))
    st.rerun()
""", language="python")

st.divider()

# =============================================================================
# 마무리
# =============================================================================

st.header("📚 다음 단계")

st.markdown("""
이제 기본 개념을 이해했다면:

1. **app1.py** - 기본 채팅 앱 구현
2. **app2.py** - 다중 세션 관리 추가
3. **app3.py** - 응답 수정 기능 추가
4. **app4.py** - 검색 통합 및 시스템 프롬프트 추가

각 파일을 순서대로 학습하면서 기능을 점진적으로 추가해보세요!
""")

with st.expander("참고 자료"):
    st.markdown("""
    - [Streamlit 공식 문서](https://docs.streamlit.io)
    - [LangChain 공식 문서](https://python.langchain.com)
    - [OpenAI API 문서](https://platform.openai.com/docs)
    """)


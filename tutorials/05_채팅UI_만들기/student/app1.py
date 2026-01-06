"""
app1.py - 기본 채팅 앱
======================

목적:
    LangChain과 Streamlit을 결합한 가장 기본적인 채팅 애플리케이션 구현
    
주요 기능:
    1. ChatOpenAI 모델 초기화 및 설정
    2. Session State를 통한 대화 이력 관리
    3. 스트리밍 방식의 AI 응답 구현
    4. 사이드바를 통한 모델 선택 및 설정
    5. 대화 히스토리 초기화 기능
    
학습 포인트:
    - Streamlit의 st.session_state를 사용한 상태 관리
    - LangChain의 HumanMessage/AIMessage를 통한 메시지 관리
    - llm.stream()을 통한 실시간 응답 스트리밍
    - st.chat_message()와 st.chat_input()을 통한 채팅 UI 구현
"""

import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from dotenv import load_dotenv
import os

# .env 파일에서 환경변수(API 키 등) 로드
load_dotenv()

# ============================================================================
# 페이지 설정
# ============================================================================
# YOUR CODE HERE - st.set_page_config()를 사용하여 페이지 설정
# page_title="LangChain Chat", page_icon="💬", layout="wide"
# 
# st.set_page_config()는 반드시 다른 Streamlit 명령보다 먼저 호출되어야 합니다.
# 페이지 제목, 아이콘, 레이아웃 등을 설정합니다.

st.title("💬 LangChain Chat")

# ============================================================================
# 모델 설정
# ============================================================================
# 사용 가능한 OpenAI 모델 목록
# key: 사용자에게 표시될 이름, value: 실제 모델 ID
MODELS = {
    "gpt-4.1-nano": "gpt-4.1-nano-2025-04-14",
    "gpt-4.1-mini": "gpt-4.1-mini-2025-04-14",
    "gpt-5-mini": "gpt-5-mini-2025-08-07",
    "gpt-5-nano": "gpt-5-nano-2025-08-07"
}

# ============================================================================
# Session State 초기화
# ============================================================================
# Streamlit의 Session State는 페이지가 새로고침되어도 데이터를 유지합니다.
# 채팅 앱에서는 대화 이력과 LLM 인스턴스를 저장하는 데 사용됩니다.

# YOUR CODE HERE - Session State에 "messages" 리스트 초기화
# if "messages" not in st.session_state:
#     st.session_state.messages = []
# 
# messages: 사용자와 AI의 대화 이력을 저장하는 리스트
# HumanMessage와 AIMessage 객체들이 순서대로 저장됩니다.

# 현재 선택된 모델 이름을 저장
if "selected_model" not in st.session_state:
    st.session_state.selected_model = "gpt-4.1-mini"

# YOUR CODE HERE - Session State에 "llm" 초기화 (ChatOpenAI 사용)
# if "llm" not in st.session_state:
#     st.session_state.llm = ChatOpenAI(
#         model=MODELS[st.session_state.selected_model],
#         temperature=0.7,
#         streaming=True,
#         api_key=os.getenv("OPENAI_API_KEY")
#     )
# 
# llm: LangChain의 ChatOpenAI 인스턴스
# - model: 사용할 OpenAI 모델 ID
# - temperature: 응답의 창의성 조절 (0.0 = 결정적, 1.0 = 창의적)
# - streaming: True로 설정하면 응답을 실시간으로 받을 수 있습니다
# - api_key: .env 파일에서 로드한 OpenAI API 키

# ============================================================================
# 사이드바: 설정 패널
# ============================================================================
with st.sidebar:
    st.header("설정")
    
    # ------------------------------------------------------------------------
    # 모델 선택 드롭다운
    # ------------------------------------------------------------------------
    # selectbox: 드롭다운 메뉴를 생성하여 사용자가 모델을 선택할 수 있게 합니다
    model_choice = st.selectbox(
        "모델 선택",
        options=list(MODELS.keys()),  # 선택 가능한 모델 목록
        index=list(MODELS.keys()).index(st.session_state.selected_model),  # 현재 선택된 모델의 인덱스
        key="model_selectbox"  # Streamlit 내부에서 위젯을 구분하는 고유 키
    )
    
    # 모델이 변경되었을 때 LLM 인스턴스를 새로 생성
    if model_choice != st.session_state.selected_model:
        st.session_state.selected_model = model_choice
        # 새로운 모델로 ChatOpenAI 인스턴스 재생성
        st.session_state.llm = ChatOpenAI(
            model=MODELS[model_choice],
            temperature=0.7,
            streaming=True,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        st.success(f"모델이 {model_choice}로 변경되었습니다.")
    
    st.divider()
    
    # ------------------------------------------------------------------------
    # 대화 히스토리 초기화 버튼
    # ------------------------------------------------------------------------
    if st.button("대화 히스토리 초기화"):
        # messages 리스트를 비워서 대화 이력 삭제
        st.session_state.messages = []
        # YOUR CODE HERE - st.rerun()을 호출하여 페이지 새로고침
        # 
        # st.rerun()은 페이지를 처음부터 다시 실행합니다.
        # 이를 통해 변경된 Session State가 UI에 즉시 반영됩니다.

    st.divider()
    
    # ------------------------------------------------------------------------
    # 대화 히스토리 요약 표시
    # ------------------------------------------------------------------------
    st.subheader("대화 히스토리")
    if st.session_state.messages:
        # HumanMessage와 AIMessage의 총 개수 계산
        total_messages = len([msg for msg in st.session_state.messages if isinstance(msg, (HumanMessage, AIMessage))])
        st.write(f"총 메시지 수: {total_messages}")
        
        # expander: 클릭하면 내용이 펼쳐지는 접을 수 있는 섹션
        with st.expander("전체 히스토리 보기"):
            # 모든 메시지를 순서대로 표시
            for idx, msg in enumerate(st.session_state.messages):
                if isinstance(msg, HumanMessage):
                    st.markdown(f"**사용자 [{idx+1}]:** {msg.content}")
                elif isinstance(msg, AIMessage):
                    st.markdown(f"**AI [{idx+1}]:** {msg.content}")
    else:
        st.write("대화 히스토리가 없습니다.")

# ============================================================================
# 메인 영역: 채팅 인터페이스
# ============================================================================

# ----------------------------------------------------------------------------
# 이전 메시지 표시
# ----------------------------------------------------------------------------
# Session State에 저장된 모든 대화 이력을 화면에 표시합니다.
# 페이지를 새로고침해도 대화 이력이 유지되어 보입니다.
for message in st.session_state.messages:
    if isinstance(message, HumanMessage):
        # YOUR CODE HERE - st.chat_message("user")를 사용하여 사용자 메시지 표시
        # with st.chat_message("user"):
        #     st.markdown(message.content)
        # 
        # st.chat_message("user"): 사용자 메시지를 위한 채팅 버블 생성
        # 기본적으로 오른쪽에 사용자 아이콘과 함께 표시됩니다.
        pass
    elif isinstance(message, AIMessage):
        # AI 응답 메시지 표시
        with st.chat_message("assistant"):
            st.markdown(message.content)

# ----------------------------------------------------------------------------
# 새 메시지 입력 및 처리
# ----------------------------------------------------------------------------
# YOUR CODE HERE - st.chat_input()을 사용하여 사용자 입력 받기
# if prompt := st.chat_input("메시지를 입력하세요..."):
# 
# st.chat_input(): 채팅 화면 하단에 고정된 입력창 생성
# 사용자가 메시지를 입력하고 Enter를 누르면 prompt 변수에 저장됩니다.
# := 연산자(walrus operator)는 할당과 동시에 조건 검사를 수행합니다.

if False:  # 위의 YOUR CODE HERE를 채우면 이 줄을 삭제하세요
    # ------------------------------------------------------------------------
    # 1단계: 사용자 메시지 저장 및 표시
    # ------------------------------------------------------------------------
    # YOUR CODE HERE - HumanMessage를 생성하여 messages에 추가
    # st.session_state.messages.append(HumanMessage(content=prompt))
    # 
    # HumanMessage: LangChain에서 사용자의 메시지를 표현하는 객체
    # 대화 이력에 추가하여 LLM이 맥락을 이해할 수 있게 합니다.
    
    # 사용자 메시지를 화면에 즉시 표시
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # ------------------------------------------------------------------------
    # 2단계: AI 응답 생성 (스트리밍 방식)
    # ------------------------------------------------------------------------
    with st.chat_message("assistant"):
        # YOUR CODE HERE - st.empty()를 사용하여 스트리밍 효과 구현
        # message_placeholder = st.empty()
        # 
        # st.empty(): 비어있는 컨테이너를 생성하여 나중에 내용을 업데이트할 수 있게 합니다.
        # 스트리밍 응답을 실시간으로 표시하기 위해 사용됩니다.
        
        full_response = ""
        
        # YOUR CODE HERE - llm.stream()을 사용하여 스트리밍 응답 받기
        # for chunk in st.session_state.llm.stream(st.session_state.messages):
        #     full_response += chunk.content
        #     message_placeholder.markdown(full_response + "▌")
        # 
        # llm.stream(): LLM의 응답을 청크(chunk) 단위로 실시간으로 받습니다.
        # 각 청크는 AIMessageChunk 객체이며, .content 속성에 텍스트가 들어있습니다.
        # "▌"는 타이핑 중임을 나타내는 커서 효과입니다.
        # 
        # st.session_state.messages를 전달하여 전체 대화 이력을 LLM에게 제공합니다.
        # 이를 통해 LLM이 이전 대화를 참고하여 맥락에 맞는 답변을 생성합니다.
        
        # 스트리밍이 완료되면 커서를 제거하고 최종 응답 표시
        # message_placeholder.markdown(full_response)
    
    # ------------------------------------------------------------------------
    # 3단계: AI 응답 저장
    # ------------------------------------------------------------------------
    # YOUR CODE HERE - AIMessage를 생성하여 messages에 추가
    # st.session_state.messages.append(AIMessage(content=full_response))
    # 
    # AIMessage: LangChain에서 AI의 응답을 표현하는 객체
    # 대화 이력에 추가하여 다음 응답 시 맥락으로 사용됩니다.


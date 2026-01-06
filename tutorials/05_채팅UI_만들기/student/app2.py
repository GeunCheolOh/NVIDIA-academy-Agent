"""
app2.py - 세션 관리 채팅 앱
===========================

목적:
    여러 대화를 동시에 관리할 수 있는 다중 세션 채팅 애플리케이션 구현
    
주요 기능:
    1. UUID를 사용한 고유 대화 세션 생성
    2. 여러 대화를 동시에 관리 (conversations 딕셔너리)
    3. 대화 세션 간 전환 기능
    4. 각 세션별 독립적인 메시지 이력 관리
    5. 대화 목록 표시 및 삭제 기능
    
학습 포인트:
    - uuid.uuid4()를 사용한 고유 ID 생성
    - 딕셔너리를 사용한 복잡한 데이터 구조 관리
    - datetime을 사용한 타임스탬프 기록
    - st.columns()를 사용한 레이아웃 배치
    - 세션별 데이터 격리 및 관리
    
app1.py와의 차이점:
    - app1: 단일 대화만 관리 (messages 리스트)
    - app2: 여러 대화 동시 관리 (conversations 딕셔너리)
"""

import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from dotenv import load_dotenv
import os
from datetime import datetime  # 대화 생성 시간 기록용
import uuid  # 고유 ID 생성용

load_dotenv()

st.set_page_config(page_title="LangChain Chat", page_icon="💬", layout="wide")

# ============================================================================
# 모델 설정
# ============================================================================
MODELS = {
    "gpt-4.1-nano": "gpt-4.1-nano-2025-04-14",
    "gpt-4.1-mini": "gpt-4.1-mini-2025-04-14",
    "gpt-5-mini": "gpt-5-mini-2025-08-07",
    "gpt-5-nano": "gpt-5-nano-2025-08-07"
}

# ============================================================================
# Session State 초기화 - 다중 대화 세션 관리
# ============================================================================
# YOUR CODE HERE - Session State에 "conversations" 딕셔너리 초기화
# 첫 대화 세션을 uuid로 생성하고, title, messages, created_at 포함
# if "conversations" not in st.session_state:
#     first_id = str(uuid.uuid4())
#     st.session_state.conversations = {
#         first_id: {
#             "id": first_id,
#             "title": "새 대화",
#             "messages": [],
#             "created_at": datetime.now()
#         }
#     }
#     st.session_state.active_conversation_id = first_id
# 
# conversations 구조 설명:
# {
#     "uuid-1": {
#         "id": "uuid-1",              # 대화의 고유 ID
#         "title": "파이썬 질문",       # 대화 제목 (첫 메시지로 자동 생성)
#         "messages": [...],           # 이 대화의 메시지 이력
#         "created_at": datetime(...)  # 대화 생성 시간
#     },
#     "uuid-2": { ... },  # 다른 대화
#     ...
# }
# 
# uuid.uuid4(): 전역적으로 고유한 ID를 생성합니다.
# 예: "550e8400-e29b-41d4-a716-446655440000"
# 
# active_conversation_id: 현재 사용자가 보고 있는 대화의 ID

# 현재 선택된 모델
if "selected_model" not in st.session_state:
    st.session_state.selected_model = "gpt-4.1-mini"

# ChatOpenAI LLM 인스턴스 (모든 대화에서 공유)
if "llm" not in st.session_state:
    st.session_state.llm = ChatOpenAI(
        model=MODELS[st.session_state.selected_model],
        temperature=0.7,
        streaming=True,
        api_key=os.getenv("OPENAI_API_KEY")
    )

# ============================================================================
# 헬퍼 함수들
# ============================================================================

def create_new_conversation():
    """
    새로운 대화 세션을 생성하는 함수
    
    동작:
        1. UUID로 고유 ID 생성
        2. conversations 딕셔너리에 새 세션 추가
        3. active_conversation_id를 새 세션으로 변경
    """
    # YOUR CODE HERE - 새 대화 세션 생성 (uuid 사용)
    # new_id = str(uuid.uuid4())
    # st.session_state.conversations[new_id] = {
    #     "id": new_id,
    #     "title": "새 대화",
    #     "messages": [],
    #     "created_at": datetime.now()
    # }
    # st.session_state.active_conversation_id = new_id
    # 
    # 이 함수 호출 후에는 st.rerun()을 호출하여 
    # UI가 새 대화를 즉시 반영하도록 해야 합니다.
    pass

def get_conversation_title(messages):
    """
    대화의 제목을 자동으로 생성하는 함수
    
    Args:
        messages: 대화의 메시지 리스트
        
    Returns:
        대화 제목 (첫 번째 사용자 메시지의 처음 30자)
    """
    if not messages:
        return "새 대화"
    
    # 첫 번째 HumanMessage 찾기
    first_user_msg = next((msg.content for msg in messages if isinstance(msg, HumanMessage)), None)
    
    if first_user_msg:
        # 30자로 자르고 길면 "..." 추가
        return first_user_msg[:30] + "..." if len(first_user_msg) > 30 else first_user_msg
    return "새 대화"

def delete_conversation(conv_id):
    """
    대화 세션을 삭제하는 함수
    
    Args:
        conv_id: 삭제할 대화의 ID
        
    주의사항:
        - 최소 1개의 대화는 유지되어야 함
        - 현재 활성 대화를 삭제하면 다른 대화로 자동 전환
    """
    # 최소 1개의 대화는 남겨둠
    if len(st.session_state.conversations) > 1:
        del st.session_state.conversations[conv_id]
        
        # 현재 보고 있던 대화가 삭제되었다면 다른 대화로 이동
        if st.session_state.active_conversation_id == conv_id:
            st.session_state.active_conversation_id = list(st.session_state.conversations.keys())[0]

# ============================================================================
# 현재 활성 대화 가져오기
# ============================================================================
# current_conv: 현재 사용자가 보고 있는 대화 세션의 데이터
# 이 변수를 통해 현재 대화의 messages, title 등에 접근합니다
current_conv = st.session_state.conversations[st.session_state.active_conversation_id]

# ============================================================================
# 상단 헤더: 제목 + 새 대화 버튼
# ============================================================================
# YOUR CODE HERE - st.columns()를 사용하여 제목과 버튼을 나란히 배치 (6:1 비율)
# col1, col2 = st.columns([6, 1])
# 
# st.columns([6, 1]): 화면을 6:1 비율로 나눕니다
# - col1: 넓은 영역 (제목 표시)
# - col2: 좁은 영역 (버튼 배치)
col1, col2 = None, None  # 위의 YOUR CODE HERE를 채우면 이 줄을 삭제하세요

if col1 and col2:  # YOUR CODE HERE를 채우면 자동으로 활성화됨
    with col1:
        st.title("💬 LangChain Chat")
    with col2:
        # YOUR CODE HERE - "새 대화" 버튼 추가 (클릭 시 create_new_conversation 호출)
        # if st.button("➕ 새 대화", use_container_width=True):
        #     create_new_conversation()
        #     st.rerun()
        # 
        # use_container_width=True: 버튼이 컬럼의 전체 너비를 차지하게 합니다
        # st.rerun(): 페이지를 새로고침하여 새로운 대화가 즉시 표시되도록 합니다
        pass

# ============================================================================
# 사이드바: 설정 및 대화 목록
# ============================================================================
with st.sidebar:
    st.header("설정")
    
    # ------------------------------------------------------------------------
    # 모델 선택
    # ------------------------------------------------------------------------
    model_choice = st.selectbox(
        "모델 선택",
        options=list(MODELS.keys()),
        index=list(MODELS.keys()).index(st.session_state.selected_model),
        key="model_selectbox"
    )
    
    # 모델 변경 시 LLM 인스턴스 재생성
    if model_choice != st.session_state.selected_model:
        st.session_state.selected_model = model_choice
        st.session_state.llm = ChatOpenAI(
            model=MODELS[model_choice],
            temperature=0.7,
            streaming=True,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        st.success(f"모델이 {model_choice}로 변경되었습니다.")
    
    st.divider()
    
    # ------------------------------------------------------------------------
    # 대화 세션 목록
    # ------------------------------------------------------------------------
    st.subheader("대화 세션")
    
    # YOUR CODE HERE - conversations를 created_at 기준으로 정렬 (최신순)
    # sorted_convs = sorted(
    #     st.session_state.conversations.values(),
    #     key=lambda x: x["created_at"],
    #     reverse=True
    # )
    # 
    # sorted(): 리스트를 정렬합니다
    # - key: 정렬 기준 (여기서는 created_at 필드)
    # - reverse=True: 내림차순 정렬 (최신 대화가 위로)
    # 
    # conversations.values(): 딕셔너리의 값들(대화 객체들)만 가져옵니다
    
    sorted_convs = []  # 위의 YOUR CODE HERE를 채우면 이 줄을 삭제하세요
    
    # 각 대화를 버튼으로 표시
    for conv in sorted_convs:
        # 현재 활성화된 대화인지 확인
        is_active = conv["id"] == st.session_state.active_conversation_id
        
        # 대화 버튼과 삭제 버튼을 나란히 배치 (4:1 비율)
        col1, col2 = st.columns([4, 1])
        
        with col1:
            # 활성 대화는 primary(강조), 비활성은 secondary(일반) 스타일
            button_type = "primary" if is_active else "secondary"
            title = get_conversation_title(conv["messages"])
            
            # 대화 선택 버튼
            if st.button(
                f"{'📌' if is_active else '💬'} {title}",
                key=f"conv_{conv['id']}",  # 각 버튼마다 고유 키 필요
                use_container_width=True,
                type=button_type
            ):
                # 클릭하면 해당 대화로 전환
                st.session_state.active_conversation_id = conv["id"]
                st.rerun()
        
        with col2:
            # 대화가 2개 이상일 때만 삭제 버튼 표시
            if len(st.session_state.conversations) > 1:
                if st.button("🗑️", key=f"del_{conv['id']}", use_container_width=True):
                    delete_conversation(conv["id"])
                    st.rerun()
    
    st.divider()
    
    # ------------------------------------------------------------------------
    # 현재 대화 정보
    # ------------------------------------------------------------------------
    st.subheader("현재 대화 정보")
    if current_conv["messages"]:
        # 메시지 통계 표시
        total_messages = len([msg for msg in current_conv["messages"] if isinstance(msg, (HumanMessage, AIMessage))])
        st.write(f"총 메시지 수: {total_messages}")
        st.write(f"생성 시간: {current_conv['created_at'].strftime('%Y-%m-%d %H:%M')}")
        
        # 전체 대화 이력을 접을 수 있는 영역으로 표시
        with st.expander("전체 히스토리 보기"):
            for idx, msg in enumerate(current_conv["messages"]):
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
# 현재 대화의 이전 메시지 표시
# ----------------------------------------------------------------------------
# current_conv["messages"]에서 메시지를 가져와 표시합니다
# 대화를 전환하면 다른 대화의 메시지가 표시됩니다
for message in current_conv["messages"]:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(message.content)

# ----------------------------------------------------------------------------
# 새 메시지 입력 및 처리
# ----------------------------------------------------------------------------
if prompt := st.chat_input("메시지를 입력하세요..."):
    # YOUR CODE HERE - 현재 대화의 messages에 HumanMessage 추가
    # current_conv["messages"].append(HumanMessage(content=prompt))
    # 
    # 중요: st.session_state.messages가 아닌 current_conv["messages"]에 추가
    # 이렇게 하면 현재 활성화된 대화에만 메시지가 저장됩니다
    
    # 사용자 메시지 즉시 표시
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # AI 응답 생성 (스트리밍)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # YOUR CODE HERE - 현재 대화의 messages를 사용하여 llm.stream() 호출
        # for chunk in st.session_state.llm.stream(current_conv["messages"]):
        #     full_response += chunk.content
        #     message_placeholder.markdown(full_response + "▌")
        # 
        # current_conv["messages"]를 전달하여 현재 대화의 맥락만 LLM에 제공
        # 다른 대화의 메시지는 포함되지 않습니다 (세션 간 격리)
        
        # 스트리밍 완료 후 최종 응답 표시
        message_placeholder.markdown(full_response)
    
    # AI 응답을 현재 대화에 저장
    current_conv["messages"].append(AIMessage(content=full_response))
    
    # 페이지 새로고침하여 변경사항 반영
    st.rerun()


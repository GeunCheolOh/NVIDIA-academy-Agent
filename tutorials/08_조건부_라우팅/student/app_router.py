"""
app_router.py - Router 기반 다중 경로 채팅 애플리케이션
======================================================

목적:
    Router Agent를 사용하여 질문 유형에 따라
    VectorDB, WebSearch, Direct LLM 중 자동으로 선택하는
    지능형 채팅 애플리케이션

주요 기능:
    1. D2L 교재 기반 AI/ML 질문 답변
    2. 웹 검색을 통한 최신 정보 제공
    3. 일반 대화 및 추론
    4. 라우팅 과정 시각화
"""

import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os
from datetime import datetime
import uuid
from pathlib import Path

from rag_router_agent import RouterAgent

load_dotenv()

st.set_page_config(
    page_title="Router Agent Chat",
    page_icon="🧭",
    layout="wide"
)

# ============================================================================
# D2L 벡터 스토어 로드
# ============================================================================

@st.cache_resource
def load_d2l_vectorstore():
    """D2L 벡터 스토어를 로드합니다. (캐시됨)"""
    chroma_path = "./chroma_db_d2l"
    
    if not Path(chroma_path).exists():
        st.error("""
        ❌ D2L 벡터 스토어가 없습니다!
        
        먼저 다음 명령을 실행하세요:
        ```bash
        python setup_d2l.py
        ```
        """)
        st.stop()
    
    try:
        embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            api_key=os.getenv("OPENAI_API_KEY")
        )
        vectorstore = Chroma(
            persist_directory=chroma_path,
            embedding_function=embeddings
        )
        count = vectorstore._collection.count()
        return vectorstore, count
    except Exception as e:
        st.error(f"벡터 스토어 로드 실패: {str(e)}")
        st.stop()

# ============================================================================
# Session State 초기화
# ============================================================================

# D2L 벡터 스토어 로드
if "vectorstore_loaded" not in st.session_state:
    with st.spinner("D2L 교재 로딩 중..."):
        vectorstore, vector_count = load_d2l_vectorstore()
        st.session_state.vectorstore = vectorstore
        st.session_state.vector_count = vector_count
        st.session_state.vectorstore_loaded = True

# 대화 세션 관리
if "conversations" not in st.session_state:
    first_id = str(uuid.uuid4())
    st.session_state.conversations = {
        first_id: {
            "id": first_id,
            "title": "새 대화",
            "messages": [],
            "created_at": datetime.now()
        }
    }
    st.session_state.active_conversation_id = first_id

# YOUR CODE HERE - Router Agent 초기화
# if "router_agent" not in st.session_state:
#     retriever = st.session_state.vectorstore.as_retriever(
#         search_kwargs={"k": 3}
#     )
#     st.session_state.router_agent = RouterAgent(
#         d2l_retriever=retriever,
#         api_key=os.getenv("OPENAI_API_KEY"),
#         tavily_api_key=os.getenv("TAVILY_API_KEY")
#     )
# 
# RouterAgent 생성:
# - d2l_retriever: D2L 교재 검색기
# - api_key: OpenAI API 키
# - tavily_api_key: Tavily API 키 (웹 검색용)
pass  # 위의 YOUR CODE HERE를 채우면 이 줄을 삭제하세요

# ============================================================================
# 헬퍼 함수들
# ============================================================================

def create_new_conversation():
    """새로운 대화 세션 생성"""
    new_id = str(uuid.uuid4())
    st.session_state.conversations[new_id] = {
        "id": new_id,
        "title": "새 대화",
        "messages": [],
        "created_at": datetime.now()
    }
    st.session_state.active_conversation_id = new_id

def get_conversation_title(messages):
    """대화 제목 자동 생성"""
    if not messages:
        return "새 대화"
    
    first_user_msg = next(
        (msg.content for msg in messages if isinstance(msg, HumanMessage)), 
        None
    )
    
    if first_user_msg:
        return first_user_msg[:30] + "..." if len(first_user_msg) > 30 else first_user_msg
    return "새 대화"

def delete_conversation(conv_id):
    """대화 세션 삭제"""
    if len(st.session_state.conversations) > 1:
        del st.session_state.conversations[conv_id]
        
        if st.session_state.active_conversation_id == conv_id:
            st.session_state.active_conversation_id = list(
                st.session_state.conversations.keys()
            )[0]

# ============================================================================
# 현재 활성 대화
# ============================================================================
current_conv = st.session_state.conversations[st.session_state.active_conversation_id]

# ============================================================================
# 상단 헤더: 제목 + 새 대화 버튼
# ============================================================================
col1, col2 = st.columns([6, 1])

with col1:
    st.title("🧭 Router Agent Chat")
    st.caption(f"D2L 교재: {st.session_state.vector_count}개 벡터 | 3가지 경로: VectorDB, WebSearch, Direct LLM")

with col2:
    if st.button("➕ 새 대화", use_container_width=True):
        create_new_conversation()
        st.rerun()

st.divider()

# ============================================================================
# 사이드바: 대화 세션 목록
# ============================================================================
with st.sidebar:
    st.header("💬 대화 세션")
    
    # 대화 목록 (최신순)
    sorted_convs = sorted(
        st.session_state.conversations.values(),
        key=lambda x: x["created_at"],
        reverse=True
    )
    
    for conv in sorted_convs:
        is_active = conv["id"] == st.session_state.active_conversation_id
        
        col1, col2 = st.columns([4, 1])
        
        with col1:
            button_type = "primary" if is_active else "secondary"
            title = get_conversation_title(conv["messages"])
            
            if st.button(
                f"{'📌' if is_active else '💬'} {title}",
                key=f"conv_{conv['id']}",
                use_container_width=True,
                type=button_type
            ):
                st.session_state.active_conversation_id = conv["id"]
                st.rerun()
        
        with col2:
            if len(st.session_state.conversations) > 1:
                if st.button("🗑️", key=f"del_{conv['id']}", use_container_width=True):
                    delete_conversation(conv["id"])
                    st.rerun()
    
    st.divider()
    
    # 현재 대화 정보
    st.subheader("📊 현재 대화 정보")
    if current_conv["messages"]:
        total_messages = len([
            msg for msg in current_conv["messages"] 
            if isinstance(msg, (HumanMessage, AIMessage))
        ])
        st.write(f"총 메시지: {total_messages}")
        st.write(f"생성 시간: {current_conv['created_at'].strftime('%Y-%m-%d %H:%M')}")
    else:
        st.write("대화 히스토리가 없습니다.")
    
    st.divider()
    
    # Router 정보
    st.subheader("🧭 Router 정보")
    st.info("""
    **3가지 경로**:
    
    📚 **VectorDB**
    - AI/ML 기술 질문
    - D2L 교재 검색
    
    🌐 **WebSearch**
    - 최신 정보/뉴스
    - Tavily 검색
    
    💬 **Direct LLM**
    - 일반 대화/추론
    - LLM 직접 응답
    """)

# ============================================================================
# 메인 영역: 채팅 인터페이스
# ============================================================================

# 이전 메시지 표시
for i, message in enumerate(current_conv["messages"]):
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(message.content)
            
            # 라우팅 정보가 있으면 표시 (session_state에 저장된 경우)
            if f"route_info_{i}" in st.session_state:
                route_info = st.session_state[f"route_info_{i}"]
                with st.expander("🧭 라우팅 정보"):
                    col1, col2 = st.columns(2)
                    with col1:
                        route_emoji = {
                            "vectordb": "📚",
                            "websearch": "🌐",
                            "direct": "💬"
                        }
                        st.info(f"{route_emoji.get(route_info['route'], '❓')} **경로**: {route_info['route']}")
                    with col2:
                        st.caption(f"**이유**: {route_info['reason']}")
                    
                    if route_info.get('search_results'):
                        st.text_area(
                            "검색 결과",
                            route_info['search_results'][:500] + "...",
                            height=150,
                            disabled=True
                        )

# 새 메시지 입력
if prompt := st.chat_input("질문을 입력하세요..."):
    # 사용자 메시지 추가
    current_conv["messages"].append(HumanMessage(content=prompt))
    
    # 사용자 메시지 표시
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # AI 응답 생성
    with st.chat_message("assistant"):
        # 라우팅 과정 표시
        with st.status("🧭 경로 선택 및 답변 생성 중...", expanded=True) as status:
            # 대화 이력 전달
            chat_history = [
                msg for msg in current_conv["messages"][:-1]  # 방금 추가한 메시지 제외
                if isinstance(msg, (HumanMessage, AIMessage))
            ]
            
            # YOUR CODE HERE - Router Agent 호출
            # result = st.session_state.router_agent.invoke(
            #     question=prompt,
            #     chat_history=chat_history
            # )
            # 
            # Router Agent 실행:
            # - 질문 유형 분석
            # - 적절한 경로 선택
            # - 답변 생성
            result = {"route": "direct", "routing_reason": "테스트", "answer": "답변", "search_results": ""}  # 위의 YOUR CODE HERE를 채우면 이 줄을 삭제하세요
            
            # 라우팅 정보 표시
            route_emoji = {
                "vectordb": "📚 VectorDB",
                "websearch": "🌐 WebSearch",
                "direct": "💬 Direct LLM"
            }
            st.write(f"✅ 선택된 경로: {route_emoji.get(result['route'], result['route'])}")
            st.write(f"📝 이유: {result['routing_reason']}")
            
            if result['search_results']:
                st.write(f"🔍 검색 완료")
            
            status.update(label="✅ 답변 생성 완료!", state="complete")
        
        # 답변 표시
        answer = result["answer"]
        st.markdown(answer)
        
        # 라우팅 정보 표시
        with st.expander("🧭 라우팅 정보"):
            col1, col2 = st.columns(2)
            with col1:
                route_emoji_full = {
                    "vectordb": "📚",
                    "websearch": "🌐",
                    "direct": "💬"
                }
                st.info(f"{route_emoji_full.get(result['route'], '❓')} **경로**: {result['route']}")
            with col2:
                st.caption(f"**이유**: {result['routing_reason']}")
            
            if result['search_results']:
                st.text_area(
                    "검색 결과",
                    result['search_results'][:500] + "...",
                    height=150,
                    disabled=True
                )
    
    # AI 응답 및 라우팅 정보 저장
    current_conv["messages"].append(AIMessage(content=answer))
    message_idx = len(current_conv["messages"]) - 1
    st.session_state[f"route_info_{message_idx}"] = {
        "route": result["route"],
        "reason": result["routing_reason"],
        "search_results": result.get("search_results", "")
    }
    
    # 페이지 새로고침
    st.rerun()

# ============================================================================
# 하단 안내
# ============================================================================
if not current_conv["messages"]:
    st.info("""
    ### 🧭 Router Agent 사용 방법
    
    이 Agent는 질문 유형을 자동으로 분석하여 최적의 경로를 선택합니다.
    
    **예제 질문**:
    
    📚 **VectorDB 경로** (AI/ML 질문):
    - "딥러닝에서 backpropagation이란?"
    - "CNN의 구조를 설명해주세요"
    - "gradient descent와 SGD의 차이는?"
    
    🌐 **WebSearch 경로** (최신 정보):
    - "2024년 AI 관련 최신 뉴스는?"
    - "오늘 날씨 어때?"
    - "최근 노벨상 수상자는?"
    
    💬 **Direct LLM 경로** (일반 대화):
    - "안녕하세요!"
    - "Python으로 피보나치 수열 코드 작성해줘"
    - "시 한 편 써줘"
    
    #### 💡 팁
    - Router가 자동으로 최적의 경로를 선택합니다
    - 각 답변의 라우팅 정보를 확인할 수 있습니다
    - 여러 대화를 동시에 관리할 수 있습니다
    """)


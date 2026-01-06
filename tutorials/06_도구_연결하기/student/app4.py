"""
app4.py - 웹검색 통합 채팅 앱
==============================

목적:
    LangChain Tool(웹검색)을 실제 채팅 앱에 통합하여 RAG 패턴 구현
    
주요 기능:
    1. 웹검색 도구 통합 (Tavily, DuckDuckGo)
    2. RAG (Retrieval-Augmented Generation) 패턴
       - 사용자 질문으로 웹 검색
       - 검색 결과를 프롬프트에 포함
       - LLM이 검색 결과를 참고하여 답변 생성
    3. 검색 결과 저장 및 표시
    4. 시스템 프롬프트 설정
    5. 다중 대화 세션 관리
    
학습 포인트:
    - LangChain Tool 사용 (TavilySearchResults, DDGS)
    - SystemMessage를 통한 시스템 프롬프트 전달
    - RAG 패턴: 외부 정보 검색 + LLM 결합
    - 검색 결과를 대화별로 저장하는 데이터 구조
    - st.expander()를 사용한 검색 결과 접기/펼치기
    
이전 앱과의 차이점:
    - app2: 단순 대화 세션 관리
    - app4: 대화 + 웹검색 + RAG + 시스템 프롬프트
"""

import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_community.tools.tavily_search import TavilySearchResults  # Tavily 검색 도구
from ddgs import DDGS  # DuckDuckGo 검색 라이브러리
from dotenv import load_dotenv
import os
from datetime import datetime
import uuid

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
# Session State 초기화 - 검색 기능이 추가된 다중 세션 관리
# ============================================================================
# YOUR CODE HERE (1) - Session State에 conversations 초기화
# conversations 딕셔너리는 다음 필드를 포함해야 합니다:
# - id, title, messages, search_results (dict), system_prompt (str), created_at
# if "conversations" not in st.session_state:
#     first_id = str(uuid.uuid4())
#     st.session_state.conversations = {
#         first_id: {
#             "id": first_id,
#             "title": "새 대화",
#             "messages": [],
#             "search_results": {},  # 검색 결과 저장용
#             "system_prompt": "",   # 시스템 프롬프트
#             "created_at": datetime.now()
#         }
#     }
#     st.session_state.active_conversation_id = first_id
# 
# conversations 구조 (app2와 비교):
# app2: {"id", "title", "messages", "created_at"}
# app4: {"id", "title", "messages", "created_at", "search_results", "system_prompt"}
# 
# search_results 구조:
# {
#     0: "첫 번째 사용자 메시지의 검색 결과",
#     2: "세 번째 사용자 메시지의 검색 결과",
#     ...
# }
# 메시지 인덱스를 키로 사용하여 어떤 질문에 대한 검색인지 추적

# 현재 선택된 모델
if "selected_model" not in st.session_state:
    st.session_state.selected_model = "gpt-4.1-mini"

# YOUR CODE HERE (2) - Session State에 search_engine 초기화 (초기값: None)
# if "search_engine" not in st.session_state:
#     st.session_state.search_engine = None
# 
# search_engine: 현재 활성화된 검색 엔진
# - None: 검색 비활성화
# - "tavily": Tavily 검색 활성화
# - "duckduckgo": DuckDuckGo 검색 활성화

# ChatOpenAI LLM 인스턴스
if "llm" not in st.session_state:
    st.session_state.llm = ChatOpenAI(
        model=MODELS[st.session_state.selected_model],
        temperature=0.7,
        streaming=True,
        api_key=os.getenv("OPENAI_API_KEY")
    )

# ============================================================================
# 대화 관리 헬퍼 함수들 (app2와 동일)
# ============================================================================

def create_new_conversation():
    """
    새로운 대화 세션 생성
    검색 결과와 시스템 프롬프트 필드가 추가됨
    """
    new_id = str(uuid.uuid4())
    st.session_state.conversations[new_id] = {
        "id": new_id,
        "title": "새 대화",
        "messages": [],
        "search_results": {},  # 검색 결과 저장소
        "system_prompt": "",   # 대화별 시스템 프롬프트
        "created_at": datetime.now()
    }
    st.session_state.active_conversation_id = new_id

def get_conversation_title(messages):
    """대화 제목 자동 생성 (첫 번째 사용자 메시지 사용)"""
    if not messages:
        return "새 대화"
    first_user_msg = next((msg.content for msg in messages if isinstance(msg, HumanMessage)), None)
    if first_user_msg:
        return first_user_msg[:30] + "..." if len(first_user_msg) > 30 else first_user_msg
    return "새 대화"

def delete_conversation(conv_id):
    """대화 세션 삭제 (최소 1개 유지)"""
    if len(st.session_state.conversations) > 1:
        del st.session_state.conversations[conv_id]
        if st.session_state.active_conversation_id == conv_id:
            st.session_state.active_conversation_id = list(st.session_state.conversations.keys())[0]

# ============================================================================
# 웹검색 도구 함수들
# ============================================================================

def search_tavily(query):
    """
    Tavily 검색 API를 사용한 웹 검색
    
    Args:
        query: 검색 쿼리
        
    Returns:
        (formatted_results, error): 
        - 성공 시: (검색 결과 문자열, None)
        - 실패 시: (None, 에러 메시지)
    
    Tavily의 특징:
        - LLM을 위해 최적화된 검색 API
        - 높은 품질의 결과
        - API 키 필요 (유료)
    """
    try:
        # API 키 확인
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            return None, "❌ Tavily API 키가 설정되지 않았습니다. .env 파일에 TAVILY_API_KEY를 추가하세요."
        
        # YOUR CODE HERE (3) - TavilySearchResults 초기화 및 검색 수행
        # search_tool = TavilySearchResults(
        #     max_results=5,
        #     api_key=api_key
        # )
        # results = search_tool.invoke(query)
        # 
        # TavilySearchResults: LangChain의 Tavily 검색 도구
        # - max_results: 최대 검색 결과 개수
        # - invoke(): 검색 수행 (결과는 딕셔너리 리스트)
        
        results = []  # 위의 YOUR CODE HERE를 채우면 이 줄을 삭제하세요
        
        # 검색 결과를 마크다운 형식으로 포맷팅
        formatted_results = "### 🔍 Tavily 검색 결과:\n\n"
        for i, result in enumerate(results, 1):
            formatted_results += f"**{i}. {result.get('title', 'No title')}**\n"
            formatted_results += f"{result.get('content', result.get('snippet', 'No content'))}\n"
            formatted_results += f"🔗 {result.get('url', '')}\n\n"
        
        return formatted_results, None
    except Exception as e:
        return None, f"❌ Tavily 검색 오류: {str(e)}"

def search_duckduckgo(query):
    """
    DuckDuckGo를 사용한 웹 검색
    
    Args:
        query: 검색 쿼리
        
    Returns:
        (formatted_results, error):
        - 성공 시: (검색 결과 문자열, None)
        - 실패 시: (None, 에러 메시지)
    
    DuckDuckGo의 특징:
        - 무료
        - API 키 불필요
        - 속도가 빠름
        - 결과 품질은 Tavily보다 낮을 수 있음
    """
    try:
        # YOUR CODE HERE (4) - DDGS 객체 생성 및 검색 수행
        # ddgs = DDGS()
        # results = list(ddgs.text(query, max_results=5))
        # 
        # DDGS: DuckDuckGo Search 라이브러리
        # - text(): 텍스트 검색 수행
        # - max_results: 최대 결과 개수
        # 
        # 주의: ddgs.text()는 제너레이터를 반환하므로 list()로 변환
        
        results = []  # 위의 YOUR CODE HERE를 채우면 이 줄을 삭제하세요
        
        # 검색 결과 포맷팅
        formatted_results = "### 🔍 DuckDuckGo 검색 결과:\n\n"
        
        if results:
            for i, result in enumerate(results, 1):
                formatted_results += f"**{i}. {result.get('title', 'No title')}**\n"
                formatted_results += f"{result.get('body', 'No description')}\n"
                formatted_results += f"🔗 {result.get('href', '')}\n\n"
        else:
            formatted_results += "검색 결과가 없습니다.\n"
        
        return formatted_results, None
    except Exception as e:
        return None, f"❌ DuckDuckGo 검색 오류: {str(e)}"

# ============================================================================
# 현재 활성 대화 가져오기
# ============================================================================
current_conv = st.session_state.conversations[st.session_state.active_conversation_id]

# ============================================================================
# 상단 헤더: 제목 + 새 대화 버튼
# ============================================================================
col1, col2 = st.columns([6, 1])
with col1:
    st.title("💬 LangChain Chat")
with col2:
    if st.button("➕ 새 대화", use_container_width=True):
        create_new_conversation()
        st.rerun()

# ============================================================================
# 사이드바: 설정 및 대화 관리
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
    # 시스템 프롬프트 설정
    # ------------------------------------------------------------------------
    st.subheader("시스템 프롬프트")
    
    # 시스템 프롬프트 필드가 없으면 초기화
    if "system_prompt" not in current_conv:
        current_conv["system_prompt"] = ""
    
    # 여러 줄 텍스트 입력창
    system_prompt = st.text_area(
        "시스템 프롬프트 설정",
        value=current_conv.get("system_prompt", ""),
        height=150,
        placeholder="예: 당신은 친절한 AI 어시스턴트입니다. 항상 한국어로 답변하세요.",
        help="AI의 역할과 답변 스타일을 정의합니다. 비워두면 기본 동작을 사용합니다."
    )
    
    # 시스템 프롬프트 변경 감지 및 저장
    if system_prompt != current_conv.get("system_prompt", ""):
        current_conv["system_prompt"] = system_prompt
        if system_prompt:
            st.success("시스템 프롬프트가 적용되었습니다.")
        else:
            st.info("시스템 프롬프트가 비활성화되었습니다.")
    
    # 활성 상태 표시
    if current_conv.get("system_prompt"):
        st.caption(f"✓ 시스템 프롬프트 활성화 ({len(current_conv['system_prompt'])}자)")
    
    st.divider()
    
    # ------------------------------------------------------------------------
    # 대화 세션 목록
    # ------------------------------------------------------------------------
    st.subheader("대화 세션")
    
    # 최신순으로 정렬
    sorted_convs = sorted(
        st.session_state.conversations.values(),
        key=lambda x: x["created_at"],
        reverse=True
    )
    
    # 각 대화를 버튼으로 표시
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
    
    # ------------------------------------------------------------------------
    # 현재 대화 정보
    # ------------------------------------------------------------------------
    st.subheader("현재 대화 정보")
    if current_conv["messages"]:
        total_messages = len([msg for msg in current_conv["messages"] if isinstance(msg, (HumanMessage, AIMessage))])
        st.write(f"총 메시지 수: {total_messages}")
        st.write(f"생성 시간: {current_conv['created_at'].strftime('%Y-%m-%d %H:%M')}")
        
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
# 이전 메시지 표시 (검색 결과 포함)
# ----------------------------------------------------------------------------
for idx, message in enumerate(current_conv["messages"]):
    if isinstance(message, HumanMessage):
        # 사용자 메시지 표시
        with st.chat_message("user"):
            st.markdown(message.content)
        
        # YOUR CODE HERE (5) - 검색 결과가 있으면 expander로 표시
        # if idx in current_conv.get("search_results", {}):
        #     with st.expander("🔍 검색 결과 보기", expanded=False):
        #         st.markdown(current_conv["search_results"][idx])
        # 
        # expander: 접을 수 있는 섹션 생성
        # - expanded=False: 기본적으로 접힌 상태
        # - 사용자가 클릭하면 검색 결과 표시
        # 
        # 검색 결과는 메시지 인덱스를 키로 저장되어 있음
        # 예: search_results[0] = "첫 번째 질문의 검색 결과"
        
    elif isinstance(message, AIMessage):
        # AI 응답 표시
        with st.chat_message("assistant"):
            st.markdown(message.content)

# ----------------------------------------------------------------------------
# 검색 엔진 선택 버튼
# ----------------------------------------------------------------------------
col1, col2, col3 = st.columns([1, 1, 6])

with col1:
    # Tavily 버튼 (토글 방식)
    tavily_enabled = st.button(
        "🌐 Tavily", 
        use_container_width=True, 
        type="primary" if st.session_state.search_engine == "tavily" else "secondary"
    )
    # YOUR CODE HERE (6) - Tavily 버튼 클릭 시 search_engine 토글
    # if tavily_enabled:
    #     st.session_state.search_engine = "tavily" if st.session_state.search_engine != "tavily" else None
    # 
    # 토글 로직:
    # - 현재 "tavily"가 아니면 → "tavily"로 설정
    # - 현재 "tavily"이면 → None으로 설정 (비활성화)

with col2:
    # DuckDuckGo 버튼 (토글 방식)
    duckduckgo_enabled = st.button(
        "🦆 DuckDuckGo", 
        use_container_width=True,
        type="primary" if st.session_state.search_engine == "duckduckgo" else "secondary"
    )
    # YOUR CODE HERE (7) - DuckDuckGo 버튼 클릭 시 search_engine 토글
    # if duckduckgo_enabled:
    #     st.session_state.search_engine = "duckduckgo" if st.session_state.search_engine != "duckduckgo" else None

# 검색 엔진 활성화 상태 표시
if st.session_state.search_engine:
    st.info(f"✓ {st.session_state.search_engine.capitalize()} 검색이 활성화되었습니다.")

# ============================================================================
# 사용자 입력 처리 및 RAG 패턴
# ============================================================================
if prompt := st.chat_input("메시지를 입력하세요..."):
    """
    RAG (Retrieval-Augmented Generation) 워크플로우:
    1. 사용자 질문 입력
    2. 웹 검색 수행 (선택적)
    3. 검색 결과를 프롬프트에 포함
    4. LLM이 검색 결과를 참고하여 답변 생성
    5. 검색 결과와 답변 저장
    """
    search_results = None
    search_error = None
    
    # ------------------------------------------------------------------------
    # 1단계: 웹 검색 수행 (검색 엔진이 활성화된 경우)
    # ------------------------------------------------------------------------
    if st.session_state.search_engine == "tavily":
        # Tavily 검색
        with st.spinner("Tavily로 검색 중..."):
            search_results, search_error = search_tavily(prompt)
    elif st.session_state.search_engine == "duckduckgo":
        # DuckDuckGo 검색
        with st.spinner("DuckDuckGo로 검색 중..."):
            search_results, search_error = search_duckduckgo(prompt)
    
    # ------------------------------------------------------------------------
    # 2단계: 사용자 메시지 저장 및 표시
    # ------------------------------------------------------------------------
    current_conv["messages"].append(HumanMessage(content=prompt))
    user_msg_idx = len(current_conv["messages"]) - 1  # 현재 메시지의 인덱스
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # ------------------------------------------------------------------------
    # 3단계: 검색 결과 처리 및 프롬프트 증강
    # ------------------------------------------------------------------------
    if search_error:
        # 검색 실패: 에러 표시하고 일반 대화 진행
        st.error(search_error)
        messages_with_search = current_conv["messages"].copy()
        
    elif search_results:
        # 검색 성공: RAG 패턴 적용
        
        # YOUR CODE HERE (8) - 검색 결과를 current_conv["search_results"]에 저장
        # current_conv["search_results"][user_msg_idx] = search_results
        # 
        # 검색 결과를 메시지 인덱스와 함께 저장
        # 나중에 이 메시지를 다시 표시할 때 검색 결과도 함께 표시됨
        
        # 검색 결과를 expander로 표시
        with st.expander("🔍 검색 결과 보기", expanded=False):
            st.markdown(search_results)
        
        # YOUR CODE HERE (9) - 검색 결과를 프롬프트에 포함
        # augmented_prompt = f"{prompt}\n\n{search_results}\n\n위 검색 결과를 참고하여 답변해주세요."
        # messages_with_search = current_conv["messages"][:-1] + [HumanMessage(content=augmented_prompt)]
        # 
        # RAG의 핵심: 원래 프롬프트 + 검색 결과를 결합
        # - 마지막 메시지(사용자 질문)를 증강된 프롬프트로 교체
        # - LLM은 검색 결과를 참고하여 더 정확한 답변 생성
        # 
        # 주의: messages에는 원래 프롬프트가 저장되어 있고,
        #      LLM에는 증강된 프롬프트가 전달됨 (UI와 맥락 분리)
        
        messages_with_search = current_conv["messages"].copy()  # 위의 YOUR CODE HERE를 채우면 이 줄을 삭제하세요
    else:
        # 검색 비활성화: 일반 대화
        messages_with_search = current_conv["messages"].copy()
    
    # ------------------------------------------------------------------------
    # 4단계: 시스템 프롬프트 추가
    # ------------------------------------------------------------------------
    # YOUR CODE HERE (10) - 시스템 프롬프트가 있으면 SystemMessage로 추가
    # if current_conv.get("system_prompt"):
    #     messages_with_system = [SystemMessage(content=current_conv["system_prompt"])] + messages_with_search
    # else:
    #     messages_with_system = messages_with_search
    # 
    # SystemMessage: AI의 역할과 동작을 정의하는 메시지
    # - 메시지 리스트의 맨 앞에 추가
    # - LLM이 이 지시사항을 따라 답변 생성
    # 
    # 예: "당신은 전문 개발자입니다." → 개발자 관점에서 답변
    
    messages_with_system = messages_with_search  # 위의 YOUR CODE HERE를 채우면 이 줄을 삭제하세요
    
    # ------------------------------------------------------------------------
    # 5단계: AI 응답 생성 (스트리밍)
    # ------------------------------------------------------------------------
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # LLM에 전달되는 최종 메시지 구조:
        # [SystemMessage(시스템 프롬프트), HumanMessage(증강된 프롬프트), ...]
        for chunk in st.session_state.llm.stream(messages_with_system):
            full_response += chunk.content
            message_placeholder.markdown(full_response + "▌")
        
        message_placeholder.markdown(full_response)
    
    # ------------------------------------------------------------------------
    # 6단계: AI 응답 저장
    # ------------------------------------------------------------------------
    current_conv["messages"].append(AIMessage(content=full_response))
    st.rerun()


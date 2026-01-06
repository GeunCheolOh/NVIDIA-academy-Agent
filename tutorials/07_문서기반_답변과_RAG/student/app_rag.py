"""
app_rag.py - PDF 기반 RAG 채팅 애플리케이션
===========================================

목적:
    PDF 문서를 업로드하고, 문서 내용을 기반으로 대화할 수 있는
    다중 세션 RAG 채팅 애플리케이션

주요 기능:
    1. PDF 파일 업로드 및 실시간 처리 진행 상황 표시
    2. 여러 대화 세션 관리 (app2.py 기반)
    3. LangGraph 기반 RAG Agent 통합
    4. 문서 기반 질의응답

사용 기술:
    - Streamlit: 웹 인터페이스
    - rag_processor.py: PDF 전처리
    - rag_agent.py: LangGraph RAG Agent
"""

import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv
import os
from datetime import datetime
import uuid

from rag_processor import RAGProcessor
from rag_agent import RAGAgent

load_dotenv()

st.set_page_config(
    page_title="RAG Chat - 문서 기반 대화",
    page_icon="📚",
    layout="wide"
)

# ============================================================================
# Session State 초기화
# ============================================================================

# 대화 세션 관리 (app2.py와 동일)
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

# RAG 관련 상태
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if "rag_agent" not in st.session_state:
    st.session_state.rag_agent = None

if "processor" not in st.session_state:
    st.session_state.processor = None

if "pdf_processed" not in st.session_state:
    st.session_state.pdf_processed = False

if "current_pdf_name" not in st.session_state:
    st.session_state.current_pdf_name = None

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

def process_pdf(uploaded_file):
    """
    업로드된 PDF 파일을 처리합니다.
    
    Args:
        uploaded_file: Streamlit의 UploadedFile 객체
        
    Returns:
        성공 여부 (bool)
    """
    # YOUR CODE HERE - RAGProcessor 초기화
    # if st.session_state.processor is None:
    #     st.session_state.processor = RAGProcessor(
    #         api_key=os.getenv("OPENAI_API_KEY")
    #     )
    # 
    # RAGProcessor: PDF 파일을 벡터 스토어로 변환하는 클래스
    # session_state에 저장하여 재사용
    pass  # 위의 YOUR CODE HERE를 채우면 이 줄을 삭제하세요
    
    # YOUR CODE HERE - st.status로 진행 상황 표시
    # with st.status("PDF 처리 중...", expanded=True) as status:
    #     # PDF 처리
    #     vectorstore, progress = st.session_state.processor.process_pdf_file(
    #         uploaded_file
    #     )
    # 
    # st.status(): 진행 상황을 접을 수 있는 컨테이너로 표시
    # expanded=True: 기본적으로 열린 상태로 표시
    status = None  # 위의 YOUR CODE HERE를 채우면 이 줄을 삭제하세요
    vectorstore = None  # 위의 YOUR CODE HERE를 채우면 이 줄을 삭제하세요
    progress = {"status": "실패", "steps": {}}  # 위의 YOUR CODE HERE를 채우면 이 줄을 삭제하세요
    
    if status:  # YOUR CODE HERE를 채우면 자동으로 활성화됨
        
        # 단계별 진행 상황 표시
        if "load" in progress["steps"]:
            st.write(progress["steps"]["load"]["message"])
        
        if "chunk" in progress["steps"]:
            st.write(progress["steps"]["chunk"]["message"])
        
        if "embed" in progress["steps"]:
            st.write(progress["steps"]["embed"]["message"])
        
        # 처리 결과 확인
        if progress["status"] == "완료":
            status.update(
                label="✅ PDF 처리 완료!",
                state="complete"
            )
            
            # 벡터 스토어 및 Agent 설정
            st.session_state.vectorstore = vectorstore
            st.session_state.pdf_processed = True
            st.session_state.current_pdf_name = uploaded_file.name
            
            # YOUR CODE HERE - RAG Agent 초기화
            # retriever = st.session_state.processor.get_retriever(vectorstore, k=5)
            # st.session_state.rag_agent = RAGAgent(
            #     retriever=retriever,
            #     api_key=os.getenv("OPENAI_API_KEY"),
            #     max_iterations=3
            # )
            # 
            # retriever: 벡터 스토어에서 검색하는 객체 (k=5: 상위 5개 문서)
            # RAGAgent: LangGraph 기반 ReAct 패턴 Agent
            # max_iterations: 검색 결과가 부족할 때 최대 3회 재시도
            pass  # 위의 YOUR CODE HERE를 채우면 이 줄을 삭제하세요
            
            return True
        else:
            status.update(
                label="❌ PDF 처리 실패",
                state="error"
            )
            
            if "error" in progress["steps"]:
                st.error(progress["steps"]["error"]["message"])
            
            return False

# ============================================================================
# 현재 활성 대화
# ============================================================================
current_conv = st.session_state.conversations[st.session_state.active_conversation_id]

# ============================================================================
# 상단 헤더: 제목 + 새 대화 버튼
# ============================================================================
col1, col2 = st.columns([6, 1])

with col1:
    st.title("📚 RAG Chat - 문서 기반 대화")

with col2:
    if st.button("➕ 새 대화", use_container_width=True):
        create_new_conversation()
        st.rerun()

# ============================================================================
# PDF 업로드 섹션
# ============================================================================
st.divider()

with st.container():
    st.subheader("📄 PDF 문서 업로드")
    
    col_upload, col_status = st.columns([2, 1])
    
    with col_upload:
        uploaded_file = st.file_uploader(
            "PDF 파일을 선택하세요",
            type=["pdf"],
            help="업로드된 PDF 문서의 내용을 기반으로 대화할 수 있습니다."
        )
        
        if uploaded_file is not None:
            # 파일 정보 표시
            file_size_mb = uploaded_file.size / (1024 * 1024)
            st.caption(f"📎 {uploaded_file.name} ({file_size_mb:.2f} MB)")
            
            # 처리 버튼
            if st.button("🚀 문서 처리 시작", type="primary"):
                success = process_pdf(uploaded_file)
                
                if success:
                    st.success("문서 처리가 완료되었습니다! 이제 대화를 시작하세요.")
                    st.rerun()
    
    with col_status:
        if st.session_state.pdf_processed:
            st.success("✅ 문서 준비 완료")
            st.info(f"📄 {st.session_state.current_pdf_name}")
            
            # 벡터 스토어 정보
            if st.session_state.vectorstore:
                count = st.session_state.vectorstore._collection.count()
                st.caption(f"벡터: {count}개")
        else:
            st.warning("⚠️ 문서 미등록")
            st.caption("PDF를 업로드하고 처리해주세요.")

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
        
        with st.expander("전체 히스토리"):
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

# 이전 메시지 표시
for message in current_conv["messages"]:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(message.content)

# 새 메시지 입력
if prompt := st.chat_input("문서에 대해 질문하세요..."):
    # PDF가 처리되지 않은 경우 경고
    if not st.session_state.pdf_processed:
        st.warning("⚠️ 먼저 PDF 문서를 업로드하고 처리해주세요.")
        st.stop()
    
    # 사용자 메시지 추가
    current_conv["messages"].append(HumanMessage(content=prompt))
    
    # 사용자 메시지 표시
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # AI 응답 생성
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # RAG Agent 실행
        with st.spinner("문서를 검색하고 답변을 생성하는 중..."):
            # 대화 이력 전달 (현재 대화만)
            chat_history = [
                msg for msg in current_conv["messages"][:-1]  # 방금 추가한 메시지 제외
                if isinstance(msg, (HumanMessage, AIMessage))
            ]
            
            # YOUR CODE HERE - RAG Agent 호출
            # result = st.session_state.rag_agent.invoke(
            #     question=prompt,
            #     chat_history=chat_history
            # )
            # 
            # answer = result["answer"]
            # iterations = result["iterations"]
            # 
            # rag_agent.invoke(): 질문과 대화 이력을 전달하여 답변 생성
            # 반환값: {"answer": 답변, "search_results": 검색결과, "iterations": 반복횟수}
            answer = "답변 생성 실패"  # 위의 YOUR CODE HERE를 채우면 이 줄을 삭제하세요
            iterations = 0  # 위의 YOUR CODE HERE를 채우면 이 줄을 삭제하세요
            result = {"search_results": ""}  # 위의 YOUR CODE HERE를 채우면 이 줄을 삭제하세요
        
        # 답변 표시
        message_placeholder.markdown(answer)
        
        # 검색 정보 표시 (접을 수 있는 영역)
        with st.expander("🔍 검색 정보"):
            st.caption(f"반복 횟수: {iterations}")
            if result["search_results"]:
                st.text_area(
                    "검색된 문서",
                    result["search_results"][:1000] + "...",
                    height=200,
                    disabled=True
                )
    
    # AI 응답을 대화에 저장
    current_conv["messages"].append(AIMessage(content=answer))
    
    # 페이지 새로고침
    st.rerun()

# ============================================================================
# 하단 안내
# ============================================================================
if not st.session_state.pdf_processed:
    st.info("""
    ### 📖 사용 방법
    
    1. **PDF 업로드**: 상단에서 PDF 문서를 선택하세요
    2. **문서 처리**: "문서 처리 시작" 버튼을 클릭하세요
    3. **대화 시작**: 문서 내용에 대해 자유롭게 질문하세요
    
    #### 💡 팁
    - 여러 대화를 동시에 관리할 수 있습니다
    - 각 대화는 독립적인 히스토리를 유지합니다
    - LangGraph 기반 RAG Agent가 문서를 지능적으로 검색합니다
    """)


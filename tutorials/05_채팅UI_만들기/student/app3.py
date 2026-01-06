"""
app3.py - 응답 편집 기능 채팅 앱
================================

목적:
    AI의 응답을 사용자가 검증하고 수정할 수 있는 대화형 편집 기능 구현
    
주요 기능:
    1. 4단계 stage 관리를 통한 워크플로우 제어
       - user: 사용자 입력 단계
       - validate: AI 응답 검증 단계 (수락/수정/재작성 선택)
       - correct: 문장별 수정 단계
       - rewrite: 전체 재작성 단계
    2. AI 응답을 임시로 보류(pending) 후 사용자 승인
    3. 문장 단위 편집 기능
    4. 전체 텍스트 재작성 기능
    
학습 포인트:
    - 복잡한 UI 상태 관리 (stage 패턴)
    - 조건부 렌더링 (stage별 다른 UI)
    - 텍스트 처리 및 검증
    - st.text_input(), st.text_area()를 사용한 편집 UI
    - pending 패턴: 데이터를 임시 저장 후 확정
    
app1.py와의 차이점:
    - app1: 응답 즉시 저장
    - app3: 응답을 pending에 보류 → 검증/수정 → 최종 저장
"""

import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(page_title="LangChain Chat", page_icon="💬", layout="wide")

st.title("💬 LangChain Chat")

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
# Session State 초기화 - 응답 편집 워크플로우
# ============================================================================
# 대화 이력
if "messages" not in st.session_state:
    st.session_state.messages = []

# 현재 선택된 모델
if "selected_model" not in st.session_state:
    st.session_state.selected_model = "gpt-4.1-mini"

# YOUR CODE HERE - Session State에 "stage" 초기화 (초기값: "user")
# if "stage" not in st.session_state:
#     st.session_state.stage = "user"
# 
# stage: 현재 워크플로우의 단계를 나타냅니다
# - "user": 사용자가 메시지를 입력하는 단계 (기본)
# - "validate": AI 응답을 검증하는 단계 (수락/수정/재작성 선택)
# - "correct": 문장별로 수정하는 단계
# - "rewrite": 전체 응답을 재작성하는 단계

# YOUR CODE HERE - Session State에 "pending" 초기화 (초기값: None)
# if "pending" not in st.session_state:
#     st.session_state.pending = None
# 
# pending: AI의 응답을 임시로 보관하는 변수
# - user 단계에서 AI 응답을 받으면 pending에 저장
# - validate/correct/rewrite 단계에서 수정
# - 최종 승인 시 messages에 추가

# validation: 문장별 수정 시 사용하는 데이터
# {"sentences": [...], "valid": [...]}
if "validation" not in st.session_state:
    st.session_state.validation = {}

# ChatOpenAI LLM 인스턴스
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

def validate_response(response):
    """
    AI 응답을 문장 단위로 분리하는 함수
    
    Args:
        response: AI의 전체 응답 텍스트
        
    Returns:
        response_sentences: 문장들의 리스트
        validation_list: 각 문장의 검증 상태 (True = 수정 완료, False = 수정 필요)
    """
    # 마침표(.)를 기준으로 문장 분리
    response_sentences = response.split(". ")
    
    # 각 문장 정리 (앞뒤 공백 제거, 마침표 추가)
    response_sentences = [
        sentence.strip(". ") + "." for sentence in response_sentences 
        if sentence.strip(". ") != ""  # 빈 문장 제외
    ]
    
    # 모든 문장을 "수정 필요(False)" 상태로 초기화
    validation_list = [True] * len(response_sentences)
    
    return response_sentences, validation_list

def add_highlights(response_sentences, validation_list, bg="red", text="red"):
    """
    수정이 필요한 문장에 하이라이트를 추가하는 함수
    
    Args:
        response_sentences: 문장 리스트
        validation_list: 각 문장의 검증 상태
        bg: 배경색
        text: 텍스트 색
        
    Returns:
        하이라이트가 적용된 문장 리스트
    """
    return [
        f":{text}[:{bg}-background[{sentence}]]" if not is_valid else sentence
        for sentence, is_valid in zip(response_sentences, validation_list)
    ]

# ============================================================================
# 사이드바: 설정 패널
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
    # 대화 히스토리 초기화
    # ------------------------------------------------------------------------
    if st.button("대화 히스토리 초기화"):
        # 모든 상태 변수 초기화
        st.session_state.messages = []
        st.session_state.stage = "user"  # 기본 단계로 복귀
        st.session_state.pending = None  # 보류 중인 응답 제거
        st.session_state.validation = {}  # 검증 데이터 제거
        st.rerun()
    
    st.divider()
    
    # ------------------------------------------------------------------------
    # 대화 히스토리 요약
    # ------------------------------------------------------------------------
    st.subheader("대화 히스토리")
    if st.session_state.messages:
        total_messages = len([msg for msg in st.session_state.messages if isinstance(msg, (HumanMessage, AIMessage))])
        st.write(f"총 메시지 수: {total_messages}")
        
        with st.expander("전체 히스토리 보기"):
            for idx, msg in enumerate(st.session_state.messages):
                if isinstance(msg, HumanMessage):
                    st.markdown(f"**사용자 [{idx+1}]:** {msg.content}")
                elif isinstance(msg, AIMessage):
                    st.markdown(f"**AI [{idx+1}]:** {msg.content}")
    else:
        st.write("대화 히스토리가 없습니다.")

# ============================================================================
# 메인 영역: 채팅 인터페이스 (Stage별 조건부 렌더링)
# ============================================================================

# ----------------------------------------------------------------------------
# 확정된 메시지 표시
# ----------------------------------------------------------------------------
# messages에 저장된 메시지만 표시 (pending은 제외)
for message in st.session_state.messages:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(message.content)

# ============================================================================
# Stage 1: "user" - 사용자 입력 단계
# ============================================================================
# YOUR CODE HERE - stage가 "user"일 때의 처리
# if st.session_state.stage == "user":
# 
# "user" 단계: 일반적인 채팅 입력 모드
# - 사용자가 메시지를 입력하면 AI가 응답 생성
# - 응답을 messages에 바로 추가하지 않고 pending에 보류
# - stage를 "validate"로 변경하여 검증 단계로 이동

if False:  # 위의 YOUR CODE HERE를 채우면 이 줄을 삭제하세요
    if prompt := st.chat_input("메시지를 입력하세요..."):
        # 사용자 메시지는 즉시 messages에 추가
        st.session_state.messages.append(HumanMessage(content=prompt))
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # AI 응답 생성 (스트리밍)
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            for chunk in st.session_state.llm.stream(st.session_state.messages):
                full_response += chunk.content
                message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
        
        # YOUR CODE HERE - pending에 응답 저장하고 stage를 "validate"로 변경
        # st.session_state.pending = full_response
        # st.session_state.stage = "validate"
        # 
        # 중요: AI 응답을 messages에 추가하지 않음!
        # pending에만 보관하고 사용자의 승인을 기다림
        st.rerun()

# ============================================================================
# Stage 2: "validate" - 응답 검증 단계
# ============================================================================
elif st.session_state.stage == "validate":
    """
    "validate" 단계: AI 응답에 대한 사용자의 선택을 받는 단계
    - 입력창을 비활성화하여 새 메시지 입력 방지
    - pending의 응답을 표시하고 3가지 선택지 제공:
      1. 문장별 수정: 각 문장을 하나씩 검토하고 수정
      2. 수락: 응답을 그대로 messages에 추가
      3. 전체 재작성: 전체 텍스트를 직접 수정
    """
    # 입력창 비활성화 (새 메시지 입력 방지)
    st.chat_input("응답을 수락, 수정, 또는 재작성하세요.", disabled=True)
    
    # 응답을 문장 단위로 분리
    response_sentences, validation_list = validate_response(st.session_state.pending)
    
    with st.chat_message("assistant"):
        # pending 응답 표시
        st.markdown(st.session_state.pending)
        st.divider()
        
        # YOUR CODE HERE - st.columns(3)을 사용하여 3개의 버튼 배치
        # cols = st.columns(3)
        # 
        # 3개의 버튼을 가로로 나란히 배치
        
        cols = [None, None, None]  # 위의 YOUR CODE HERE를 채우면 이 줄을 삭제하세요
        
        if cols[0]:  # YOUR CODE HERE를 채우면 자동으로 활성화됨
            # 버튼 1: 문장별 수정
            if cols[0].button("문장별 수정", type="secondary"):
                # validation 데이터 초기화
                st.session_state.validation = {
                    "sentences": response_sentences,
                    "valid": validation_list,
                }
                st.session_state.stage = "correct"  # correct 단계로 이동
                st.rerun()
            
            # YOUR CODE HERE - "수락" 버튼 (클릭 시 pending을 messages에 추가하고 stage를 "user"로)
            # if cols[1].button("수락", type="primary"):
            #     st.session_state.messages.append(
            #         AIMessage(content=st.session_state.pending)
            #     )
            #     st.session_state.pending = None
            #     st.session_state.validation = {}
            #     st.session_state.stage = "user"
            #     st.rerun()
            # 
            # 버튼 2: 수락
            # - pending 응답을 messages에 최종 추가
            # - 모든 임시 데이터 정리 (pending, validation)
            # - stage를 "user"로 되돌려 다음 메시지 입력 가능하게 함
            
            # 버튼 3: 전체 재작성
            if cols[2].button("전체 재작성", type="secondary"):
                st.session_state.stage = "rewrite"  # rewrite 단계로 이동
                st.rerun()

# ============================================================================
# Stage 3: "correct" - 문장별 수정 단계
# ============================================================================
elif st.session_state.stage == "correct":
    """
    "correct" 단계: 응답을 문장 단위로 검토하고 수정하는 단계
    - 수정되지 않은 첫 번째 문장에 포커스
    - 해당 문장을 하이라이트 표시
    - 수정/삭제/건너뛰기 선택 가능
    - 모든 문장이 검토되면 수락 버튼 표시
    """
    st.chat_input("응답을 수락, 수정, 또는 재작성하세요.", disabled=True)
    
    # validation 데이터에서 문장 정보 가져오기
    response_sentences = st.session_state.validation["sentences"]
    validation_list = st.session_state.validation["valid"]
    
    # 아직 검토하지 않은 첫 번째 문장 찾기
    if not all(validation_list):
        focus = validation_list.index(False)  # False인 첫 번째 인덱스
    else:
        focus = None  # 모든 문장 검토 완료
    
    with st.chat_message("assistant"):
        # 모든 문장 표시 (포커스 문장은 하이라이트)
        for idx, sentence in enumerate(response_sentences):
            if idx == focus:
                # 현재 포커스 문장: 빨간 배경으로 강조
                st.markdown(f":red[:red-background[{sentence}]]")
            else:
                # 다른 문장: 일반 표시
                st.markdown(sentence)
        
        st.divider()
        
        # ------------------------------------------------------------------------
        # 케이스 1: 수정할 문장이 있는 경우
        # ------------------------------------------------------------------------
        if focus is not None:
            st.write(f"문장 {focus + 1} 수정:")
            
            # 텍스트 입력창 (현재 문장 내용이 기본값)
            new_sentence = st.text_input(
                "수정할 텍스트:",
                value=response_sentences[focus],
                key=f"edit_{focus}"
            )
            
            cols = st.columns(3)
            
            # 버튼 1: 업데이트 (수정 내용 적용)
            if cols[0].button(
                "업데이트",
                type="primary",
                disabled=len(new_sentence.strip()) < 1  # 빈 문장 방지
            ):
                # 수정된 문장으로 교체
                st.session_state.validation["sentences"][focus] = (
                    new_sentence.strip(". ") + "."
                )
                # 이 문장을 검토 완료로 표시
                st.session_state.validation["valid"][focus] = True
                # pending 업데이트 (모든 문장 결합)
                st.session_state.pending = " ".join(
                    st.session_state.validation["sentences"]
                )
                st.rerun()
            
            # 버튼 2: 삭제 (문장 제거)
            if cols[1].button("삭제"):
                st.session_state.validation["sentences"].pop(focus)
                st.session_state.validation["valid"].pop(focus)
                if len(st.session_state.validation["sentences"]) > 0:
                    # pending 업데이트
                    st.session_state.pending = " ".join(
                        st.session_state.validation["sentences"]
                    )
                    st.rerun()
                else:
                    st.warning("마지막 문장입니다. 전체 재작성을 사용하세요.")
            
            # 버튼 3: 다음 문장 (수정 없이 건너뛰기)
            if cols[2].button("다음 문장"):
                st.session_state.validation["valid"][focus] = True
                st.rerun()
        
        # ------------------------------------------------------------------------
        # 케이스 2: 모든 문장 검토 완료
        # ------------------------------------------------------------------------
        else:
            cols = st.columns(2)
            
            # 수락: 수정된 응답을 messages에 추가
            if cols[0].button("수락", type="primary"):
                st.session_state.messages.append(
                    AIMessage(content=st.session_state.pending)
                )
                # 모든 임시 데이터 정리
                st.session_state.pending = None
                st.session_state.validation = {}
                st.session_state.stage = "user"  # 사용자 입력 모드로 복귀
                st.rerun()
            
            # 처음부터 다시: 모든 문장을 다시 검토
            if cols[1].button("처음부터 다시"):
                for i in range(len(st.session_state.validation["valid"])):
                    st.session_state.validation["valid"][i] = False
                st.rerun()

# ============================================================================
# Stage 4: "rewrite" - 전체 재작성 단계
# ============================================================================
elif st.session_state.stage == "rewrite":
    """
    "rewrite" 단계: 응답 전체를 직접 편집하는 단계
    - text_area로 여러 줄의 텍스트를 자유롭게 수정
    - 업데이트: 수정된 내용을 messages에 추가
    - 취소: validate 단계로 돌아가기
    """
    st.chat_input("응답을 수락, 수정, 또는 재작성하세요.", disabled=True)
    
    with st.chat_message("assistant"):
        # YOUR CODE HERE - st.text_area()를 사용하여 응답 재작성 UI 생성
        # new_response = st.text_area(
        #     "응답 재작성:",
        #     value=st.session_state.pending,
        #     height=200
        # )
        # 
        # st.text_area(): 여러 줄 텍스트 입력창
        # - value: 초기값 (현재 pending 응답)
        # - height: 입력창 높이 (픽셀)
        # 사용자가 전체 텍스트를 자유롭게 편집할 수 있습니다
        
        new_response = ""  # 위의 YOUR CODE HERE를 채우면 이 줄을 삭제하세요
        
        cols = st.columns(2)
        
        # 빈 응답 체크
        is_empty = new_response is None or new_response.strip() == ""
        
        # 버튼 1: 업데이트 (수정된 응답 저장)
        if cols[0].button(
            "업데이트",
            type="primary",
            disabled=is_empty  # 빈 응답이면 버튼 비활성화
        ) and not is_empty:
            # 수정된 응답을 messages에 추가
            st.session_state.messages.append(
                AIMessage(content=new_response)
            )
            # 모든 임시 데이터 정리
            st.session_state.pending = None
            st.session_state.validation = {}
            st.session_state.stage = "user"  # 사용자 입력 모드로 복귀
            st.rerun()
        
        # 버튼 2: 취소 (validate 단계로 복귀)
        if cols[1].button("취소"):
            st.session_state.stage = "validate"
            st.rerun()


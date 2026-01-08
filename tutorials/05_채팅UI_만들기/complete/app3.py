import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(page_title="LangChain Chat", page_icon="💬", layout="wide")

st.title("💬 LangChain Chat")

MODELS = {
    "gpt-4.1-nano": "gpt-4.1-nano-2025-04-14",
    "gpt-4.1-mini": "gpt-4.1-mini-2025-04-14",
    "gpt-5-mini": "gpt-5-mini-2025-08-07",
    "gpt-5-nano": "gpt-5-nano-2025-08-07"
}

if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_model" not in st.session_state:
    st.session_state.selected_model = "gpt-4.1-mini"

if "stage" not in st.session_state:
    st.session_state.stage = "user"

if "pending" not in st.session_state:
    st.session_state.pending = None

if "validation" not in st.session_state:
    st.session_state.validation = {}

if "llm" not in st.session_state:
    st.session_state.llm = ChatOpenAI(
        model=MODELS[st.session_state.selected_model],
        temperature=0.7,
        streaming=True,
        api_key=os.getenv("OPENAI_API_KEY")
    )

def validate_response(response):
    response_sentences = response.split(". ")
    response_sentences = [
        sentence.strip(". ") + "." for sentence in response_sentences 
        if sentence.strip(". ") != ""
    ]
    validation_list = [True] * len(response_sentences)
    return response_sentences, validation_list

def add_highlights(response_sentences, validation_list, bg="red", text="red"):
    return [
        f":{text}[:{bg}-background[{sentence}]]" if not is_valid else sentence
        for sentence, is_valid in zip(response_sentences, validation_list)
    ]

with st.sidebar:
    st.header("설정")
    
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
    
    if st.button("대화 히스토리 초기화"):
        st.session_state.messages = []
        st.session_state.stage = "user"
        st.session_state.pending = None
        st.session_state.validation = {}
        st.rerun()
    
    st.divider()
    
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

for message in st.session_state.messages:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(message.content)

if st.session_state.stage == "user":
    if prompt := st.chat_input("메시지를 입력하세요..."):
        st.session_state.messages.append(HumanMessage(content=prompt))
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            for chunk in st.session_state.llm.stream(st.session_state.messages):
                full_response += chunk.content
                message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
        
        st.session_state.pending = full_response
        st.session_state.stage = "validate"
        st.rerun()

elif st.session_state.stage == "validate":
    st.chat_input("응답을 수락, 수정, 또는 재작성하세요.", disabled=True)
    
    response_sentences, validation_list = validate_response(st.session_state.pending)
    
    with st.chat_message("assistant"):
        st.markdown(st.session_state.pending)
        st.divider()
        
        cols = st.columns(3)
        
        if cols[0].button("문장별 수정", type="secondary"):
            st.session_state.validation = {
                "sentences": response_sentences,
                "valid": validation_list,
            }
            st.session_state.stage = "correct"
            st.rerun()
        
        if cols[1].button("수락", type="primary"):
            st.session_state.messages.append(
                AIMessage(content=st.session_state.pending)
            )
            st.session_state.pending = None
            st.session_state.validation = {}
            st.session_state.stage = "user"
            st.rerun()
        
        if cols[2].button("전체 재작성", type="secondary"):
            st.session_state.stage = "rewrite"
            st.rerun()

elif st.session_state.stage == "correct":
    st.chat_input("응답을 수락, 수정, 또는 재작성하세요.", disabled=True)
    
    response_sentences = st.session_state.validation["sentences"]
    validation_list = st.session_state.validation["valid"]
    
    if not all(validation_list):
        focus = validation_list.index(False)
    else:
        focus = None
    
    with st.chat_message("assistant"):
        for idx, sentence in enumerate(response_sentences):
            if idx == focus:
                st.markdown(f":red[:red-background[{sentence}]]")
            else:
                st.markdown(sentence)
        
        st.divider()
        
        if focus is not None:
            st.write(f"문장 {focus + 1} 수정:")
            new_sentence = st.text_input(
                "수정할 텍스트:",
                value=response_sentences[focus],
                key=f"edit_{focus}"
            )
            
            cols = st.columns(3)
            
            if cols[0].button(
                "업데이트",
                type="primary",
                disabled=len(new_sentence.strip()) < 1
            ):
                st.session_state.validation["sentences"][focus] = (
                    new_sentence.strip(". ") + "."
                )
                st.session_state.validation["valid"][focus] = True
                st.session_state.pending = " ".join(
                    st.session_state.validation["sentences"]
                )
                st.rerun()
            
            if cols[1].button("삭제"):
                st.session_state.validation["sentences"].pop(focus)
                st.session_state.validation["valid"].pop(focus)
                if len(st.session_state.validation["sentences"]) > 0:
                    st.session_state.pending = " ".join(
                        st.session_state.validation["sentences"]
                    )
                    st.rerun()
                else:
                    st.warning("마지막 문장입니다. 전체 재작성을 사용하세요.")
            
            if cols[2].button("다음 문장"):
                st.session_state.validation["valid"][focus] = True
                st.rerun()
        else:
            cols = st.columns(2)
            
            if cols[0].button("수락", type="primary"):
                st.session_state.messages.append(
                    AIMessage(content=st.session_state.pending)
                )
                st.session_state.pending = None
                st.session_state.validation = {}
                st.session_state.stage = "user"
                st.rerun()
            
            if cols[1].button("처음부터 다시"):
                for i in range(len(st.session_state.validation["valid"])):
                    st.session_state.validation["valid"][i] = False
                st.rerun()

elif st.session_state.stage == "rewrite":
    st.chat_input("응답을 수락, 수정, 또는 재작성하세요.", disabled=True)
    
    with st.chat_message("assistant"):
        new_response = st.text_area(
            "응답 재작성:",
            value=st.session_state.pending,
            height=200
        )
        
        cols = st.columns(2)
        
        is_empty = new_response is None or new_response.strip() == ""
        
        if cols[0].button(
            "업데이트",
            type="primary",
            disabled=is_empty
        ) and not is_empty:
            st.session_state.messages.append(
                AIMessage(content=new_response)
            )
            st.session_state.pending = None
            st.session_state.validation = {}
            st.session_state.stage = "user"
            st.rerun()
        
        if cols[1].button("취소"):
            st.session_state.stage = "validate"
            st.rerun()


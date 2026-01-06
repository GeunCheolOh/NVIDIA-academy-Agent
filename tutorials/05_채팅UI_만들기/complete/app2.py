import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from dotenv import load_dotenv
import os
from datetime import datetime
import uuid

load_dotenv()

st.set_page_config(page_title="LangChain Chat", page_icon="💬", layout="wide")

MODELS = {
    "gpt-4.1-nano": "gpt-4.1-nano-2025-04-14",
    "gpt-4.1-mini": "gpt-4.1-mini-2025-04-14",
    "gpt-5-mini": "gpt-5-mini-2025-08-07",
    "gpt-5-nano": "gpt-5-nano-2025-08-07"
}

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

if "selected_model" not in st.session_state:
    st.session_state.selected_model = "gpt-4.1-mini"

if "llm" not in st.session_state:
    st.session_state.llm = ChatOpenAI(
        model=MODELS[st.session_state.selected_model],
        temperature=0.7,
        streaming=True,
        api_key=os.getenv("OPENAI_API_KEY")
    )

def create_new_conversation():
    new_id = str(uuid.uuid4())
    st.session_state.conversations[new_id] = {
        "id": new_id,
        "title": "새 대화",
        "messages": [],
        "created_at": datetime.now()
    }
    st.session_state.active_conversation_id = new_id

def get_conversation_title(messages):
    if not messages:
        return "새 대화"
    first_user_msg = next((msg.content for msg in messages if isinstance(msg, HumanMessage)), None)
    if first_user_msg:
        return first_user_msg[:30] + "..." if len(first_user_msg) > 30 else first_user_msg
    return "새 대화"

def delete_conversation(conv_id):
    if len(st.session_state.conversations) > 1:
        del st.session_state.conversations[conv_id]
        if st.session_state.active_conversation_id == conv_id:
            st.session_state.active_conversation_id = list(st.session_state.conversations.keys())[0]

current_conv = st.session_state.conversations[st.session_state.active_conversation_id]

col1, col2 = st.columns([6, 1])
with col1:
    st.title("💬 LangChain Chat")
with col2:
    if st.button("➕ 새 대화", use_container_width=True):
        create_new_conversation()
        st.rerun()

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
    
    st.subheader("대화 세션")
    
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

for message in current_conv["messages"]:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(message.content)

if prompt := st.chat_input("메시지를 입력하세요..."):
    current_conv["messages"].append(HumanMessage(content=prompt))
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        for chunk in st.session_state.llm.stream(current_conv["messages"]):
            full_response += chunk.content
            message_placeholder.markdown(full_response + "▌")
        
        message_placeholder.markdown(full_response)
    
    current_conv["messages"].append(AIMessage(content=full_response))
    st.rerun()

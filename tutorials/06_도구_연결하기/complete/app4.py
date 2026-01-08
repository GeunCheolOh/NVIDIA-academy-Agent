import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_community.tools.tavily_search import TavilySearchResults
from ddgs import DDGS
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
            "search_results": {},
            "system_prompt": "",
            "created_at": datetime.now()
        }
    }
    st.session_state.active_conversation_id = first_id

if "selected_model" not in st.session_state:
    st.session_state.selected_model = "gpt-4.1-mini"

if "search_engine" not in st.session_state:
    st.session_state.search_engine = None

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
        "search_results": {},
        "system_prompt": "",
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

def search_tavily(query):
    try:
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            return None, "❌ Tavily API 키가 설정되지 않았습니다. .env 파일에 TAVILY_API_KEY를 추가하세요."
        
        search_tool = TavilySearchResults(
            max_results=5,
            api_key=api_key
        )
        results = search_tool.invoke(query)
        
        formatted_results = "### 🔍 Tavily 검색 결과:\n\n"
        for i, result in enumerate(results, 1):
            formatted_results += f"**{i}. {result.get('title', 'No title')}**\n"
            formatted_results += f"{result.get('content', result.get('snippet', 'No content'))}\n"
            formatted_results += f"🔗 {result.get('url', '')}\n\n"
        
        return formatted_results, None
    except Exception as e:
        return None, f"❌ Tavily 검색 오류: {str(e)}"

def search_duckduckgo(query):
    try:
        ddgs = DDGS()
        results = list(ddgs.text(query, max_results=5))
        
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
    
    st.subheader("시스템 프롬프트")
    
    if "system_prompt" not in current_conv:
        current_conv["system_prompt"] = ""
    
    system_prompt = st.text_area(
        "시스템 프롬프트 설정",
        value=current_conv.get("system_prompt", ""),
        height=150,
        placeholder="예: 당신은 친절한 AI 어시스턴트입니다. 항상 한국어로 답변하세요.",
        help="AI의 역할과 답변 스타일을 정의합니다. 비워두면 기본 동작을 사용합니다."
    )
    
    if system_prompt != current_conv.get("system_prompt", ""):
        current_conv["system_prompt"] = system_prompt
        if system_prompt:
            st.success("시스템 프롬프트가 적용되었습니다.")
        else:
            st.info("시스템 프롬프트가 비활성화되었습니다.")
    
    if current_conv.get("system_prompt"):
        st.caption(f"✓ 시스템 프롬프트 활성화 ({len(current_conv['system_prompt'])}자)")
    
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

for idx, message in enumerate(current_conv["messages"]):
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
        if idx in current_conv.get("search_results", {}):
            with st.expander("🔍 검색 결과 보기", expanded=False):
                st.markdown(current_conv["search_results"][idx])
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(message.content)

col1, col2, col3 = st.columns([1, 1, 6])
with col1:
    tavily_enabled = st.button("🌐 Tavily", use_container_width=True, 
                               type="primary" if st.session_state.search_engine == "tavily" else "secondary")
    if tavily_enabled:
        st.session_state.search_engine = "tavily" if st.session_state.search_engine != "tavily" else None

with col2:
    duckduckgo_enabled = st.button("🦆 DuckDuckGo", use_container_width=True,
                              type="primary" if st.session_state.search_engine == "duckduckgo" else "secondary")
    if duckduckgo_enabled:
        st.session_state.search_engine = "duckduckgo" if st.session_state.search_engine != "duckduckgo" else None

if st.session_state.search_engine:
    st.info(f"✓ {st.session_state.search_engine.capitalize()} 검색이 활성화되었습니다.")

if prompt := st.chat_input("메시지를 입력하세요..."):
    search_results = None
    search_error = None
    
    if st.session_state.search_engine == "tavily":
        with st.spinner("Tavily로 검색 중..."):
            search_results, search_error = search_tavily(prompt)
    elif st.session_state.search_engine == "duckduckgo":
        with st.spinner("DuckDuckGo로 검색 중..."):
            search_results, search_error = search_duckduckgo(prompt)
    
    current_conv["messages"].append(HumanMessage(content=prompt))
    user_msg_idx = len(current_conv["messages"]) - 1
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    if search_error:
        st.error(search_error)
        messages_with_search = current_conv["messages"].copy()
    elif search_results:
        current_conv["search_results"][user_msg_idx] = search_results
        
        with st.expander("🔍 검색 결과 보기", expanded=False):
            st.markdown(search_results)
        
        augmented_prompt = f"{prompt}\n\n{search_results}\n\n위 검색 결과를 참고하여 답변해주세요."
        messages_with_search = current_conv["messages"][:-1] + [HumanMessage(content=augmented_prompt)]
    else:
        messages_with_search = current_conv["messages"].copy()
    
    if current_conv.get("system_prompt"):
        messages_with_system = [SystemMessage(content=current_conv["system_prompt"])] + messages_with_search
    else:
        messages_with_system = messages_with_search
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        for chunk in st.session_state.llm.stream(messages_with_system):
            full_response += chunk.content
            message_placeholder.markdown(full_response + "▌")
        
        message_placeholder.markdown(full_response)
    
    current_conv["messages"].append(AIMessage(content=full_response))
    st.rerun()


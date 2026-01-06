"""
rag_router_agent.py - Router 기반 다중 경로 Agent
================================================

목적:
    LLM을 Router로 사용하여 질문 유형에 따라
    VectorDB, WebSearch, Direct LLM 중 적절한 경로를 선택

주요 기능:
    1. Router Node: LLM이 경로 결정
    2. VectorDB Node: D2L 교재 검색
    3. WebSearch Node: Tavily 웹검색
    4. Direct LLM Node: LLM 직접 응답
    5. Answer Node: 최종 답변 생성
"""

import json
from typing import TypedDict, Annotated, List, Optional
import operator

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, BaseMessage
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.graph import StateGraph, END


class AgentState(TypedDict):
    """Agent의 상태 정의"""
    messages: Annotated[List[BaseMessage], operator.add]  # 대화 이력
    question: str                    # 현재 질문
    route: str                       # 선택된 경로
    routing_reason: str              # 라우팅 이유
    search_results: str              # 검색 결과
    final_answer: str                # 최종 답변


class RouterAgent:
    """
    Router 기반 다중 경로 RAG Agent
    
    경로:
    - vectordb: AI/딥러닝 관련 질문 → D2L 교재 검색
    - websearch: 최신 정보 → 웹검색
    - direct: 일반 질문 → LLM 직접 응답
    """
    
    def __init__(
        self,
        d2l_retriever,
        api_key: str,
        model: str = "gpt-4.1-mini-2025-04-14",
        tavily_api_key: Optional[str] = None
    ):
        """
        Args:
            d2l_retriever: D2L 교재 검색기
            api_key: OpenAI API 키
            model: 사용할 LLM 모델
            tavily_api_key: Tavily API 키
        """
        self.d2l_retriever = d2l_retriever
        
        # LLM 초기화
        self.llm = ChatOpenAI(
            model=model,
            temperature=0.3,
            api_key=api_key
        )
        
        # Tavily 웹검색 도구
        if tavily_api_key:
            self.tavily_tool = TavilySearchResults(
                max_results=3,
                api_key=tavily_api_key
            )
        else:
            self.tavily_tool = None
        
        # Agent 그래프 생성
        self.agent = self._build_graph()
    
    def _build_graph(self):
        """LangGraph 상태 그래프를 구성"""
        workflow = StateGraph(AgentState)
        
        # 노드 추가
        workflow.add_node("router", self._router_node)
        workflow.add_node("vectordb", self._vectordb_node)
        workflow.add_node("websearch", self._websearch_node)
        workflow.add_node("direct_llm", self._direct_llm_node)
        workflow.add_node("answer", self._answer_node)
        
        # 시작점
        workflow.set_entry_point("router")
        
        # 조건부 엣지: router에서 경로 분기
        workflow.add_conditional_edges(
            "router",
            self._route_question,
            {
                "vectordb": "vectordb",
                "websearch": "websearch",
                "direct": "direct_llm"
            }
        )
        
        # vectordb/websearch → answer
        workflow.add_edge("vectordb", "answer")
        workflow.add_edge("websearch", "answer")
        
        # direct_llm → END (답변 이미 생성됨)
        workflow.add_edge("direct_llm", END)
        
        # answer → END
        workflow.add_edge("answer", END)
        
        return workflow.compile()
    
    def _router_node(self, state: AgentState) -> dict:
        """
        Router 노드: LLM이 질문을 분석하여 적절한 경로 결정
        
        Args:
            state: 현재 Agent 상태
            
        Returns:
            업데이트할 상태 (route, routing_reason)
        """
        question = state["question"]
        
        router_prompt = f"""다음 질문을 분석하여 가장 적절한 처리 방법을 선택하세요.

질문: {question}

선택지:
1. **vectordb**: AI, 딥러닝, 머신러닝, 신경망, 최적화 알고리즘 등 AI/ML 기술적 질문
   - 예: "backpropagation이란?", "CNN의 구조는?", "gradient descent 설명"
   - 출처: D2L (Dive into Deep Learning) 교재

2. **websearch**: 최신 뉴스, 실시간 정보, 2023년 이후 이벤트, 현재 날씨/주가 등
   - 예: "2024년 노벨상", "오늘 날씨", "최신 AI 뉴스"
   - 출처: 웹 검색

3. **direct**: 일반 대화, 번역, 계산, 추론, 창작 등
   - 예: "안녕하세요", "1+1은?", "시 써줘", "Python 코드 작성"
   - 출처: LLM 직접 응답

다음 형식으로 JSON 응답:
{{
    "route": "vectordb" 또는 "websearch" 또는 "direct",
    "reasoning": "선택한 이유를 한 문장으로"
}}

JSON만 출력하세요."""

        try:
            response = self.llm.invoke([SystemMessage(content=router_prompt)])
            result = json.loads(response.content)
            
            route = result.get("route", "direct")
            reasoning = result.get("reasoning", "기본 경로 선택")
            
            # 유효성 검사
            if route not in ["vectordb", "websearch", "direct"]:
                route = "direct"
                reasoning = "알 수 없는 경로, 기본 경로 사용"
            
            print(f"🧭 Router 결정: {route}")
            print(f"   이유: {reasoning}")
            
            return {
                "route": route,
                "routing_reason": reasoning
            }
            
        except Exception as e:
            print(f"⚠️ Router 오류: {str(e)}, 기본 경로 사용")
            return {
                "route": "direct",
                "routing_reason": f"라우팅 오류 발생: {str(e)}"
            }
    
    def _vectordb_node(self, state: AgentState) -> dict:
        """
        VectorDB 노드: D2L 교재에서 검색
        
        Args:
            state: 현재 Agent 상태
            
        Returns:
            업데이트할 상태 (search_results)
        """
        question = state["question"]
        
        try:
            print(f"📚 D2L 교재 검색: '{question}'")
            docs = self.d2l_retriever.invoke(question)
            
            if docs:
                results = "\n\n".join([
                    f"[문서 {i+1}]\n{doc.page_content}" 
                    for i, doc in enumerate(docs)
                ])
                print(f"✅ {len(docs)}개 문서 검색 완료")
            else:
                results = "관련 문서를 찾을 수 없습니다."
                print("⚠️ 검색 결과 없음")
            
            return {"search_results": results}
            
        except Exception as e:
            print(f"❌ VectorDB 검색 실패: {str(e)}")
            return {"search_results": f"검색 중 오류 발생: {str(e)}"}
    
    def _websearch_node(self, state: AgentState) -> dict:
        """
        WebSearch 노드: Tavily로 웹 검색
        
        Args:
            state: 현재 Agent 상태
            
        Returns:
            업데이트할 상태 (search_results)
        """
        question = state["question"]
        
        if not self.tavily_tool:
            return {
                "search_results": "웹 검색 도구가 설정되지 않았습니다. Tavily API 키를 확인하세요."
            }
        
        try:
            print(f"🌐 웹 검색: '{question}'")
            search_results = self.tavily_tool.invoke(question)
            
            if search_results:
                results = "\n\n".join([
                    f"[{r.get('title', '제목 없음')}]\n{r.get('content', '')}" 
                    for r in search_results
                ])
                print(f"✅ {len(search_results)}개 결과 검색 완료")
            else:
                results = "검색 결과를 찾을 수 없습니다."
                print("⚠️ 검색 결과 없음")
            
            return {"search_results": results}
            
        except Exception as e:
            print(f"❌ 웹 검색 실패: {str(e)}")
            return {"search_results": f"검색 중 오류 발생: {str(e)}"}
    
    def _direct_llm_node(self, state: AgentState) -> dict:
        """
        Direct LLM 노드: LLM에 직접 질문
        
        Args:
            state: 현재 Agent 상태
            
        Returns:
            업데이트할 상태 (final_answer)
        """
        question = state["question"]
        messages = state.get("messages", [])
        
        try:
            print(f"💬 LLM 직접 응답: '{question}'")
            
            # 대화 이력 포함
            conversation = messages + [HumanMessage(content=question)]
            response = self.llm.invoke(conversation)
            
            print("✅ 답변 생성 완료")
            
            return {
                "final_answer": response.content,
                "messages": [
                    HumanMessage(content=question),
                    AIMessage(content=response.content)
                ]
            }
            
        except Exception as e:
            print(f"❌ LLM 응답 실패: {str(e)}")
            return {
                "final_answer": f"답변 생성 중 오류가 발생했습니다: {str(e)}",
                "messages": []
            }
    
    def _answer_node(self, state: AgentState) -> dict:
        """
        Answer 노드: 검색 결과를 바탕으로 최종 답변 생성
        
        Args:
            state: 현재 Agent 상태
            
        Returns:
            업데이트할 상태 (final_answer, messages)
        """
        question = state["question"]
        search_results = state["search_results"]
        route = state["route"]
        messages = state.get("messages", [])
        
        # direct 경로는 이미 답변이 생성되어 있음
        if route == "direct":
            return {}
        
        try:
            print(f"✍️  최종 답변 생성 중...")
            
            # 대화 이력 포맷팅
            history = ""
            if messages:
                history = "\n이전 대화:\n"
                for msg in messages[-4:]:  # 최근 4개만
                    role = "사용자" if isinstance(msg, HumanMessage) else "AI"
                    history += f"{role}: {msg.content[:100]}...\n"
            
            answer_prompt = f"""{history}

질문: {question}

참고 자료 (출처: {'D2L 교재' if route == 'vectordb' else '웹 검색'}):
{search_results}

위 참고 자료를 바탕으로 질문에 대해 정확하고 상세한 답변을 작성해주세요.
참고 자료에서 답을 찾을 수 없다면 솔직하게 말씀해주세요."""

            response = self.llm.invoke([SystemMessage(content=answer_prompt)])
            
            print("✅ 답변 생성 완료")
            
            return {
                "final_answer": response.content,
                "messages": [
                    HumanMessage(content=question),
                    AIMessage(content=response.content)
                ]
            }
            
        except Exception as e:
            print(f"❌ 답변 생성 실패: {str(e)}")
            return {
                "final_answer": f"답변 생성 중 오류가 발생했습니다: {str(e)}",
                "messages": []
            }
    
    def _route_question(self, state: AgentState) -> str:
        """
        라우팅 함수: state["route"]를 보고 다음 노드 결정
        
        Args:
            state: 현재 Agent 상태
            
        Returns:
            다음 노드 이름
        """
        return state["route"]
    
    def invoke(self, question: str, chat_history: Optional[List[BaseMessage]] = None) -> dict:
        """
        질문에 대한 답변을 생성합니다.
        
        Args:
            question: 사용자 질문
            chat_history: 이전 대화 이력
            
        Returns:
            결과 딕셔너리
            {
                "question": 질문,
                "route": 선택된 경로,
                "routing_reason": 라우팅 이유,
                "search_results": 검색 결과 (있는 경우),
                "answer": 최종 답변
            }
        """
        print("\n" + "=" * 60)
        print(f"질문: {question}")
        print("=" * 60)
        
        # 초기 상태 설정
        initial_state = {
            "messages": chat_history or [],
            "question": question,
            "route": "",
            "routing_reason": "",
            "search_results": "",
            "final_answer": ""
        }
        
        # Agent 실행
        result = self.agent.invoke(initial_state)
        
        return {
            "question": question,
            "route": result.get("route", "unknown"),
            "routing_reason": result.get("routing_reason", ""),
            "search_results": result.get("search_results", ""),
            "answer": result.get("final_answer", "답변을 생성할 수 없습니다.")
        }


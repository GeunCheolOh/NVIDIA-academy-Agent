"""
rag_agent.py - LangGraph 기반 RAG Agent
========================================

목적:
    ReAct 패턴을 사용하여 문서 검색과 응답 생성을 수행하는 
    지능형 RAG Agent를 구현합니다.

주요 기능:
    1. ReAct 패턴 (Thought-Action-Observation)
    2. 문서 검색 (VectorDB)
    3. 검색 결과 평가
    4. 대화 컨텍스트 유지
    5. 재시도 메커니즘

사용 기술:
    - LangGraph: 상태 그래프
    - LangChain: LLM, 검색기
    - SqliteSaver: 대화 메모리
"""

import json
from typing import TypedDict, Annotated, List, Optional
import operator

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, BaseMessage
from langgraph.graph import StateGraph, END


class AgentState(TypedDict):
    """
    Agent의 상태를 정의하는 TypedDict
    """
    messages: Annotated[List[BaseMessage], operator.add]  # 대화 이력
    question: str  # 현재 질문
    search_results: str  # 검색 결과
    is_relevant: bool  # 검색 결과가 관련 있는지
    iteration: int  # 현재 반복 횟수
    final_answer: str  # 최종 답변


class RAGAgent:
    """
    LangGraph 기반 RAG Agent
    
    ReAct 패턴으로 동작:
    1. Thought: 검색 필요성 판단
    2. Action: 문서 검색 수행
    3. Observation: 결과 평가 및 답변 생성
    """
    
    def __init__(
        self, 
        retriever, 
        api_key: str,
        model: str = "gpt-4.1-mini-2025-04-14",
        max_iterations: int = 3
    ):
        """
        Args:
            retriever: 벡터 스토어 검색기
            api_key: OpenAI API 키
            model: 사용할 LLM 모델
            max_iterations: 최대 재시도 횟수
        """
        self.retriever = retriever
        self.max_iterations = max_iterations
        
        # LLM 초기화
        self.llm = ChatOpenAI(
            model=model,
            temperature=0.3,
            api_key=api_key
        )
        
        # Agent 그래프 생성
        self.agent = self._build_graph()
    
    def _build_graph(self):
        """
        LangGraph 상태 그래프를 구성합니다.
        """
        workflow = StateGraph(AgentState)
        
        # 노드 추가
        workflow.add_node("thought", self._thought_node)
        workflow.add_node("action", self._action_node)
        workflow.add_node("observation", self._observation_node)
        
        # 엣지 연결
        workflow.set_entry_point("thought")
        workflow.add_edge("thought", "action")
        workflow.add_edge("action", "observation")
        workflow.add_conditional_edges(
            "observation",
            self._should_continue,
            {"continue": "thought", "end": END}
        )
        
        # 메모리 없이 컴파일 (각 대화는 독립적)
        return workflow.compile()
    
    def _format_history(self, messages: List[BaseMessage]) -> str:
        """
        대화 히스토리를 문자열로 포맷합니다.
        
        Args:
            messages: 메시지 리스트
            
        Returns:
            포맷된 히스토리 문자열
        """
        if not messages:
            return ""
        
        history = "\n이전 대화:\n"
        for msg in messages[-6:]:  # 최근 6개만
            role = "사용자" if isinstance(msg, HumanMessage) else "AI"
            content = msg.content[:200] if len(msg.content) > 200 else msg.content
            history += f"{role}: {content}\n"
        
        return history
    
    def _thought_node(self, state: AgentState) -> dict:
        """
        Thought 노드: 검색 필요성을 판단합니다.
        
        Args:
            state: 현재 Agent 상태
            
        Returns:
            업데이트할 상태 딕셔너리
        """
        question = state["question"]
        iteration = state.get("iteration", 0)
        
        # 첫 시도이거나 재시도인 경우
        if iteration > 0:
            context = "이전 검색 결과가 충분하지 않았습니다. 다시 검색이 필요합니다.\n"
        else:
            context = ""
        
        return {"iteration": iteration + 1}
    
    def _action_node(self, state: AgentState) -> dict:
        """
        Action 노드: 문서 검색을 수행합니다.
        
        Args:
            state: 현재 Agent 상태
            
        Returns:
            업데이트할 상태 딕셔너리
        """
        question = state["question"]
        
        try:
            # 벡터 스토어에서 관련 문서 검색
            docs = self.retriever.invoke(question)
            
            # 검색 결과를 하나의 문자열로 결합
            if docs:
                results = "\n\n".join([
                    f"[문서 {i+1}]\n{doc.page_content}" 
                    for i, doc in enumerate(docs)
                ])
            else:
                results = "관련 문서를 찾을 수 없습니다."
            
            return {"search_results": results}
            
        except Exception as e:
            return {"search_results": f"검색 중 오류 발생: {str(e)}"}
    
    def _observation_node(self, state: AgentState) -> dict:
        """
        Observation 노드: 검색 결과를 평가하고 답변을 생성합니다.
        
        Args:
            state: 현재 Agent 상태
            
        Returns:
            업데이트할 상태 딕셔너리
        """
        question = state["question"]
        results = state["search_results"]
        iteration = state.get("iteration", 0)
        messages = state.get("messages", [])
        
        # 1단계: 검색 결과 평가
        eval_prompt = f"""검색 결과가 질문에 답할 수 있을 만큼 충분한지 평가해주세요.

질문: {question}

검색 결과:
{results[:1000]}...

다음 형식으로 JSON 응답:
{{
    "is_relevant": true/false,
    "reason": "평가 이유"
}}
"""
        
        try:
            eval_response = self.llm.invoke([SystemMessage(content=eval_prompt)])
            eval_result = json.loads(eval_response.content)
            is_relevant = eval_result.get("is_relevant", False)
        except:
            # JSON 파싱 실패 시 기본값
            is_relevant = True
        
        # 2단계: 검색 결과가 부족하고 재시도 가능한 경우
        if not is_relevant and iteration < self.max_iterations:
            return {"is_relevant": False}
        
        # 3단계: 최종 답변 생성
        history = self._format_history(messages)
        
        answer_prompt = f"""{history}

질문: {question}

참고 문서:
{results}

위 문서를 바탕으로 질문에 대해 정확하고 상세한 답변을 작성해주세요.
문서에서 답을 찾을 수 없다면 솔직하게 말씀해주세요."""

        try:
            response = self.llm.invoke([SystemMessage(content=answer_prompt)])
            answer = response.content
        except Exception as e:
            answer = f"답변 생성 중 오류가 발생했습니다: {str(e)}"
        
        return {
            "is_relevant": True,
            "final_answer": answer,
            "messages": [
                HumanMessage(content=question),
                AIMessage(content=answer)
            ]
        }
    
    def _should_continue(self, state: AgentState) -> str:
        """
        계속 진행할지 종료할지 결정하는 조건부 엣지 함수
        
        Args:
            state: 현재 Agent 상태
            
        Returns:
            "continue" 또는 "end"
        """
        is_relevant = state.get("is_relevant", False)
        iteration = state.get("iteration", 0)
        
        if is_relevant or iteration >= self.max_iterations:
            return "end"
        else:
            return "continue"
    
    def invoke(self, question: str, chat_history: Optional[List[BaseMessage]] = None) -> dict:
        """
        질문에 대한 답변을 생성합니다.
        
        Args:
            question: 사용자 질문
            chat_history: 이전 대화 이력 (선택사항)
            
        Returns:
            결과 딕셔너리
            {
                "question": 질문,
                "answer": 답변,
                "search_results": 검색 결과,
                "iterations": 반복 횟수
            }
        """
        # 초기 상태 설정
        initial_state = {
            "messages": chat_history or [],
            "question": question,
            "search_results": "",
            "is_relevant": False,
            "iteration": 0,
            "final_answer": ""
        }
        
        # Agent 실행
        result = self.agent.invoke(initial_state)
        
        return {
            "question": question,
            "answer": result.get("final_answer", "답변을 생성할 수 없습니다."),
            "search_results": result.get("search_results", ""),
            "iterations": result.get("iteration", 0)
        }
    
    def stream(self, question: str, chat_history: Optional[List[BaseMessage]] = None):
        """
        스트리밍 방식으로 답변을 생성합니다.
        (현재는 invoke와 동일하게 동작, 향후 확장 가능)
        
        Args:
            question: 사용자 질문
            chat_history: 이전 대화 이력
            
        Yields:
            답변 청크
        """
        result = self.invoke(question, chat_history)
        
        # 답변을 단어 단위로 나누어 반환 (스트리밍 효과)
        answer = result["answer"]
        words = answer.split()
        
        for i, word in enumerate(words):
            if i == 0:
                yield word
            else:
                yield " " + word


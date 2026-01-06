"""
rag_agent.py - LangGraph 기반 RAG Agent
========================================

학습 목표:
    1. LangGraph StateGraph 구성
    2. ReAct 패턴 (Thought-Action-Observation)
    3. 문서 검색 (Retriever)
    4. 검색 결과 평가 및 재시도
    5. 최종 답변 생성
"""

import json
from typing import TypedDict, Annotated, List, Optional
import operator

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, BaseMessage
from langgraph.graph import StateGraph, END


class AgentState(TypedDict):
    """
    Agent의 상태를 정의
    
    LangGraph에서 상태는 노드 간 전달되는 데이터입니다.
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
    
    ReAct 패턴:
    - Thought (생각): 무엇을 해야 하나?
    - Action (행동): 문서 검색
    - Observation (관찰): 결과 평가 → 재시도 or 답변 생성
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
        
        # YOUR CODE HERE - ChatOpenAI LLM 초기화
        # self.llm = ChatOpenAI(
        #     model=model,
        #     temperature=0.3,
        #     api_key=api_key
        # )
        # 
        # temperature=0.3: 약간의 창의성(낮을수록 일관적)
        # model: 사용할 LLM 모델 (gpt-4.1-mini 등)
        self.llm = None  # 위의 YOUR CODE HERE를 채우면 이 줄을 삭제하세요
        
        # Agent 그래프 생성
        self.agent = self._build_graph()
    
    def _build_graph(self):
        """
        LangGraph 상태 그래프를 구성합니다.
        
        그래프 구조:
        thought → action → observation
           ↑                    ↓
           └──── (재시도) ───────┘
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
        
        return workflow.compile()
    
    def _format_history(self, messages: List[BaseMessage]) -> str:
        """대화 히스토리를 문자열로 포맷"""
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
        Thought 노드: 검색 필요성을 판단
        
        실제로는 단순히 반복 횟수만 증가시킵니다.
        (더 복잡한 로직을 추가할 수 있음)
        """
        iteration = state.get("iteration", 0)
        return {"iteration": iteration + 1}
    
    def _action_node(self, state: AgentState) -> dict:
        """
        Action 노드: 문서 검색을 수행
        
        Args:
            state: 현재 Agent 상태
            
        Returns:
            업데이트할 상태 (search_results)
        """
        question = state["question"]
        
        try:
            # YOUR CODE HERE - retriever로 관련 문서 검색
            # docs = self.retriever.invoke(question)
            # 
            # retriever.invoke(query): 질문과 유사한 문서를 검색
            # 벡터 유사도 기반으로 상위 k개 문서 반환
            docs = []  # 위의 YOUR CODE HERE를 채우면 이 줄을 삭제하세요
            
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
        Observation 노드: 검색 결과를 평가하고 답변을 생성
        
        Args:
            state: 현재 Agent 상태
            
        Returns:
            업데이트할 상태 (is_relevant, final_answer, messages)
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
            # YOUR CODE HERE - LLM으로 검색 결과 평가
            # eval_response = self.llm.invoke([SystemMessage(content=eval_prompt)])
            # eval_result = json.loads(eval_response.content)
            # is_relevant = eval_result.get("is_relevant", False)
            # 
            # LLM에게 검색 결과가 충분한지 평가를 요청
            # JSON 형식으로 답변을 받아 파싱
            is_relevant = True  # 위의 YOUR CODE HERE를 채우면 이 줄을 삭제하세요
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
            # YOUR CODE HERE - LLM으로 최종 답변 생성
            # response = self.llm.invoke([SystemMessage(content=answer_prompt)])
            # answer = response.content
            # 
            # 검색된 문서를 기반으로 질문에 대한 답변 생성
            # LLM이 문서 내용을 참고하여 답변을 작성
            answer = "답변 생성 실패"  # 위의 YOUR CODE HERE를 채우면 이 줄을 삭제하세요
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
        # YOUR CODE HERE - 초기 상태 설정
        # initial_state = {
        #     "messages": chat_history or [],
        #     "question": question,
        #     "search_results": "",
        #     "is_relevant": False,
        #     "iteration": 0,
        #     "final_answer": ""
        # }
        # 
        # initial_state: Agent가 시작할 때의 초기 상태
        # 각 필드를 적절히 초기화해야 함
        initial_state = {}  # 위의 YOUR CODE HERE를 채우면 이 줄을 삭제하세요
        
        # YOUR CODE HERE - Agent 실행
        # result = self.agent.invoke(initial_state)
        # 
        # agent.invoke(): 상태 그래프를 실행
        # Thought → Action → Observation을 반복하며 답변 생성
        result = {}  # 위의 YOUR CODE HERE를 채우면 이 줄을 삭제하세요
        
        return {
            "question": question,
            "answer": result.get("final_answer", "답변을 생성할 수 없습니다."),
            "search_results": result.get("search_results", ""),
            "iterations": result.get("iteration", 0)
        }
    
    def stream(self, question: str, chat_history: Optional[List[BaseMessage]] = None):
        """
        스트리밍 방식으로 답변을 생성합니다.
        (현재는 invoke와 동일하게 동작)
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


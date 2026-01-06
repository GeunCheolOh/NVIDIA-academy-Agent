# 06. LangChain에 도구 연결하기

LLM에 외부 도구(Tool)를 연결하여 확장된 기능을 제공하는 방법을 학습합니다.

## 📚 학습 내용

### 06_1. OpenAI Function Calling
- OpenAI API의 Function Calling 기능 이해
- 수학 계산 도구 정의 및 사용
- 세 가지 Agent 프롬프팅 기법:
  - **Plan-and-Execute**: 계획 수립 후 순차 실행
  - **ReAct**: Thought-Action-Observation 반복
  - **Self-Reflection**: 자기 성찰을 통한 답변 개선

### 06_2. LangChain Built-in & Third-party Tools
- Third-party Tool: Tavily 웹 검색
- Built-in Tool: DuckDuckGo 검색
- Toolkit: File Management Toolkit
- Agent 생성 및 실행

### 06_3. LangChain Custom Tools
- Custom Tool을 만드는 4가지 방법:
  - `@tool` 데코레이터
  - `StructuredTool` 클래스
  - `BaseTool` 클래스 상속
  - LangChain Runnable(LCEL) 활용
- 복합 도구를 사용하는 Agent 구현

## 🎯 핵심 개념

### Function Calling이란?
LLM이 자체적으로 수행할 수 없는 작업(계산, 검색, 파일 조작 등)을 외부 함수를 호출하여 해결하는 기능입니다.

### Tool vs Toolkit
- **Tool**: 단일 기능을 수행하는 도구 (예: 검색, 계산)
- **Toolkit**: 관련된 여러 도구의 묶음 (예: 파일 관리 도구 모음)

### Agent Prompting 기법

#### 1. Plan-and-Execute
```
장점: 명확한 구조, 체계적 접근
단점: 계획 변경 어려움, 유연성 부족
```

#### 2. ReAct (Reasoning + Acting)
```
Thought → Action → Observation 반복
장점: 유연한 대응, 동적 문제 해결
단점: 반복으로 인한 비효율성
```

#### 3. Self-Reflection
```
초기 답변 → 비판적 평가 → 개선된 답변
장점: 높은 품질, 오류 자체 수정
단점: 추가 API 호출, 시간 소요
```

## 🚀 실행 방법

### 환경 설정

```bash
cd tutorials/06_도구_연결하기

# 필요한 패키지 설치
pip install langchain langchain-openai langchain-community langchain-tavily
pip install openai tavily-python duckduckgo-search

# API 키 설정
# 프로젝트 루트의 .env 파일에 추가
# OPENAI_API_KEY=your-api-key
# TAVILY_API_KEY=your-api-key (Tavily 사용 시)
```

### Jupyter Notebook 실행

```bash
jupyter notebook 06_1_OpenAI_Function_Calling.ipynb
jupyter notebook 06_2_LangChain_Built_in_Tools.ipynb
jupyter notebook 06_3_LangChain_Custom_Tools.ipynb
```

## 📋 실습 구성

### 06_1_OpenAI_Function_Calling.ipynb
```
1. 환경 설정 및 모델 준비
2. 수학 계산 도구 정의
3. Plan-and-Execute 방식 구현
4. ReAct 방식 구현
5. Self-Reflection 방식 구현
```

**예제 문제**: 반지름이 5cm인 원에 내접하는 정삼각형의 한 변의 길이 구하기

### 06_2_LangChain_Built_in_Tools.ipynb
```
1. 환경 설정
2. Tavily 웹 검색 도구
3. DuckDuckGo 웹 검색 도구
4. File Management Toolkit
5. Agent 생성 및 실행

빈칸 채우기:
- DuckDuckGo 도구 호출
- Toolkit의 get_tools() 메서드
- Tool 정의 (Tavily, DuckDuckGo)
- AgentExecutor 생성
- Agent 실행 (invoke)
```

### 06_3_LangChain_Custom_Tools.ipynb
```
1. 환경 설정
2. @tool 데코레이터로 시간 조회 도구
3. StructuredTool로 계산기 도구
4. BaseTool로 사용자 프로필 도구
5. Runnable로 텍스트 요약 도구
6. Agent 생성 및 실행

빈칸 채우기:
- Pydantic 모델로 인자 정의
- StructuredTool.from_function()
- BaseTool 클래스 상속
- Runnable을 Tool로 변환
- Agent 생성
```

## 💡 주요 API

### OpenAI Function Calling
```python
from openai import OpenAI

client = OpenAI()

# Function 정의
tools = [{
    "type": "function",
    "function": {
        "name": "calculate",
        "description": "수학 표현식을 계산",
        "parameters": {...}
    }
}]

# Function Calling 실행
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    tools=tools,
    tool_choice="auto"
)
```

### LangChain Tool
```python
from langchain.tools import tool, Tool, StructuredTool, BaseTool

# 1. @tool 데코레이터
@tool
def my_tool(query: str) -> str:
    """도구 설명"""
    return result

# 2. Tool 클래스
tool = Tool(
    name="MyTool",
    func=my_function,
    description="도구 설명"
)

# 3. StructuredTool
tool = StructuredTool.from_function(
    func=my_function,
    name="MyTool",
    description="도구 설명",
    args_schema=MyInputSchema
)

# 4. BaseTool 상속
class MyTool(BaseTool):
    name: str = "my_tool"
    description: str = "도구 설명"
    
    def _run(self, query: str) -> str:
        return result
```

### LangChain Agent
```python
from langchain_classic.agents import create_openai_functions_agent, AgentExecutor
from langchain_classic import hub

# Agent 생성
prompt = hub.pull("hwchase17/openai-functions-agent")
agent = create_openai_functions_agent(llm, tools, prompt)

# AgentExecutor로 실행
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True
)

response = agent_executor.invoke({"input": "질문"})
```

## 🎓 학습 포인트

### Function Calling의 핵심
1. **Tool 정의**: 명확한 이름, 설명, 인자 스키마
2. **Tool 호출**: LLM이 적절한 도구 선택
3. **결과 처리**: 도구 실행 결과를 LLM에 전달
4. **반복**: 필요시 추가 도구 호출

### Agent Prompting 선택 기준
- **Plan-and-Execute**: 구조화된 문제, 명확한 단계
- **ReAct**: 탐색적 문제, 동적 상황
- **Self-Reflection**: 높은 정확도 요구, 시간 여유

### Custom Tool 작성 시 주의사항
1. **명확한 설명**: Agent가 도구를 언제 사용할지 판단
2. **인자 스키마**: Pydantic 모델로 타입 안전성 확보
3. **에러 처리**: 도구 실행 실패 시 적절한 피드백
4. **비동기 지원**: 필요시 `_arun()` 메서드 구현

## 🔗 참고 자료

- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)
- [LangChain Tools](https://python.langchain.com/docs/how_to/#tools)
- [LangChain Agents](https://python.langchain.com/docs/how_to/#agents)
- [Tavily Search](https://tavily.com/)

## 📊 실습 후 확인사항

- [ ] OpenAI Function Calling 기본 개념 이해
- [ ] Plan-and-Execute, ReAct, Self-Reflection 비교
- [ ] LangChain Tool과 Toolkit 차이 이해
- [ ] 4가지 방법으로 Custom Tool 작성
- [ ] Agent에 도구 연결 및 실행
- [ ] 도구 설명(description)의 중요성 이해

## 🎨 실전 프로젝트: 웹검색 통합 채팅 앱

이제 배운 내용을 실제 앱에 적용해봅니다!

### app4.py - 웹검색 통합 Streamlit 앱

**위치**: `complete/app4.py` (정답), `student/app4.py` (실습용)

**기능**:
- Tavily와 DuckDuckGo 웹 검색 통합
- 검색 결과를 LLM 프롬프트에 포함 (RAG 패턴)
- 세션별 검색 결과 저장
- 시스템 프롬프트 설정
- 다중 대화 세션 관리

**실습 빈칸 (10개)**:
1. Session State - conversations 초기화 (search_results, system_prompt 추가)
2. Session State - search_engine 초기화
3. TavilySearchResults 초기화 및 호출
4. DDGS 객체 생성 및 검색
5. 검색 결과 expander 표시
6. Tavily 버튼 토글 로직
7. DuckDuckGo 버튼 토글 로직
8. 검색 결과 저장
9. 검색 결과를 프롬프트에 포함
10. SystemMessage 추가

**실행 방법**:
```bash
# 정답 실행
cd complete
streamlit run app4.py

# 학생용 실습
cd student
streamlit run app4.py
```

**학습 포인트**:
- Tool 실전 적용
- RAG (Retrieval-Augmented Generation) 패턴
- 검색 결과 저장 및 표시
- 다중 도구 선택 UI

## 🔜 다음 단계

이 실습을 완료하면:
- **07. 웹검색 기반 LangChain 앱 만들기**에서 더 고급 RAG 패턴 학습
- **08. 문서기반 답변과 RAG**에서 벡터 DB와 임베딩 학습
- **09. LangGraph 기초**에서 더 복잡한 Agent 워크플로우 구현

이제 LLM의 한계를 넘어 외부 도구와 연동하는 방법을 마스터했습니다!


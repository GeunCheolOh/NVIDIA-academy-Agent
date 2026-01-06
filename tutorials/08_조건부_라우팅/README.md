# 08. 조건부 라우팅 (Conditional Routing)

LLM을 Router로 사용하여 질문 유형에 따라 최적의 처리 경로를 자동으로 선택하는 지능형 Agent를 구축합니다.

## 🎯 학습 목표

1. **Router LLM**: LLM을 의사결정 엔진으로 활용하는 방법
2. **조건부 엣지**: LangGraph에서 동적 그래프 흐름 제어
3. **다중 경로 시스템**: VectorDB, WebSearch, Direct LLM
4. **하이브리드 시스템**: 여러 데이터 소스를 통합한 스마트 챗봇

## 📂 폴더 구조

```
08_조건부_라우팅/
├── README.md                     # 이 파일
│
├── complete/                     # 정답 (완성 버전)
│   ├── setup_d2l.py             # D2L PDF 다운로드 및 벡터 스토어 구축
│   ├── rag_router_agent.py      # Router Agent (3가지 경로)
│   └── app_router.py            # Streamlit UI
│
└── student/                      # 학생용 (연습 버전)
    ├── setup_d2l.py             # 빈칸 2개
    ├── rag_router_agent.py      # 빈칸 6개
    ├── app_router.py            # 빈칸 2개
    ├── README_STUDENT.md        # 학생용 가이드
    ├── requirements.txt
    └── env.example
```

## 🧭 Router Agent 개요

### 3가지 경로

1. **📚 VectorDB 경로** (AI/ML 질문)
   - D2L (Dive into Deep Learning) 교재 검색
   - 예: "딥러닝에서 backpropagation이란?", "CNN 구조는?"

2. **🌐 WebSearch 경로** (최신 정보)
   - Tavily를 통한 웹 검색
   - 예: "2024년 노벨상 수상자는?", "오늘 날씨는?"

3. **💬 Direct LLM 경로** (일반 대화)
   - LLM 직접 응답
   - 예: "안녕하세요!", "Python 코드 작성해줘"

### 작동 원리

```
사용자 질문
    ↓
┌────────────────────┐
│   Router Node      │  ← LLM이 질문 유형 분석
│   (LLM 판단)       │     & 최적 경로 선택
└────────────────────┘
    ↓    ↓    ↓
┌────┐ ┌────┐ ┌────┐
│Vec │ │Web │ │Dire│
│torD│ │Sear│ │ct  │
│B   │ │ch  │ │LLM │
└────┘ └────┘ └────┘
    ↓    ↓      ↓
┌────────────────────┐
│   Answer Node      │
│   (최종 답변 생성) │
└────────────────────┘
```

## 🚀 사용 방법

### 1. 환경 변수 설정

프로젝트 루트의 `.env` 파일에 추가:

```bash
OPENAI_API_KEY=your-api-key
TAVILY_API_KEY=your-tavily-key
```

### 2. 패키지 설치

```bash
cd complete
pip install -r requirements.txt
```

### 3. D2L 교재 설정 (최초 1회)

```bash
python setup_d2l.py
```

이 명령은:
- D2L PDF 다운로드 (약 44MB)
- 벡터 스토어 구축 (처음 100페이지, 276개 청크)
- 약 5-10분 소요
- `./chroma_db_d2l` 폴더 생성

### 4. 애플리케이션 실행

```bash
streamlit run app_router.py
```

## 📊 주요 기능

### Router Agent (rag_router_agent.py)

**핵심 클래스**: `RouterAgent`

**주요 메서드**:
- `_router_node()`: LLM이 경로 결정 (JSON 응답 파싱)
- `_vectordb_node()`: D2L 교재 검색
- `_websearch_node()`: Tavily 웹 검색
- `_direct_llm_node()`: LLM 직접 응답
- `_answer_node()`: 검색 결과 기반 최종 답변 생성
- `_route_question()`: 조건부 엣지의 라우팅 함수

**LangGraph 구조**:
```python
workflow.add_conditional_edges(
    "router",
    route_question,  # 라우팅 함수
    {
        "vectordb": "vectordb",
        "websearch": "websearch",
        "direct": "direct_llm"
    }
)
```

### Streamlit UI (app_router.py)

**주요 기능**:
- D2L 벡터 스토어 자동 로드 (`@st.cache_resource`)
- 다중 대화 세션 관리 (UUID 기반)
- 라우팅 과정 실시간 시각화 (`st.status`)
- 각 답변의 라우팅 정보 표시 (expander)

## 🎓 핵심 학습 포인트

### 1. LLM as Router

**개념**: LLM을 의사결정 엔진으로 활용

```python
router_prompt = """
질문: {question}

선택지:
1. vectordb: AI/ML 질문 → D2L 교재
2. websearch: 최신 정보 → 웹 검색
3. direct: 일반 대화 → LLM 직접

JSON 응답: {"route": "...", "reasoning": "..."}
"""

response = llm.invoke([SystemMessage(content=router_prompt)])
result = json.loads(response.content)
```

### 2. 조건부 엣지 (Conditional Edges)

**개념**: 상태에 따라 다음 노드를 동적으로 결정

```python
def route_question(state: AgentState) -> str:
    return state["route"]  # "vectordb", "websearch", "direct" 중 하나

workflow.add_conditional_edges(
    source="router",
    path=route_question,
    path_map={
        "vectordb": "vectordb",
        "websearch": "websearch",
        "direct": "direct_llm"
    }
)
```

### 3. 하이브리드 시스템의 장점

| 항목 | 단일 경로 | Router (하이브리드) |
|------|----------|-------------------|
| 정확도 | 보통 | **높음** ✅ |
| 비용 | 높음 | **최적화** ✅ |
| 속도 | 느림 | **빠름** ✅ |
| 유연성 | 낮음 | **높음** ✅ |

**이유**:
- **정확성**: 전문 지식은 VectorDB에서
- **최신성**: 실시간 정보는 WebSearch에서
- **유연성**: 일반 질문은 LLM 직접 처리
- **비용 효율**: 필요한 경우에만 검색 수행

## 🧪 테스트 예제

### VectorDB 경로 (AI/ML 질문)

```
Q: "딥러닝에서 backpropagation이란 무엇인가요?"
→ Router: vectordb
→ D2L 교재 검색
→ Answer: 교재 기반 상세 설명
```

### WebSearch 경로 (최신 정보)

```
Q: "2024년 AI 관련 최신 뉴스는?"
→ Router: websearch
→ Tavily 웹 검색
→ Answer: 최신 뉴스 요약
```

### Direct LLM 경로 (일반 대화)

```
Q: "안녕하세요! Python으로 피보나치 수열을 구하는 코드를 작성해주세요"
→ Router: direct
→ LLM 직접 응답
→ Answer: 코드 생성
```

## 🔗 참고 자료

- **레퍼런스**: `reference/5_1_3_LangGraph_RAG_Agent.ipynb`
- **D2L 교재**: https://d2l.ai/
- **LangGraph 문서**: https://langchain-ai.github.io/langgraph/
- **Tavily API**: https://tavily.com/

## 📝 학생용 과제

`student` 폴더에서:
- 총 10개의 빈칸 (`# YOUR CODE HERE`)
- `README_STUDENT.md`에 자세한 힌트 제공

## 💡 Troubleshooting

### D2L 벡터 스토어가 없음
```
❌ D2L 벡터 스토어가 없습니다!
```
→ `python setup_d2l.py` 실행

### Tavily API 키 오류
```
❌ 웹 검색 실패: API key not found
```
→ `.env`에 `TAVILY_API_KEY` 추가

### Router 오류
```
⚠️ Router 오류: ..., 기본 경로 사용
```
→ JSON 파싱 실패, LLM 응답 확인

## 🎉 다음 단계

1. ✅ **완료**: 조건부 라우팅 구현
2. ⏳ **다음**: LangGraph 고급 기능 (9번)
3. ⏳ **최종**: 종합 프로젝트 (10번)

화이팅!


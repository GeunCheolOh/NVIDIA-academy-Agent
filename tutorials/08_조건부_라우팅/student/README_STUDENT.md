# 🧭 조건부 라우팅 (Conditional Routing) - 학생용

LLM을 Router로 사용하여 질문 유형에 따라 다른 처리 경로로 분기하는 지능형 Agent를 구축합니다.

## 🎯 학습 목표

1. **Router LLM**: LLM을 의사결정자로 활용
2. **조건부 엣지**: LangGraph에서 동적 그래프 흐름 제어
3. **다중 경로**: VectorDB, WebSearch, Direct LLM
4. **하이브리드 시스템**: 여러 데이터 소스 통합

## 📂 파일 구조

```
student/
├── setup_d2l.py              # D2L PDF 다운로드 및 벡터 스토어 (빈칸 2개)
├── rag_router_agent.py        # Router Agent (빈칸 6개)
├── app_router.py              # Streamlit UI (빈칸 2개)
├── README_STUDENT.md          # 이 파일
├── requirements.txt
└── env.example
```

## 🚀 설정 방법

### 1. 환경 변수 설정

```bash
# 프로젝트 루트의 .env 파일에 추가
OPENAI_API_KEY=your-api-key
TAVILY_API_KEY=your-tavily-key
```

### 2. 패키지 설치

```bash
pip install -r requirements.txt
```

### 3. D2L 교재 설정

```bash
python setup_d2l.py
```

이 명령은:
- D2L PDF 다운로드 (https://d2l.ai/d2l-en.pdf)
- 벡터 스토어 구축 (./chroma_db_d2l)
- 약 5-10분 소요

### 4. 애플리케이션 실행

```bash
streamlit run app_router.py
```

## ✏️ 빈칸 채우기 가이드

### setup_d2l.py (2개 빈칸)

#### 빈칸 1: PDF 다운로드
```python
response = requests.get(url, stream=True)
response.raise_for_status()
```
**힌트**: `requests.get()`으로 PDF를 스트리밍 다운로드

#### 빈칸 2: 벡터 스토어 생성
```python
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory=chroma_path
)
```
**힌트**: `Chroma.from_documents()`로 벡터 스토어 구축

### rag_router_agent.py (6개 빈칸)

#### 빈칸 1: Router Node - LLM 호출 및 JSON 파싱
```python
response = self.llm.invoke([SystemMessage(content=router_prompt)])
result = json.loads(response.content)

route = result.get("route", "direct")
reasoning = result.get("reasoning", "기본 경로 선택")
```
**힌트**: LLM에게 라우팅 결정을 요청하고 JSON 응답 파싱

#### 빈칸 2: VectorDB Node - 문서 검색
```python
docs = self.d2l_retriever.invoke(question)
```
**힌트**: D2L 교재 검색기로 관련 문서 검색

#### 빈칸 3: WebSearch Node - 웹 검색
```python
search_results = self.tavily_tool.invoke(question)
```
**힌트**: Tavily API로 웹 검색 수행

#### 빈칸 4: Direct LLM Node - LLM 직접 응답
```python
conversation = messages + [HumanMessage(content=question)]
response = self.llm.invoke(conversation)
```
**힌트**: 대화 이력을 포함하여 LLM에 직접 질문

#### 빈칸 5: Answer Node - 최종 답변 생성
```python
response = self.llm.invoke([SystemMessage(content=answer_prompt)])
```
**힌트**: 검색 결과를 바탕으로 최종 답변 생성

#### 빈칸 6: 라우팅 함수
```python
return state["route"]
```
**힌트**: router_node에서 결정한 경로 반환

### app_router.py (2개 빈칸)

#### 빈칸 1: Router Agent 초기화
```python
if "router_agent" not in st.session_state:
    retriever = st.session_state.vectorstore.as_retriever(
        search_kwargs={"k": 3}
    )
    st.session_state.router_agent = RouterAgent(
        d2l_retriever=retriever,
        api_key=os.getenv("OPENAI_API_KEY"),
        tavily_api_key=os.getenv("TAVILY_API_KEY")
    )
```
**힌트**: D2L 검색기와 API 키로 RouterAgent 생성

#### 빈칸 2: Router Agent 호출
```python
result = st.session_state.router_agent.invoke(
    question=prompt,
    chat_history=chat_history
)
```
**힌트**: 질문과 대화 이력을 전달하여 Agent 실행

## 🧪 테스트 방법

### 1. 모듈별 테스트

```bash
# Router Agent 테스트
python3 -c "from rag_router_agent import RouterAgent; print('✅ OK')"
```

### 2. 전체 앱 실행

```bash
streamlit run app_router.py
```

### 3. 경로별 테스트

**VectorDB 경로** (AI/ML 질문):
- "딥러닝에서 backpropagation이란?"
- "CNN의 구조를 설명해주세요"

**WebSearch 경로** (최신 정보):
- "2024년 노벨상 수상자는?"
- "오늘 날씨 어때?"

**Direct LLM 경로** (일반 대화):
- "안녕하세요!"
- "Python 코드 작성해줘"

## 🏗️ 아키텍처

```
사용자 질문
    ↓
┌─────────────────────┐
│   Router Node       │
│   (LLM이 경로 결정) │
└─────────────────────┘
    ↓    ↓    ↓
┌────┐ ┌────┐ ┌────┐
│Vec │ │Web │ │Dire│
│torD│ │Sear│ │ct  │
│B   │ │ch  │ │LLM │
└────┘ └────┘ └────┘
    ↓    ↓      ↓
┌─────────────────────┐
│   Answer Node       │
│   (최종 답변 생성)   │
└─────────────────────┘
```

## 📝 체크리스트

- [ ] setup_d2l.py의 2개 빈칸 완성
- [ ] rag_router_agent.py의 6개 빈칸 완성
- [ ] app_router.py의 2개 빈칸 완성
- [ ] D2L 벡터 스토어 구축 완료
- [ ] 모듈별 import 테스트 통과
- [ ] VectorDB 경로 테스트 성공
- [ ] WebSearch 경로 테스트 성공
- [ ] Direct LLM 경로 테스트 성공
- [ ] 라우팅 정보 시각화 확인

## 💡 디버깅 팁

### Router 오류
```
⚠️ Router 오류: ..., 기본 경로 사용
```
- JSON 파싱 실패 → LLM 응답 확인
- 라우팅 로직 검증

### VectorDB 검색 실패
```
❌ VectorDB 검색 실패: ...
```
- D2L 벡터 스토어 확인 (`setup_d2l.py` 실행)
- retriever 초기화 확인

### WebSearch 오류
```
❌ 웹 검색 실패: ...
```
- Tavily API 키 확인
- 네트워크 연결 확인

## 🎓 학습 포인트

### LLM as Router

**개념**: LLM을 의사결정 엔진으로 활용

```python
# LLM에게 질문 유형 분석 요청
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

### 조건부 엣지 (Conditional Edges)

**개념**: 상태에 따라 다음 노드를 동적으로 결정

```python
workflow.add_conditional_edges(
    "router",
    route_question,  # 라우팅 함수
    {
        "vectordb": "vectordb",    # route가 "vectordb"면 vectordb 노드로
        "websearch": "websearch",  # route가 "websearch"면 websearch 노드로
        "direct": "direct_llm"     # route가 "direct"면 direct_llm 노드로
    }
)
```

### 하이브리드 시스템

**장점**:
- 정확성: 전문 지식은 VectorDB에서
- 최신성: 실시간 정보는 WebSearch에서
- 유연성: 일반 질문은 LLM 직접 처리

**vs 단일 경로**:
| 항목 | 하이브리드 | 단일 경로 |
|------|-----------|----------|
| 정확도 | 높음 | 보통 |
| 비용 | 최적화 | 높음 |
| 속도 | 빠름 | 느림 |
| 유연성 | 높음 | 낮음 |

## 🔗 참고 자료

- **완성 코드**: `../complete/` 폴더
- **레퍼런스**: `reference/5_1_3_LangGraph_RAG_Agent.ipynb`
- **LangGraph 문서**: https://langchain-ai.github.io/langgraph/

## 📞 도움이 필요하면

1. 완성 코드와 비교 (`../complete/` 폴더)
2. 레퍼런스 노트북 참고
3. 주석의 힌트 확인

화이팅! 🚀


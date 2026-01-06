# 📚 RAG 채팅 애플리케이션

PDF 문서를 업로드하고 문서 내용을 기반으로 대화할 수 있는 지능형 채팅 애플리케이션입니다.

## 🏗️ 아키텍처

### 파일 구조

```
07_문서기반_답변과_RAG/
├── app_rag.py              # Streamlit 프론트엔드 (메인 애플리케이션)
├── rag_processor.py        # PDF 전처리 (로딩, 청킹, 임베딩, 벡터 스토어)
├── rag_agent.py            # LangGraph 기반 RAG Agent (ReAct 패턴)
└── README_RAG_APP.md       # 이 파일
```

### 시스템 구성도

```
┌─────────────────────────────────────────────────────────────────┐
│                         app_rag.py                              │
│                   (Streamlit 프론트엔드)                        │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  PDF 업로드  →  진행 상황 표시  →  채팅 인터페이스      │  │
│  └──────────────────────────────────────────────────────────┘  │
│                           ↓                ↓                    │
│              ┌─────────────────┐   ┌──────────────────┐        │
│              │ rag_processor.py│   │  rag_agent.py    │        │
│              │   (전처리)      │   │  (RAG Agent)     │        │
│              └─────────────────┘   └──────────────────┘        │
└─────────────────────────────────────────────────────────────────┘

            ↓                              ↓
    
┌─────────────────────┐          ┌───────────────────────┐
│   PDF 파일          │          │   LangGraph Agent     │
│   ↓                 │          │   ┌─────────────┐     │
│   PyMuPDFLoader     │          │   │  Thought    │     │
│   ↓                 │          │   │     ↓       │     │
│   RecursiveCharacter│          │   │  Action     │     │
│   TextSplitter      │          │   │     ↓       │     │
│   ↓                 │          │   │ Observation │     │
│   OpenAIEmbeddings  │          │   └─────────────┘     │
│   ↓                 │          │                       │
│   Chroma VectorStore│←─────────│  검색기 (Retriever)   │
└─────────────────────┘          └───────────────────────┘
```

## 🎯 주요 기능

### 1. PDF 업로드 및 실시간 처리 진행 상황 표시

**파일**: `app_rag.py` + `rag_processor.py`

```python
# 진행 상황 구조
{
    "status": "진행중" | "완료" | "실패",
    "current_step": "현재 단계 이름",
    "steps": {
        "load": {"message": "✅ 5개의 페이지를 로드했습니다.", "success": True},
        "chunk": {"message": "✅ 23개의 청크로 분할했습니다.", "success": True},
        "embed": {"message": "✅ 23개의 벡터를 생성했습니다.", "success": True}
    },
    "file_info": {
        "name": "document.pdf",
        "size": 1048576,
        "pages": 5,
        "chunks": 23
    }
}
```

**사용 기술**:
- `st.status()`: 진행 상황을 접을 수 있는 컨테이너로 표시
- `st.file_uploader()`: PDF 파일 업로드
- 단계별 상태 업데이트 및 표시

### 2. 다중 세션 관리 (app2.py 기반)

**파일**: `app_rag.py`

- UUID 기반 고유 대화 세션
- 여러 대화 동시 관리
- 대화 전환 및 삭제
- 각 세션별 독립적인 히스토리

```python
conversations = {
    "uuid-1": {
        "id": "uuid-1",
        "title": "첫 번째 질문...",
        "messages": [...],
        "created_at": datetime.now()
    },
    "uuid-2": { ... }
}
```

### 3. LangGraph 기반 RAG Agent

**파일**: `rag_agent.py`

**ReAct 패턴** (Reasoning + Acting):

```
1. Thought (생각): 
   - 검색이 필요한가?
   - 어떤 정보가 필요한가?

2. Action (행동):
   - 벡터 스토어에서 관련 문서 검색
   - 상위 5개 문서 추출

3. Observation (관찰):
   - 검색 결과가 충분한가?
   - 부족하면 재시도 (최대 3회)
   - 충분하면 답변 생성
```

**상태 그래프**:

```python
workflow = StateGraph(AgentState)

workflow.add_node("thought", thought_node)
workflow.add_node("action", action_node)
workflow.add_node("observation", observation_node)

workflow.set_entry_point("thought")
workflow.add_edge("thought", "action")
workflow.add_edge("action", "observation")
workflow.add_conditional_edges(
    "observation",
    should_continue,
    {"continue": "thought", "end": END}
)
```

### 4. PDF 전처리 파이프라인

**파일**: `rag_processor.py`

**전체 파이프라인**:

```
PDF 파일
   ↓
PyMuPDFLoader (로딩)
   ↓
List[Document] (페이지 단위)
   ↓
RecursiveCharacterTextSplitter (청킹)
   - chunk_size: 800
   - chunk_overlap: 200
   ↓
List[Document] (청크 단위)
   ↓
OpenAIEmbeddings (임베딩)
   - model: text-embedding-3-small
   ↓
Chroma VectorStore (저장)
   ↓
Retriever (검색기 생성)
   - search_type: similarity
   - k: 5
```

**클래스 구조**:

```python
class RAGProcessor:
    def load_pdf(file_path) → (docs, message)
    def split_documents(docs) → (chunks, message)
    def create_vectorstore(chunks) → (vectorstore, message)
    def process_pdf_file(uploaded_file) → (vectorstore, progress)
    def get_retriever(vectorstore) → retriever
```

## 🚀 실행 방법

### 1. 필요 패키지 설치

```bash
cd tutorials/07_문서기반_답변과_RAG

# 필요 패키지 설치
pip install streamlit langchain-openai langchain-core \
            langchain-community langchain-text-splitters \
            langgraph chromadb pymupdf python-dotenv
```

### 2. API 키 설정

프로젝트 루트의 `.env` 파일에 추가:

```bash
OPENAI_API_KEY=your-api-key-here
```

### 3. 애플리케이션 실행

```bash
streamlit run app_rag.py
```

### 4. 브라우저 접속

- 로컬: http://localhost:8502
- 네트워크: http://192.168.x.x:8502

## 📖 사용 방법

### Step 1: PDF 업로드

1. 상단의 "PDF 문서 업로드" 섹션에서 **파일 선택**
2. PDF 파일 선택 (예: 논문, 보고서, 교재 등)
3. "🚀 문서 처리 시작" 버튼 클릭

### Step 2: 처리 진행 상황 확인

실시간으로 진행 상황이 표시됩니다:

```
📄 PDF 처리 중...
✅ 15개의 페이지를 로드했습니다.
✅ 58개의 청크로 분할했습니다. (평균 750자)
✅ 58개의 벡터를 생성하고 저장했습니다.

✅ PDF 처리 완료!
```

### Step 3: 대화 시작

처리가 완료되면:

1. 하단 채팅 입력창에 질문 입력
2. RAG Agent가 문서를 검색하고 답변 생성
3. "🔍 검색 정보" 영역에서 검색된 문서 확인 가능

### Step 4: 다중 대화 관리

- **새 대화**: 우측 상단 "➕ 새 대화" 버튼
- **대화 전환**: 좌측 사이드바에서 대화 선택
- **대화 삭제**: 각 대화 옆 "🗑️" 버튼

## 💡 코드 하이라이트

### 1. PDF 전처리 (rag_processor.py)

```python
def process_pdf_file(self, uploaded_file, persist_directory=None):
    """
    업로드된 PDF 파일을 전체 파이프라인으로 처리
    
    반환값:
        (vectorstore, progress_dict)
    """
    # 1. 임시 파일로 저장
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_path = tmp_file.name
    
    # 2. PDF 로딩
    documents, load_msg = self.load_pdf(tmp_path)
    
    # 3. 청킹
    chunks, chunk_msg = self.split_documents(documents)
    
    # 4. 벡터 스토어 생성
    vectorstore, embed_msg = self.create_vectorstore(chunks, persist_directory)
    
    return vectorstore, progress
```

### 2. RAG Agent (rag_agent.py)

```python
def _observation_node(self, state: AgentState) -> dict:
    """검색 결과를 평가하고 답변을 생성"""
    
    # 1단계: 검색 결과 평가
    eval_response = self.llm.invoke([SystemMessage(content=eval_prompt)])
    is_relevant = eval_result.get("is_relevant", False)
    
    # 2단계: 부족하면 재시도
    if not is_relevant and iteration < self.max_iterations:
        return {"is_relevant": False}
    
    # 3단계: 최종 답변 생성
    response = self.llm.invoke([SystemMessage(content=answer_prompt)])
    
    return {
        "is_relevant": True,
        "final_answer": response.content,
        "messages": [HumanMessage(...), AIMessage(...)]
    }
```

### 3. Streamlit 프론트엔드 (app_rag.py)

```python
# PDF 처리
with st.status("PDF 처리 중...", expanded=True) as status:
    vectorstore, progress = st.session_state.processor.process_pdf_file(
        uploaded_file
    )
    
    # 단계별 진행 상황 표시
    for step_name, step_info in progress["steps"].items():
        st.write(step_info["message"])
    
    if progress["status"] == "완료":
        status.update(label="✅ PDF 처리 완료!", state="complete")
        
        # RAG Agent 초기화
        retriever = processor.get_retriever(vectorstore, k=5)
        st.session_state.rag_agent = RAGAgent(retriever, api_key)
```

## 🔍 주요 API 정리

### Streamlit UI

| API | 용도 | 예제 |
|-----|------|------|
| `st.file_uploader()` | 파일 업로드 | `uploaded_file = st.file_uploader("PDF", type=["pdf"])` |
| `st.status()` | 진행 상황 표시 | `with st.status("처리 중...") as status:` |
| `st.columns()` | 레이아웃 분할 | `col1, col2 = st.columns([6, 1])` |
| `st.chat_message()` | 채팅 메시지 | `with st.chat_message("user"):` |
| `st.chat_input()` | 채팅 입력 | `if prompt := st.chat_input("질문"):` |
| `st.expander()` | 접을 수 있는 영역 | `with st.expander("검색 정보"):` |

### LangChain/LangGraph

| API | 용도 | 파일 |
|-----|------|------|
| `PyMuPDFLoader` | PDF 로딩 | rag_processor.py |
| `RecursiveCharacterTextSplitter` | 텍스트 청킹 | rag_processor.py |
| `OpenAIEmbeddings` | 임베딩 생성 | rag_processor.py |
| `Chroma` | 벡터 스토어 | rag_processor.py |
| `StateGraph` | 상태 그래프 | rag_agent.py |
| `ChatOpenAI` | LLM | rag_agent.py |

## 🎓 학습 포인트

### 1. 모듈화된 아키텍처

**장점**:
- 각 모듈이 독립적으로 테스트 가능
- 코드 재사용성 향상
- 유지보수 용이

**구조**:
```
app_rag.py (UI)
    ↓
rag_processor.py (전처리)
    ↓
rag_agent.py (Agent)
```

### 2. 진행 상황 추적

**중요성**:
- 사용자 경험 향상
- 오류 발생 시 어느 단계에서 문제인지 파악 가능
- 처리 시간이 긴 작업에 필수

**구현**:
```python
progress = {
    "status": "진행중",
    "current_step": "청킹",
    "steps": {
        "load": {"message": "...", "success": True},
        "chunk": {"message": "...", "success": True}
    }
}
```

### 3. ReAct 패턴

**개념**:
- Reasoning (추론) + Acting (행동)
- Agent가 생각하고 행동하고 관찰하는 반복적 과정

**구현**:
```
Thought → Action → Observation
   ↑                    ↓
   └────── (재시도) ─────┘
```

### 4. 벡터 검색

**원리**:
1. 질문을 임베딩으로 변환
2. 벡터 스토어에서 유사도 계산
3. 가장 유사한 문서 k개 반환

**코드**:
```python
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 5}
)

docs = retriever.invoke("질문")
```

## 🐛 문제 해결

### 문제 1: ModuleNotFoundError

```bash
ModuleNotFoundError: No module named 'langchain_text_splitters'
```

**해결책**:
```bash
pip install langchain-text-splitters
```

### 문제 2: 벡터 스토어 생성 실패

```
❌ 벡터 스토어 생성 실패: ...
```

**원인**:
- API 키 누락
- 청크가 비어있음
- 메모리 부족

**해결책**:
1. `.env` 파일에 `OPENAI_API_KEY` 확인
2. PDF 파일이 텍스트를 포함하는지 확인
3. chunk_size 줄이기

### 문제 3: Agent 응답 느림

**원인**:
- PDF가 너무 큼
- 검색 결과가 많음
- 재시도 횟수가 많음

**해결책**:
```python
# k 값 줄이기
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# 최대 반복 횟수 줄이기
agent = RAGAgent(retriever, max_iterations=2)

# chunk_size 늘리기
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1200)
```

## 🔜 향후 개선 방향

1. **하이브리드 검색**: VectorDB + 웹검색 결합
2. **Re-ranking**: 검색 결과 재정렬로 정확도 향상
3. **인용 표시**: 답변의 출처 페이지 번호 표시
4. **다중 문서**: 여러 PDF를 동시에 검색
5. **벡터 스토어 영구 저장**: 재업로드 없이 이전 문서 사용

## 📊 성능 최적화 팁

### 청킹 전략

```python
# 작은 문서 (논문, 기사)
chunk_size=500, chunk_overlap=100

# 중간 크기 (보고서, 교재)
chunk_size=800, chunk_overlap=200  # 기본값

# 큰 문서 (책, 매뉴얼)
chunk_size=1200, chunk_overlap=300
```

### 검색 개수

```python
# 빠른 응답 (간단한 질문)
k=3

# 균형 (기본)
k=5

# 높은 정확도 (복잡한 질문)
k=10
```

### LLM 모델 선택

```python
# 빠르고 저렴
model="gpt-4.1-nano-2025-04-14"

# 균형
model="gpt-4.1-mini-2025-04-14"

# 높은 품질
model="gpt-5-mini-2025-08-07"
```

---

이제 PDF 문서를 업로드하고 대화를 시작해보세요! 🚀


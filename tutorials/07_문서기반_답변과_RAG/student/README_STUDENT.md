# 📚 RAG 채팅 애플리케이션 - 학생용

PDF 문서를 업로드하고 문서 내용을 기반으로 대화하는 RAG 시스템을 구축합니다.

## 🎯 학습 목표

1. **PDF 전처리** (`rag_processor.py`)
   - PDF 로딩 (PyMuPDFLoader)
   - 텍스트 청킹 (RecursiveCharacterTextSplitter)
   - 임베딩 생성 (OpenAIEmbeddings)
   - 벡터 스토어 구축 (Chroma)

2. **LangGraph RAG Agent** (`rag_agent.py`)
   - StateGraph 구성
   - ReAct 패턴 (Thought-Action-Observation)
   - 문서 검색 (Retriever)
   - 검색 결과 평가 및 재시도

3. **Streamlit UI** (`app_rag.py`)
   - PDF 업로드 인터페이스
   - 실시간 진행 상황 표시
   - 다중 세션 관리
   - RAG Agent 통합

## 📂 파일 구조

```
student/
├── rag_processor.py    # PDF 전처리 모듈 (빈칸 5개)
├── rag_agent.py         # LangGraph RAG Agent (빈칸 6개)
├── app_rag.py           # Streamlit UI (빈칸 4개)
├── README_STUDENT.md    # 이 파일
├── requirements.txt     # 필요 패키지
└── env.example          # 환경 변수 예제
```

## 🚀 설정 방법

### 1. 환경 변수 설정

```bash
# .env 파일 생성
cp env.example ../../.env

# OpenAI API 키 입력
# OPENAI_API_KEY=your-api-key-here
```

### 2. 패키지 설치

```bash
pip install -r requirements.txt
```

### 3. 애플리케이션 실행

```bash
streamlit run app_rag.py
```

## ✏️ 빈칸 채우기 가이드

### rag_processor.py (5개 빈칸)

#### 빈칸 1: OpenAIEmbeddings 초기화
```python
self.embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    api_key=api_key
)
```
**힌트**: 텍스트를 숫자 벡터로 변환하는 임베딩 모델을 초기화합니다.

#### 빈칸 2: RecursiveCharacterTextSplitter 초기화
```python
self.text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=200,
    length_function=len,
    separators=["\n\n", "\n", " ", ""]
)
```
**힌트**: 문서를 800자 크기의 청크로 분할하며, 200자씩 중복됩니다.

#### 빈칸 3: PyMuPDFLoader로 PDF 로딩
```python
loader = PyMuPDFLoader(file_path)
documents = loader.load()
```
**힌트**: PDF의 각 페이지를 Document 객체로 변환합니다.

#### 빈칸 4: text_splitter로 문서 분할
```python
chunks = self.text_splitter.split_documents(documents)
```
**힌트**: Document 리스트를 작은 청크로 분할합니다.

#### 빈칸 5: Chroma 벡터 스토어 생성
```python
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=self.embeddings,
    persist_directory=persist_directory
)
```
**힌트**: 청크를 임베딩하고 벡터 스토어에 저장합니다.

### rag_agent.py (6개 빈칸)

#### 빈칸 1: ChatOpenAI LLM 초기화
```python
self.llm = ChatOpenAI(
    model=model,
    temperature=0.3,
    api_key=api_key
)
```
**힌트**: OpenAI LLM을 초기화합니다. temperature가 낮을수록 일관적입니다.

#### 빈칸 2: retriever로 관련 문서 검색
```python
docs = self.retriever.invoke(question)
```
**힌트**: 질문과 유사한 문서를 벡터 스토어에서 검색합니다.

#### 빈칸 3: LLM으로 검색 결과 평가
```python
eval_response = self.llm.invoke([SystemMessage(content=eval_prompt)])
eval_result = json.loads(eval_response.content)
is_relevant = eval_result.get("is_relevant", False)
```
**힌트**: LLM에게 검색 결과가 충분한지 평가를 요청합니다.

#### 빈칸 4: LLM으로 최종 답변 생성
```python
response = self.llm.invoke([SystemMessage(content=answer_prompt)])
answer = response.content
```
**힌트**: 검색된 문서를 기반으로 질문에 대한 답변을 생성합니다.

#### 빈칸 5: 초기 상태 설정
```python
initial_state = {
    "messages": chat_history or [],
    "question": question,
    "search_results": "",
    "is_relevant": False,
    "iteration": 0,
    "final_answer": ""
}
```
**힌트**: Agent가 시작할 때의 초기 상태를 설정합니다.

#### 빈칸 6: Agent 실행
```python
result = self.agent.invoke(initial_state)
```
**힌트**: 상태 그래프를 실행하여 답변을 생성합니다.

### app_rag.py (4개 빈칸)

#### 빈칸 1: RAGProcessor 초기화
```python
if st.session_state.processor is None:
    st.session_state.processor = RAGProcessor(
        api_key=os.getenv("OPENAI_API_KEY")
    )
```
**힌트**: PDF 전처리를 담당하는 Processor를 초기화합니다.

#### 빈칸 2: st.status로 진행 상황 표시
```python
with st.status("PDF 처리 중...", expanded=True) as status:
    vectorstore, progress = st.session_state.processor.process_pdf_file(
        uploaded_file
    )
```
**힌트**: 진행 상황을 접을 수 있는 컨테이너로 표시합니다.

#### 빈칸 3: RAG Agent 초기화
```python
retriever = st.session_state.processor.get_retriever(vectorstore, k=5)
st.session_state.rag_agent = RAGAgent(
    retriever=retriever,
    api_key=os.getenv("OPENAI_API_KEY"),
    max_iterations=3
)
```
**힌트**: 검색기를 생성하고 RAG Agent를 초기화합니다.

#### 빈칸 4: RAG Agent 호출
```python
result = st.session_state.rag_agent.invoke(
    question=prompt,
    chat_history=chat_history
)

answer = result["answer"]
iterations = result["iterations"]
```
**힌트**: Agent를 호출하여 답변을 생성합니다.

## 🧪 테스트 방법

### 1. 모듈별 테스트

```bash
# RAGProcessor 테스트
python3 -c "from rag_processor import RAGProcessor; print('✅ OK')"

# RAGAgent 테스트
python3 -c "from rag_agent import RAGAgent; print('✅ OK')"
```

### 2. 전체 앱 실행

```bash
streamlit run app_rag.py
```

### 3. PDF 업로드 및 테스트

1. 브라우저에서 http://localhost:8502 접속
2. PDF 파일 업로드
3. "문서 처리 시작" 버튼 클릭
4. 진행 상황 확인
5. 문서에 대해 질문하기

## 📝 체크리스트

- [ ] `rag_processor.py`의 5개 빈칸 완성
- [ ] `rag_agent.py`의 6개 빈칸 완성
- [ ] `app_rag.py`의 4개 빈칸 완성
- [ ] 모듈별 import 테스트 통과
- [ ] PDF 업로드 및 처리 성공
- [ ] 문서 기반 질의응답 작동
- [ ] 다중 세션 관리 확인

## 💡 디버깅 팁

### import 오류
```bash
# 패키지 재설치
pip install -r requirements.txt --upgrade
```

### PDF 로딩 실패
- PDF 파일이 텍스트를 포함하는지 확인
- 파일 크기가 너무 크지 않은지 확인 (<10MB 권장)

### 벡터 스토어 생성 실패
- API 키가 올바른지 확인
- 네트워크 연결 확인

### Agent 응답 느림
- chunk_size 늘리기 (800 → 1200)
- k 값 줄이기 (5 → 3)
- max_iterations 줄이기 (3 → 2)

## 🎓 학습 포인트

### RAG 파이프라인
```
PDF → 로딩 → 청킹 → 임베딩 → 벡터 스토어 → 검색 → 답변 생성
```

### ReAct 패턴
```
Thought (생각): 무엇을 해야 하나?
   ↓
Action (행동): 문서 검색
   ↓
Observation (관찰): 결과 평가
   ↓
재시도 or 답변 생성
```

### LangGraph 구조
```
StateGraph
├── thought_node (생각)
├── action_node (행동)
└── observation_node (관찰)
     ↓
조건부 엣지 → continue or end
```

## 🔗 참고 자료

- **완성 코드**: `../complete/` 폴더
- **전체 README**: `../README_RAG_APP.md`
- **단원 README**: `../README.md`

## 📞 도움이 필요하면

1. 완성 코드와 비교 (`../complete/` 폴더)
2. README_RAG_APP.md의 "문제 해결" 섹션 참고
3. 주석의 힌트 확인

화이팅! 🚀


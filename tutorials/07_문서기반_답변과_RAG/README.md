# 07. 문서기반 답변과 RAG (Retrieval-Augmented Generation)

문서를 기반으로 정확한 답변을 생성하는 RAG 시스템을 구축합니다.

## 📚 학습 내용

### 07_1. LangChain RAG 기초
- PDF 문서 로딩 및 전처리
- 텍스트 청킹 (Chunking)
- 임베딩 (Embedding) 생성
- 벡터 스토어 (Vector Store) 구축
- 검색기 (Retriever) 생성
- RAG 체인 구성 (LCEL & RetrievalQA)

### 07_2. RAG Tool 만들기
- 웹에서 PDF 직접 로딩
- FAISS 벡터 스토어 사용
- `create_retriever_tool`로 RAG Tool 생성
- Agent에 RAG Tool + 웹검색 Tool 통합
- 다양한 질문 유형 테스트

### 07_3. LangGraph RAG Agent
- LangGraph 기반 고급 RAG
- ReAct 패턴 (Thought-Action-Observation)
- VectorDB + 웹검색 하이브리드
- 검색 결과 평가 및 재시도
- 대화 컨텍스트 유지

## 🎯 핵심 개념

### RAG란?
**Retrieval-Augmented Generation**은 외부 지식(문서)을 검색하여 LLM의 답변을 보강하는 기법입니다.

```
사용자 질문
    ↓
문서 검색 (Retrieval)
    ↓
관련 문서 추출
    ↓
문서 + 질문 → LLM
    ↓
정확한 답변 생성
```

### RAG vs Fine-tuning

| 항목 | RAG | Fine-tuning |
|------|-----|-------------|
| 지식 업데이트 | 쉬움 (문서만 교체) | 어려움 (재학습 필요) |
| 비용 | 낮음 | 높음 |
| 출처 추적 | 가능 | 불가능 |
| 정확도 | 높음 | 보통 |

### RAG 파이프라인

#### 1. 인덱싱 (Indexing)
```python
# 문서 로딩
docs = loader.load()

# 청킹
chunks = text_splitter.split_documents(docs)

# 임베딩
embeddings = OpenAIEmbeddings()

# 벡터 스토어
vectorstore = Chroma.from_documents(chunks, embeddings)
```

#### 2. 검색 (Retrieval)
```python
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 5}
)

relevant_docs = retriever.invoke("질문")
```

#### 3. 생성 (Generation)
```python
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

answer = rag_chain.invoke("질문")
```

## 🚀 실행 방법

### 환경 설정

```bash
cd tutorials/07_문서기반_답변과_RAG

# 패키지 설치
pip install -r requirements.txt

# API 키 설정
# 프로젝트 루트의 .env 파일에 추가
# OPENAI_API_KEY=your-api-key
# TAVILY_API_KEY=your-api-key (07_2, 07_3 사용 시)
```

### Jupyter Notebook 실행

```bash
jupyter notebook 07_1_LangChain_RAG_기초.ipynb
jupyter notebook 07_2_RAG_Tool_만들기.ipynb
jupyter notebook 07_3_LangGraph_RAG_Agent.ipynb
```

## 📋 실습 구성

### 07_1_LangChain_RAG_기초.ipynb

**사용 데이터**: `data/` 폴더의 PDF 파일들 (귀신고래.pdf, 범고래.pdf, 흰꼬리수리.pdf)

```
1. 환경 설정
2. PDF 문서 로딩 (PyMuPDFLoader)
3. 텍스트 청킹 (RecursiveCharacterTextSplitter)
4. 임베딩 생성 (OpenAIEmbeddings)
5. 벡터 스토어 구축 (Chroma)
6. 검색기 생성
7. RAG 체인 구성 (LCEL)
8. RAG 체인 구성 (RetrievalQA)
```

**예제 질문**: "범고래는 어떤 먹이를 먹나요?"

### 07_2_RAG_Tool_만들기.ipynb

**사용 데이터**: "Attention Is All You Need" 논문 (웹에서 직접 로딩)

```
1. 환경 설정
2. 데이터 로드 (PyPDFLoader - 웹)
3. 텍스트 전처리 (분할)
4. 임베딩 및 벡터 스토어 (FAISS)
5. RAG Tool 생성 (create_retriever_tool)
6. Tavily Tool 생성
7. Agent 연동 및 테스트

빈칸 채우기:
- Tavily Tool 생성
- tools 리스트 구성
- Agent 생성 (llm, tools, prompt)
- AgentExecutor 생성
```

**예제 질문**:
1. 논문 내용: "트랜스포머 모델의 주요 구성 요소는?"
2. 웹 검색: "요즘 인기 있는 프론트엔드 프레임워크는?"
3. 복합 질문: "논문 저자 Ashish Vaswani의 다른 연구는?"

### 07_3_LangGraph_RAG_Agent.ipynb

**사용 데이터**: D2L (Dive into Deep Learning) 교재 PDF

```
1. 환경 설정
2. PDF 다운로드 및 VectorDB 검색기 설정
3. State 및 노드 정의
   - thought_node: 검색 전략 수립
   - action_node: 검색 수행
   - observation_node: 결과 평가 및 답변 생성
4. 그래프 구성
5. 실행 함수
6. 테스트
   - VectorDB 검색
   - 웹 검색
   - 대화 컨텍스트 유지
```

**특징**:
- ReAct 패턴으로 동적 검색
- 검색 결과 평가 후 재시도
- 최대 5회 반복 시도
- 대화 히스토리 유지

## 💡 주요 API

### 문서 로딩
```python
from langchain_community.document_loaders import PyMuPDFLoader, PyPDFLoader

# 로컬 파일
loader = PyMuPDFLoader("file.pdf")

# 웹 URL
loader = PyPDFLoader("https://example.com/paper.pdf")

docs = loader.load()
```

### 텍스트 청킹
```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,      # 청크 크기
    chunk_overlap=200    # 중복 크기
)

chunks = splitter.split_documents(docs)
```

### 임베딩
```python
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
```

### 벡터 스토어
```python
from langchain_community.vectorstores import Chroma, FAISS

# Chroma (영구 저장)
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

# FAISS (메모리)
vectorstore = FAISS.from_documents(chunks, embeddings)
```

### 검색기
```python
retriever = vectorstore.as_retriever(
    search_type="similarity",           # 유사도 검색
    search_kwargs={"k": 5}              # 상위 5개
)

# 또는 MMR (최대 한계 관련성)
retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 5, "fetch_k": 10}
)
```

### RAG 체인 (LCEL)
```python
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

answer = rag_chain.invoke("질문")
```

### RAG 체인 (RetrievalQA)
```python
from langchain_classic.chains import RetrievalQA

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True
)

result = qa_chain.invoke({"query": "질문"})
```

### RAG Tool
```python
from langchain_core.tools import create_retriever_tool

retriever_tool = create_retriever_tool(
    retriever,
    "document_search",
    "Searches information from the document. Use this for document-related questions."
)
```

### LangGraph RAG Agent
```python
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver

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

agent = workflow.compile(checkpointer=memory)
```

## 🎓 학습 포인트

### 청킹 전략
1. **chunk_size**: 너무 작으면 문맥 손실, 너무 크면 검색 정확도 저하
2. **chunk_overlap**: 문맥 연결성 유지
3. **분할 기준**: 문단 → 문장 → 단어 (RecursiveCharacterTextSplitter)

### 임베딩 모델 선택
- **text-embedding-3-small**: 빠르고 저렴, 대부분의 경우 충분
- **text-embedding-3-large**: 더 높은 정확도, 비용 증가

### 벡터 스토어 비교

| 항목 | Chroma | FAISS | Pinecone |
|------|--------|-------|----------|
| 영구 저장 | O | X | O |
| 확장성 | 중간 | 낮음 | 높음 |
| 설정 | 쉬움 | 쉬움 | 복잡 |
| 비용 | 무료 | 무료 | 유료 |

### 검색 전략
1. **Similarity**: 기본, 코사인 유사도
2. **MMR**: 다양성 고려, 중복 감소
3. **Similarity Score Threshold**: 임계값 이상만 반환

### RAG 평가
- **정확도**: 답변이 문서 내용과 일치하는가?
- **관련성**: 검색된 문서가 질문과 관련 있는가?
- **완전성**: 모든 필요한 정보가 포함되었는가?

## 🔗 참고 자료

- [LangChain RAG Tutorial](https://python.langchain.com/docs/tutorials/rag/)
- [OpenAI Embeddings](https://platform.openai.com/docs/guides/embeddings)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Vector Database Comparison](https://www.datacamp.com/blog/the-top-5-vector-databases)

## 📊 실습 후 확인사항

- [ ] PDF 문서 로딩 및 청킹 이해
- [ ] 임베딩과 벡터 스토어 개념 파악
- [ ] RAG 체인 구성 (LCEL & RetrievalQA)
- [ ] RAG를 Tool로 만들어 Agent에 통합
- [ ] LangGraph로 고급 RAG Agent 구현
- [ ] VectorDB + 웹검색 하이브리드 전략

## 🔜 다음 단계

이 실습을 완료하면:
- **08. RAG 최적화 기법**에서 청킹 전략, 하이브리드 검색, Re-ranking 학습
- **09. LangGraph 기초**에서 복잡한 Agent 워크플로우 구현
- **10. 종합 프로젝트**에서 모든 내용을 통합한 고급 챗봇 구현

이제 문서를 기반으로 정확한 답변을 생성하는 RAG 시스템을 마스터했습니다!


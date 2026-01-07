# LangChain & LangGraph 교육 자료

NVIDIA Academy Agent 과정을 위한 LangChain/LangGraph 실습 자료입니다.

## 📚 커리큘럼

### 1. LLM API 사용 방법
- OpenAI API 기초
- Chat Completion
- Vision API

### 2. 프롬프트 엔지니어링
- Zero-shot, Few-shot
- Chain-of-Thought (CoT)
- Self-Consistency

### 3. LangChain 기초
- LLM과 템플릿
- LCEL과 체인
- Memory
- Output Parsers

### 4. Streamlit 기초
- 기본 컴포넌트
- 레이아웃
- Session State
- Chat Interface

### 5. 채팅 UI 만들기
- 기본 채팅 앱 (app1.py)
- 세션 관리 (app2.py)
- 응답 편집 (app3.py)

### 6. 도구 연결하기
- OpenAI Function Calling
- LangChain Built-in Tools
- Custom Tools
- 웹 검색 통합 (app4.py)

### 7. 문서기반 답변과 RAG
- Chunking, Embedding, Retrieval
- LangChain RAG 기초
- RAG Tool 만들기
- LangGraph RAG Agent

### 8. 조건부 라우팅
- Router LLM
- 조건부 엣지
- VectorDB / WebSearch / Direct LLM
- 하이브리드 시스템

## 🚀 시작하기

### 환경 설정

```bash
# 1. 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate  # Windows

# 2. 패키지 설치
pip install -r requirements.txt

# 3. 환경 변수 설정
cp env.example .env
# .env 파일을 열어 API 키 입력
```

### API 키 발급

- **OpenAI API**: https://platform.openai.com/api-keys
- **Tavily API** (웹 검색용): https://tavily.com/

## 📂 폴더 구조

```
LangChain/
├── tutorials/                    # 실습 자료
│   ├── 01_LLM_API_사용방법/
│   ├── 02_프롬프트_엔지니어링/
│   ├── 03_LangChain_기초/
│   ├── 04_Streamlit_기초/
│   │   └── student/            # 학생용 코드
│   ├── 05_채팅UI_만들기/
│   │   └── student/
│   ├── 06_도구_연결하기/
│   │   └── student/
│   ├── 07_문서기반_답변과_RAG/
│   │   └── student/
│   └── 08_조건부_라우팅/
│       └── student/
└── requirements.txt             # Python 패키지 목록
```

## 🎯 각 단원 구조

각 단원은 다음과 같이 구성되어 있습니다:

- **README.md**: 단원 개요 및 학습 목표
- **student/**: 학생용 코드 (빈칸 포함)
- **README_STUDENT.md**: 학생용 가이드 (힌트 포함)

> ⚠️ **정답 파일(complete/)은 교육 종료 후 공개 예정입니다.**

## 💻 실행 방법

### Jupyter Notebook 실행

```bash
# Jupyter Notebook 시작
jupyter notebook

# 또는 JupyterLab
jupyter lab
```

### Streamlit 앱 실행

```bash
# 예: 4번 단원 Streamlit 기초
cd tutorials/04_Streamlit_기초/complete
streamlit run app.py

# 예: 8번 단원 Router Agent
cd tutorials/08_조건부_라우팅/complete
python setup_d2l.py  # 최초 1회 실행
streamlit run app_router.py
```

## 📖 학습 방법

### 1. 이론 학습
- 각 단원의 README.md 읽기
- Jupyter Notebook 실습 따라하기

### 2. 실습
- `student/` 폴더의 코드에서 `# YOUR CODE HERE` 부분 채우기
- `README_STUDENT.md`의 힌트 참고

### 3. 검증
- 코드 실행하여 작동 확인
- 동료들과 코드 리뷰
- ⚠️ 정답 파일은 교육 종료 후 공개됩니다

### 4. 응용
- 배운 내용을 바탕으로 자신만의 프로젝트 구현

## 🛠️ 주요 기술 스택

- **LangChain**: LLM 애플리케이션 프레임워크
- **LangGraph**: 상태 기반 멀티 에이전트 프레임워크
- **Streamlit**: 웹 UI 프레임워크
- **OpenAI API**: GPT 모델
- **Tavily**: AI 최적화 웹 검색
- **ChromaDB**: 벡터 데이터베이스

## 📝 요구사항

- Python 3.8 이상
- OpenAI API 키
- Tavily API 키 (웹 검색 기능 사용 시)

## ⚠️ 주의사항

1. **API 키 보안**
   - `.env` 파일은 절대 Git에 커밋하지 마세요
   - `env.example`을 참고하여 `.env` 파일을 생성하세요

2. **가상환경 사용**
   - 반드시 가상환경을 사용하세요
   - 프로젝트별로 독립적인 환경 유지

3. **비용 관리**
   - OpenAI API는 사용량에 따라 과금됩니다
   - 테스트 시 적절한 모델 선택 (예: gpt-4.1-mini)

## 🔗 참고 자료

- [LangChain 문서](https://python.langchain.com/)
- [LangGraph 문서](https://langchain-ai.github.io/langgraph/)
- [Streamlit 문서](https://docs.streamlit.io/)
- [OpenAI API 문서](https://platform.openai.com/docs)
- [D2L 교재](https://d2l.ai/)

## 📄 라이선스

이 자료는 교육 목적으로 제공됩니다.

## 👥 기여

버그 리포트, 개선 제안 등은 이슈로 등록해주세요.

---

**Happy Learning!** 🚀

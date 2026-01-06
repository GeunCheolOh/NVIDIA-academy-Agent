# 06. 도구가 연결된 채팅 앱 - 학생용 실습

LangChain Tool을 실제 Streamlit 앱에 통합하는 실습입니다.

## 🎯 학습 목표

**3번(LangChain), 4번(Streamlit), 5번(채팅UI), 6번(도구 연결)에서 배운 내용**을 모두 활용합니다.

## 📝 파일 구성

### 정답 파일 (../complete/)
- `app4.py` - 웹검색 통합 채팅 앱

### 학생용 파일 (현재 폴더)
- `app4.py` - 웹검색 통합 실습 (10개 빈칸)

## 🚀 실행 방법

### 1. 환경 설정

```bash
# 상위 디렉토리에서 패키지 설치
cd ..
pip install -r requirements.txt

# API 키 설정
cp env.example .env
# .env 파일을 열어 API 키를 입력하세요:
# OPENAI_API_KEY=your-api-key
# TAVILY_API_KEY=your-api-key (Tavily 사용 시)
```

### 2. 학생용 파일 실행

```bash
cd student
streamlit run app4.py
```

### 3. 정답 확인

```bash
streamlit run ../complete/app4.py
```

## 📋 실습 가이드

### app4.py - 웹검색 통합 채팅 앱 (10개 빈칸)

#### 학습할 API:

**LangChain Tool (06에서 배움):**
- `TavilySearchResults()` - Tavily 검색 도구
- `DDGS()` - DuckDuckGo 검색 도구
- `tool.invoke()` - 도구 실행

**LangChain Messages (03에서 배움):**
- `SystemMessage()` - 시스템 프롬프트 전달

**Streamlit (04에서 배움):**
- `st.session_state` - 상태 관리
- `st.expander()` - 접을 수 있는 섹션
- `st.spinner()` - 로딩 표시

**Session 관리 (05에서 배움):**
- `conversations` 딕셔너리 구조
- 대화별 데이터 저장

#### 실습 순서:

**빈칸 1-2: Session State 초기화**
- `conversations`에 `search_results`, `system_prompt` 필드 추가
- `search_engine` 상태 초기화

**빈칸 3-4: 검색 도구 사용**
- `TavilySearchResults` 초기화 및 호출
- `DDGS` 객체 생성 및 검색

**빈칸 5: 검색 결과 표시**
- `st.expander()`로 검색 결과 표시

**빈칸 6-7: 검색 버튼 토글**
- 버튼 클릭 시 `search_engine` 상태 변경

**빈칸 8-9: 검색 결과 처리**
- 검색 결과 저장
- 검색 결과를 프롬프트에 포함

**빈칸 10: 시스템 프롬프트**
- `SystemMessage`로 시스템 프롬프트 추가

---

## 💡 실습 팁

### 막힐 때:
1. **주석 힌트 확인**: 각 빈칸에 구체적인 코드 예시 제공
2. **06_2, 06_3 노트북 참고**: Tool 사용법 복습
3. **정답 참고**: `../complete/app4.py` 확인
4. **단계별 테스트**: 빈칸 하나씩 채우고 실행

### 디버깅:
- 터미널에서 에러 메시지 확인
- `st.write()`로 변수 값 출력
- `st.json(st.session_state)`로 상태 확인

## 📊 빈칸별 학습 포인트

### 빈칸 1-2: Session State 확장
```python
# 기존 (05에서 배움)
"messages": []

# 추가 (06에서 배움)
"search_results": {},  # 메시지 인덱스 → 검색 결과
"system_prompt": ""    # 시스템 프롬프트
```

### 빈칸 3: Tavily Tool
```python
# 06_2에서 배운 내용
from langchain_community.tools.tavily_search import TavilySearchResults

search_tool = TavilySearchResults(max_results=5, api_key=api_key)
results = search_tool.invoke(query)
```

### 빈칸 4: DuckDuckGo
```python
# 06_2에서 배운 내용
from ddgs import DDGS

ddgs = DDGS()
results = list(ddgs.text(query, max_results=5))
```

### 빈칸 5: 검색 결과 표시
```python
# 04에서 배운 내용
if idx in current_conv.get("search_results", {}):
    with st.expander("🔍 검색 결과 보기", expanded=False):
        st.markdown(current_conv["search_results"][idx])
```

### 빈칸 6-7: 버튼 토글
```python
# 04에서 배운 내용 + 상태 관리
if button_clicked:
    st.session_state.search_engine = "tavily" if st.session_state.search_engine != "tavily" else None
```

### 빈칸 8: 검색 결과 저장
```python
# 05에서 배운 딕셔너리 저장 패턴
current_conv["search_results"][user_msg_idx] = search_results
```

### 빈칸 9: RAG 패턴
```python
# 검색 결과를 프롬프트에 포함
augmented_prompt = f"{prompt}\n\n{search_results}\n\n위 검색 결과를 참고하여 답변해주세요."
```

### 빈칸 10: SystemMessage
```python
# 03에서 배운 내용
from langchain_core.messages import SystemMessage

if system_prompt:
    messages = [SystemMessage(content=system_prompt)] + messages
```

## 🎓 주요 개념

### Tool Integration (도구 통합)
1. **Tool 초기화**: API 키, 파라미터 설정
2. **Tool 실행**: `tool.invoke(query)`
3. **결과 처리**: 포맷팅 및 저장
4. **오류 처리**: Try-except로 안전하게 처리

### RAG (Retrieval-Augmented Generation)
```
사용자 질문
    ↓
외부 검색 (Tool)
    ↓
검색 결과 + 질문 = 증강된 프롬프트
    ↓
LLM 응답
```

### Session State 구조
```python
conversations = {
    "session_id": {
        "messages": [HumanMessage, AIMessage, ...],
        "search_results": {
            0: "검색결과1",  # 메시지 인덱스 → 결과
            2: "검색결과2"
        },
        "system_prompt": "당신은 친절한 AI입니다.",
        ...
    }
}
```

## 🆘 문제 해결

### API 키 오류
```
Tavily API 키가 설정되지 않았습니다
```
→ `.env` 파일에 `TAVILY_API_KEY` 추가

### Tool import 오류
```
ModuleNotFoundError: No module named 'langchain_community'
```
→ `pip install langchain-community` 실행

### 검색 결과 표시 안 됨
```
검색은 되는데 결과가 안 보임
```
→ 빈칸 5, 8 확인 (저장 및 표시 로직)

### 검색 버튼 토글 안 됨
```
버튼을 눌러도 활성화 안 됨
```
→ 빈칸 6-7 확인 (토글 로직)

## 📚 참고 코드

### 완전한 Tool 사용 예시
```python
# 1. Tool 초기화
from langchain_community.tools.tavily_search import TavilySearchResults

search_tool = TavilySearchResults(
    max_results=5,
    api_key=os.getenv("TAVILY_API_KEY")
)

# 2. Tool 실행
results = search_tool.invoke("LangChain이란?")

# 3. 결과 처리
for result in results:
    print(result.get('title'))
    print(result.get('content'))
```

### 검색 결과를 LLM에 전달
```python
# 원래 질문
user_question = "LangChain이란?"

# 검색 수행
search_results = search_tool.invoke(user_question)

# 증강된 프롬프트
augmented_prompt = f"""
{user_question}

검색 결과:
{search_results}

위 검색 결과를 참고하여 답변해주세요.
"""

# LLM에 전달
messages = [HumanMessage(content=augmented_prompt)]
response = llm.stream(messages)
```

## 🎉 완료 후

모든 빈칸을 채우고 앱이 정상 작동하면:

### 테스트해볼 기능:
1. **검색 없이 질문**: "안녕하세요"
2. **Tavily 검색**: "2024년 AI 트렌드는?"
3. **DuckDuckGo 검색**: "파이썬 최신 버전"
4. **시스템 프롬프트**: "당신은 전문 개발자입니다."
5. **세션 전환**: 새 대화 만들고 전환

### 확인사항:
- [ ] 검색 버튼 토글 작동
- [ ] 검색 결과 expander 표시
- [ ] 검색 결과 기반 답변 생성
- [ ] 검색 결과 세션별 저장
- [ ] 시스템 프롬프트 적용

## 🔗 다음 단계

이 실습을 완료하면:
- **07. 웹검색 기반 LangChain 앱**에서 더 고급 RAG 패턴 학습
- **08. 문서기반 답변과 RAG**에서 벡터 DB와 임베딩 학습
- **09. LangGraph 기초**에서 복잡한 워크플로우 구현

축하합니다! LangChain Tool을 실전 앱에 통합하는 방법을 마스터했습니다! 🎊


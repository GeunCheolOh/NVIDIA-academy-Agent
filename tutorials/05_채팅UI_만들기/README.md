# 05. 채팅 UI 만들기 (Streamlit + LangChain)

LangChain과 Streamlit을 결합하여 실전 채팅 애플리케이션을 구축합니다.

## 📚 학습 내용

3번(LangChain 기초)과 4번(Streamlit 기초)에서 배운 내용을 실전에 적용합니다.

### app1.py - 기본 채팅 앱
- ChatOpenAI 모델 초기화
- Session State로 메시지 관리
- Chat UI 구성 (chat_message, chat_input)
- 스트리밍 응답 구현
- 사이드바 설정 패널

### app2.py - 세션 관리
- UUID로 대화 세션 생성
- 여러 대화 동시 관리
- 대화 목록 표시 및 전환
- 세션별 메시지 저장

### app3.py - 응답 편집 기능
- 4단계 stage 관리 (user, validate, correct, rewrite)
- AI 응답 검증 및 수정
- 문장별 편집
- 전체 재작성

## 🚀 실행 방법

### 1. 환경 설정

```bash
# 패키지 설치
cd tutorials/05_채팅UI_만들기
pip install -r requirements.txt

# API 키 설정
cp .env.example .env
# .env 파일을 열어 OPENAI_API_KEY를 입력하세요
```

### 2. 정답 파일 실행

```bash
streamlit run complete/app1.py    # 기본 채팅
streamlit run complete/app2.py    # 세션 관리
streamlit run complete/app3.py    # 응답 편집
```

### 3. 학생용 파일 실습

```bash
streamlit run student/app1.py     # 빈칸 채우기 실습
streamlit run student/app2.py
streamlit run student/app3.py
```

## 📋 실습 빈칸 목록

### app1.py (7개 빈칸)
1. `st.set_page_config()` - 페이지 설정
2. Session State "messages" 초기화
3. Session State "llm" 초기화 (ChatOpenAI)
4. `st.rerun()` - 페이지 새로고침
5. `st.chat_message("user")` - 사용자 메시지 표시
6. `st.chat_input()` - 사용자 입력
7. `HumanMessage` 생성 및 추가
8. `st.empty()` - 스트리밍 placeholder
9. `llm.stream()` - 스트리밍 응답
10. `AIMessage` 생성 및 추가

### app2.py (6개 빈칸)
1. Session State "conversations" 딕셔너리 초기화 (uuid 사용)
2. `create_new_conversation()` 함수 구현
3. `st.columns([6, 1])` - 제목과 버튼 배치
4. "새 대화" 버튼 구현
5. conversations 정렬 (created_at 기준)
6. 현재 대화의 messages에 HumanMessage 추가
7. 현재 대화의 messages로 llm.stream() 호출

### app3.py (6개 빈칸)
1. Session State "stage" 초기화
2. Session State "pending" 초기화
3. stage == "user" 조건문
4. pending에 응답 저장 및 stage 변경
5. `st.columns(3)` - 3개 버튼 배치
6. "수락" 버튼 구현
7. `st.text_area()` - 응답 재작성 UI

## 🎯 학습 목표

### LangChain 관련 (3번 복습)
- ✅ `ChatOpenAI` 초기화 및 설정
- ✅ `HumanMessage`, `AIMessage` 사용
- ✅ `llm.stream()` - 스트리밍 응답 처리

### Streamlit 관련 (4번 복습)
- ✅ `st.session_state` - 상태 관리
- ✅ `st.chat_message()` - 채팅 메시지 컨테이너
- ✅ `st.chat_input()` - 채팅 입력창
- ✅ `st.empty()` - 동적 업데이트
- ✅ `st.sidebar` - 사이드바 구성
- ✅ `st.columns()` - 레이아웃 분할
- ✅ `st.rerun()` - 페이지 새로고침

## 💡 실습 팁

1. **app1부터 시작**: 가장 기본적인 기능부터 구현
2. **정답 참고**: 막히면 complete 폴더의 정답 확인
3. **테스트**: 빈칸을 채운 후 바로 실행해보기
4. **에러 확인**: Streamlit 오류 메시지를 잘 읽기

## 📖 참고 자료

- [LangChain ChatOpenAI](https://python.langchain.com/docs/integrations/chat/openai)
- [Streamlit Chat Elements](https://docs.streamlit.io/develop/api-reference/chat)
- [Streamlit Session State](https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state)

## 🔗 다음 단계

이 실습을 완료하면:
- **06. LangChain에 도구 연결하기**로 넘어가 Tool 사용법 학습
- **07. 웹검색 기반 LangChain 앱 만들기**에서 Tavily/DuckDuckGo 통합


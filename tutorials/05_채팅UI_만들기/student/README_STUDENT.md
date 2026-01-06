# 05. 채팅 UI 만들기 - 학생용 실습

LangChain과 Streamlit을 결합한 채팅 애플리케이션을 직접 만들어봅니다.

## 🎯 학습 목표

**3번(LangChain 기초)과 4번(Streamlit 기초)에서 배운 내용**을 실전에 적용합니다.

## 📝 파일 구성

### 정답 파일 (../complete/)
- `app1.py` - 기본 채팅 앱
- `app2.py` - 세션 관리
- `app3.py` - 응답 편집

### 학생용 파일 (현재 폴더)
- `app1.py` - 기본 채팅 앱 실습
- `app2.py` - 세션 관리 실습
- `app3.py` - 응답 편집 실습

## 🚀 실행 방법

### 1. 환경 설정

```bash
# 상위 디렉토리에서 패키지 설치
cd ..
pip install -r requirements.txt

# API 키 설정
cp env.example .env
# .env 파일을 열어 OPENAI_API_KEY를 입력하세요
```

### 2. 학생용 파일 실행

```bash
cd student
streamlit run app1.py
streamlit run app2.py
streamlit run app3.py
```

### 3. 정답 확인

```bash
streamlit run ../complete/app1.py
```

## 📋 실습 가이드

### app1.py - 기본 채팅 앱 (10개 빈칸)

#### 학습할 API:
**LangChain (3번에서 배움):**
- `ChatOpenAI()` - LLM 모델 초기화
- `HumanMessage()` - 사용자 메시지 생성
- `AIMessage()` - AI 응답 저장
- `llm.stream()` - 스트리밍 응답

**Streamlit (4번에서 배움):**
- `st.set_page_config()` - 페이지 설정
- `st.session_state` - 상태 관리
- `st.chat_message()` - 채팅 메시지 표시
- `st.chat_input()` - 사용자 입력
- `st.empty()` - 동적 업데이트
- `st.rerun()` - 페이지 새로고침

#### 실습 순서:
1. 페이지 설정 (`st.set_page_config`)
2. Session State 초기화 (messages, llm)
3. 사이드바 구성 완료
4. 메시지 표시 구현
5. 사용자 입력 처리
6. 스트리밍 응답 구현

---

### app2.py - 세션 관리 (7개 빈칸)

#### 추가 학습 내용:
- `uuid.uuid4()` - 고유 ID 생성
- `datetime.now()` - 현재 시간
- 딕셔너리 기반 다중 세션 관리
- `st.columns()` - 레이아웃 구성

#### 실습 순서:
1. conversations 딕셔너리 초기화
2. create_new_conversation() 함수 구현
3. 제목과 버튼 레이아웃
4. 새 대화 버튼 구현
5. 대화 목록 정렬
6. 현재 대화에 메시지 추가

---

### app3.py - 응답 편집 (7개 빈칸)

#### 추가 학습 내용:
- 4단계 stage 관리
- 조건부 렌더링
- `st.text_area()` - 다중 라인 입력
- `st.text_input()` - 단일 라인 입력

#### 실습 순서:
1. stage, pending Session State 초기화
2. stage별 조건문 구현
3. pending 저장 및 stage 전환
4. 버튼 레이아웃 구성
5. 수락 버튼 구현
6. 재작성 UI 구현

## 💡 실습 팁

### 막힐 때:
1. **주석 힌트 확인**: 각 빈칸에 어떤 코드를 작성해야 하는지 주석으로 안내
2. **정답 참고**: `../complete/` 폴더의 정답 파일 확인
3. **오류 메시지**: Streamlit과 Python 오류 메시지를 잘 읽기
4. **단계별 테스트**: 빈칸 하나씩 채우고 실행해보기

### 디버깅:
- 터미널에서 에러 메시지 확인
- `st.write()`로 변수 값 출력
- Session State 값 확인: `st.json(st.session_state)`

## 📊 진도 체크리스트

### app1.py
- [ ] 페이지 설정 완료
- [ ] Session State 초기화
- [ ] 메시지 표시 구현
- [ ] 사용자 입력 처리
- [ ] 스트리밍 응답 구현
- [ ] 전체 동작 확인

### app2.py
- [ ] 다중 세션 초기화
- [ ] 새 대화 생성 구현
- [ ] 대화 목록 표시
- [ ] 세션 전환 기능
- [ ] 세션별 메시지 저장
- [ ] 전체 동작 확인

### app3.py
- [ ] Stage 관리 구현
- [ ] 응답 검증 단계
- [ ] 문장별 수정 기능
- [ ] 전체 재작성 기능
- [ ] 전체 동작 확인

## 🎓 학습 효과

이 실습을 완료하면:
- ✅ LangChain과 Streamlit을 실전에서 활용
- ✅ 상태 관리의 중요성 이해
- ✅ 복잡한 UI 흐름 구현 경험
- ✅ 실무에서 사용 가능한 채팅 앱 구축 능력

## 🆘 문제 해결

### API 키 오류
```
OpenAI API key가 없습니다
```
→ `.env` 파일에 `OPENAI_API_KEY` 설정

### 모듈 import 오류
```
ModuleNotFoundError: No module named 'langchain_openai'
```
→ `pip install -r requirements.txt` 실행

### Session State 오류
```
AttributeError: 'NoneType' object has no attribute 'append'
```
→ Session State 초기화 확인

## 🔗 참고 자료

- [LangChain Chat Models](https://python.langchain.com/docs/integrations/chat/)
- [Streamlit Chat Elements](https://docs.streamlit.io/develop/api-reference/chat)
- [Session State Guide](https://docs.streamlit.io/develop/concepts/architecture/session-state)

## 🎉 완료 후

모든 실습을 완료하셨나요? 축하합니다! 🎊

이제 다음 단계로:
- **06. LangChain에 도구 연결하기**
- **07. 웹검색 기반 LangChain 앱 만들기**

실전 능력을 더욱 향상시켜보세요!


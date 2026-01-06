# 04. Streamlit 기초 튜토리얼 - 학생용 교안

Streamlit의 핵심 컴포넌트와 기능을 학습하는 실습 자료입니다.
**이 파일들은 학생용 교안으로, 중요한 코드 부분이 `# YOUR CODE HERE`로 표시되어 있습니다.**

## 📚 학습 방법

1. **정답 파일 먼저 확인**: `app.py`, `tutorial.py`, `pages/page*.py` 파일들을 먼저 실행하고 동작을 확인하세요.
2. **학생용 파일 실습**: `*_student.py` 파일을 열고 `# YOUR CODE HERE` 부분을 채워보세요.
3. **실행 및 확인**: 작성한 코드를 실행하여 정답 파일과 같이 동작하는지 확인하세요.

## 📝 파일 구성

### 정답 파일 (참고용 - ../complete/)
- `app.py` - 메인 페이지
- `tutorial.py` - 기본 컴포넌트
- `pages/page1_basic_widgets.py` - 기본 위젯
- `pages/page2_layout.py` - 레이아웃
- `pages/page3_session_state.py` - 세션 상태
- `pages/page4_chat_interface.py` - 채팅 UI
- `pages/page5_advanced.py` - 고급 기능

### 학생용 파일 (실습용 - 현재 폴더)
- `app.py` - 메인 페이지 실습
- `tutorial.py` - 기본 컴포넌트 실습
- `pages/page1_basic_widgets.py` - 기본 위젯 실습
- `pages/page2_layout.py` - 레이아웃 실습
- `pages/page3_session_state.py` - 세션 상태 실습
- `pages/page4_chat_interface.py` - 채팅 UI 실습
- `pages/page5_advanced.py` - 고급 기능 실습

## 🎯 각 파일별 학습 목표

### 1. app_student.py (5개 빈칸)
학습할 API:
- `st.set_page_config()` - 페이지 설정
- `st.text_input()` - 텍스트 입력
- `st.success()` - 성공 메시지
- `st.columns()` - 컬럼 레이아웃
- `st.metric()` - 메트릭 카드

### 2. tutorial_student.py (6개 빈칸)
학습할 API:
- `st.columns()` - 컬럼 생성
- `st.success()`, `st.info()` - 성공/정보 메시지
- `st.warning()`, `st.error()` - 경고/오류 메시지
- `st.dataframe()` - 데이터프레임 표시
- `st.json()` - JSON 데이터 표시
- `col.metric()` - 메트릭 표시

### 3. page1_basic_widgets_student.py (6개 빈칸)
학습할 API:
- `st.text_input()` - 텍스트 입력
- `st.text_area()` - 여러 줄 텍스트
- `st.selectbox()` - 선택 박스
- `st.checkbox()` - 체크박스
- `st.button()` - 버튼
- `st.file_uploader()` - 파일 업로드

### 4. page2_layout_student.py (5개 빈칸)
학습할 API:
- `with st.sidebar:` - 사이드바
- `st.columns()` - 컬럼 레이아웃
- `st.tabs()` - 탭 레이아웃
- `with st.expander():` - 확장 섹션
- `st.container()` - 컨테이너

### 5. page3_session_state_student.py (6개 빈칸)
학습할 API:
- Session State 초기화
- Session State 값 증가
- `st.rerun()` - 페이지 새로고침
- Session State 리스트 조작
- Session State 딕셔너리 저장

### 6. page4_chat_interface_student.py (5개 빈칸)
학습할 API:
- `st.chat_message()` - 채팅 메시지 컨테이너 (2개)
- Session State 초기화
- `st.empty()` - 빈 컨테이너
- 스트리밍 효과 구현 (for loop)

### 7. page5_advanced_student.py (6개 빈칸)
학습할 API:
- `st.spinner()` - 로딩 스피너
- `st.progress()` - 진행바
- `st.status()` - 상태 표시
- `st.toast()` - 알림 메시지
- `st.download_button()` - 다운로드 버튼
- `with st.form():` - 폼 제출

## 🚀 실행 방법

### 정답 확인 (상위 폴더로 이동)
```bash
cd ../complete
streamlit run app.py
streamlit run tutorial.py
```

### 학생용 파일 실행 (현재 폴더)
```bash
streamlit run app.py
streamlit run tutorial.py
```

### 개별 페이지 실행
```bash
# 정답
streamlit run ../complete/pages/page1_basic_widgets.py

# 학생용 (현재 폴더)
streamlit run pages/page1_basic_widgets.py
```

## 💡 실습 팁

1. **정답 파일 참고**: 막히면 정답 파일을 확인하세요.
2. **공식 문서**: [Streamlit Documentation](https://docs.streamlit.io)을 참고하세요.
3. **단계적 학습**: 한 번에 하나씩 빈칸을 채워가며 실행해보세요.
4. **실험**: 파라미터를 바꿔가며 다양하게 실험해보세요.
5. **오류 메시지**: 오류 메시지를 잘 읽고 문제를 해결해보세요.

## 📊 진도 체크리스트

- [ ] app.py 완료
- [ ] tutorial.py 완료
- [ ] page1_basic_widgets.py 완료
- [ ] page2_layout.py 완료
- [ ] page3_session_state.py 완료
- [ ] page4_chat_interface.py 완료
- [ ] page5_advanced.py 완료

## 🎓 추가 학습 자료

- [Streamlit 공식 튜토리얼](https://docs.streamlit.io/get-started/tutorials)
- [Streamlit API Reference](https://docs.streamlit.io/develop/api-reference)
- [Streamlit Gallery](https://streamlit.io/gallery) - 다양한 예제 앱

## ❓ 문제 해결

### 실행이 안 될 때
```bash
# 패키지 재설치
pip install -r requirements.txt

# 캐시 초기화
streamlit cache clear
```

### 변경사항이 반영 안 될 때
- 브라우저 새로고침 (F5)
- Streamlit 우측 상단 "Rerun" 클릭
- "Always rerun" 설정 활성화

## 🎉 완료 후

모든 실습을 완료하셨나요? 축하합니다! 🎊

이제 다음 단계로 진행하세요:
- **05. Streamlit으로 LangChain 연결하여 채팅 UI 만들기**

궁금한 점이 있으면 언제든지 질문하세요!


# 04. Streamlit 기초 튜토리얼

Streamlit의 핵심 컴포넌트와 기능을 학습하는 실습 자료입니다.
이 튜토리얼은 app1~4에서 사용된 모든 Streamlit API를 포함합니다.

## 📚 학습 내용

1. **기본 위젯**: 텍스트 입력, 버튼, 선택 도구
2. **레이아웃**: 사이드바, 컬럼, 탭, Expander
3. **세션 상태**: Session State를 활용한 상태 관리
4. **채팅 인터페이스**: Chat UI 구성 요소
5. **고급 기능**: Spinner, Empty, Rerun 등

## 🚀 준비

```bash
cd tutorials/04_streamlit
pip install -r requirements.txt
```

## 📖 실행 방법

### 정답 파일 실행 (강사/참고용)
```bash
streamlit run complete/app.py        # 메인 페이지
streamlit run complete/tutorial.py   # 기본 컴포넌트
```

### 학생용 파일 실행 (실습용)
```bash
streamlit run student/app.py        # 메인 페이지 실습
streamlit run student/tutorial.py   # 기본 컴포넌트 실습
```

### 개별 페이지 실행
```bash
# 정답 확인
streamlit run complete/pages/page1_basic_widgets.py

# 학생 실습
streamlit run student/pages/page1_basic_widgets.py
```

## 📋 페이지 구성

### complete/ (정답 파일)
| 파일 | 내용 | 사용된 API |
|------|------|-----------|
| `app.py` | 소개 페이지 | title, write, text_input |
| `tutorial.py` | 기본 컴포넌트 | title, header, write, success, info, warning, error |
| `pages/page1_basic_widgets.py` | 기본 입력 위젯 | text_input, text_area, selectbox, button, checkbox |
| `pages/page2_layout.py` | 레이아웃 구성 | sidebar, columns, tabs, expander, divider |
| `pages/page3_session_state.py` | 세션 상태 관리 | session_state, rerun |
| `pages/page4_chat_interface.py` | 채팅 UI | chat_message, chat_input, empty |
| `pages/page5_advanced.py` | 고급 기능 | spinner, progress, markdown |

### student/ (학생용 파일)
학생용 파일은 위와 동일한 구조이며, `# YOUR CODE HERE`로 표시된 빈칸을 채우는 형식입니다.
자세한 내용은 `student/README_STUDENT.md`를 참고하세요.

## 🛑 종료

터미널에서 `Ctrl + C`를 눌러 실행을 중지합니다.

## 💡 팁

- 코드를 수정하면 자동으로 앱이 새로고침됩니다 (우측 상단의 "Always rerun" 설정)
- 각 페이지는 독립적으로 실행 가능합니다
- Session State는 페이지 리로드 시에도 유지됩니다


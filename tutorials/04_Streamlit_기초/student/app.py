import streamlit as st

# 페이지 설정
# YOUR CODE HERE - st.set_page_config()를 사용하여 페이지 제목, 아이콘, 레이아웃 설정
# page_title="Streamlit 튜토리얼", page_icon="🎓", layout="wide"

st.title("🎓 Streamlit 기초 튜토리얼")
st.write("Streamlit의 핵심 기능을 학습하는 실습 자료입니다.")

st.markdown("---")

st.header("📚 학습 목표")
st.write("""
이 튜토리얼에서는 다음 내용을 학습합니다:
- 기본 위젯과 입력 요소
- 레이아웃 구성 (사이드바, 컬럼, 탭)
- 세션 상태 관리
- 채팅 인터페이스 구축
- 고급 기능 (Spinner, Empty, Rerun)
""")

st.info("👈 왼쪽 사이드바에서 다양한 페이지를 탐색해보세요!")

st.markdown("---")

st.header("🚀 시작하기")

# YOUR CODE HERE - st.text_input()을 사용하여 이름 입력받기
# name = st.text_input(...)

if name:
    # YOUR CODE HERE - st.success()를 사용하여 환영 메시지 표시
    # st.success(f"안녕하세요, {name}님!...")
    
    # YOUR CODE HERE - st.columns(3)을 사용하여 3개의 컬럼 생성
    # col1, col2, col3 = ...
    
    with col1:
        # YOUR CODE HERE - st.metric()을 사용하여 메트릭 표시
        # label="학습 페이지", value="5개", delta="실습 준비"
        pass
    
    with col2:
        st.metric(label="API 개수", value="30+", delta="충분한 예제")
    
    with col3:
        st.metric(label="예상 시간", value="1-2시간", delta="집중 학습")


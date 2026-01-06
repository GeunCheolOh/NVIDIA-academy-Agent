import streamlit as st

# 제목과 헤더
st.title("나의 첫 Streamlit 앱")
st.header("첫 번째 섹션")
st.subheader("세부 내용")

# 일반 텍스트 출력
st.write("안녕하세요! Streamlit으로 만든 앱입니다.")

# 특별한 메시지 표시
st.success("성공적으로 처리되었습니다!")
st.info("참고하세요: 이것은 정보 메시지입니다.")
st.warning("주의: 이 작업은 되돌릴 수 없습니다.")
st.error("오류가 발생했습니다.")

# 작은 캡션 텍스트
st.caption("이것은 작은 글씨로 표시되는 부가 설명입니다.")
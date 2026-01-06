import streamlit as st

st.header("첫 번째 섹션")
st.write("여기에 내용이 들어갑니다.")

# 구분선
st.divider()  # 또는 st.markdown("---")

st.header("두 번째 섹션")
st.write("다른 내용이 여기에 표시됩니다.")
st.markdown("---")

# 확장탭
with st.expander("자세히 보기"):
    st.write("이 부분은 기본적으로 접혀 있으며, 사용자가 클릭하면 펼쳐집니다.")
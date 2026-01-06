import streamlit as st

st.title("나의 첫 Streamlit 앱")
st.write("안녕하세요! Streamlit의 세계에 오신 것을 환영합니다.")

name = st.text_input("이름을 입력하세요")
if name:
    st.write(f"반갑습니다, {name}님!")

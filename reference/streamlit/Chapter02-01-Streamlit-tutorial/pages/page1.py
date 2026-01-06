import streamlit as st

# 텍스트 입력
name = st.text_input("이름을 입력하세요")
description = st.text_area("자기소개를 작성해주세요", height=150)

# 숫자 입력
age = st.number_input("나이", min_value=0, max_value=120, value=25)
height = st.slider("키(cm)", min_value=100.0, max_value=220.0, value=170.0)

# 선택 요소
gender = st.radio("성별", ["남성", "여성"])
favorite_color = st.selectbox("좋아하는 색상", ["빨강", "파랑", "초록", "노랑", "보라"])
interests = st.multiselect("관심사 (여러 개 선택 가능)", ["음악", "영화", "독서", "스포츠", "여행", "요리"])

# 날짜 선택
import datetime
birthday = st.date_input("생일", datetime.date(2000, 1, 1))

# 파일 업로드
uploaded_file = st.file_uploader("프로필 사진 업로드", type=["jpg", "png", "jpeg"])

# 체크박스
agree = st.checkbox("이용약관에 동의합니다")

if st.button("회원가입"):
    if agree:
        st.success(f"안녕하세요, {name}님! 가입을 환영합니다!")
    else:
        st.error("이용약관에 동의해주세요.")
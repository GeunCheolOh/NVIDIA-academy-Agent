import streamlit as st
import datetime

st.set_page_config(page_title="기본 위젯", page_icon="🎨")

st.title("🎨 기본 입력 위젯")
st.write("사용자 입력을 받는 다양한 Streamlit 위젯들을 학습합니다.")

st.divider()

# 텍스트 입력
st.header("1. 텍스트 입력")

col1, col2 = st.columns(2)

with col1:
    st.subheader("st.text_input()")
    # YOUR CODE HERE - st.text_input()을 사용하여 이름 입력받기
    # name = st.text_input("이름을 입력하세요", placeholder="홍길동")
    if name:
        st.write(f"입력된 이름: **{name}**")

with col2:
    st.subheader("st.text_area()")
    # YOUR CODE HERE - st.text_area()를 사용하여 자기소개 입력받기
    # description = st.text_area("자기소개를 작성하세요", height=100)
    if description:
        st.write(f"글자 수: {len(description)}자")

st.divider()

# 숫자 입력
st.header("2. 숫자 입력")

col1, col2 = st.columns(2)

with col1:
    st.subheader("st.number_input()")
    age = st.number_input("나이", min_value=0, max_value=120, value=25, step=1)
    st.write(f"선택된 나이: **{age}세**")

with col2:
    st.subheader("st.slider()")
    height = st.slider("키(cm)", min_value=100.0, max_value=220.0, value=170.0, step=0.1)
    st.write(f"선택된 키: **{height}cm**")

st.divider()

# 선택 위젯
st.header("3. 선택 위젯")

col1, col2 = st.columns(2)

with col1:
    st.subheader("st.selectbox()")
    # YOUR CODE HERE - st.selectbox()를 사용하여 모델 선택
    # model = st.selectbox(
    #     "모델을 선택하세요",
    #     ["gpt-4.1-nano", "gpt-4.1-mini", "gpt-5-mini", "gpt-5-nano"],
    #     index=1
    # )
    st.write(f"선택된 모델: **{model}**")

with col2:
    st.subheader("st.radio()")
    gender = st.radio("성별", ["남성", "여성", "기타"])
    st.write(f"선택: **{gender}**")

st.divider()

# 다중 선택
st.header("4. 다중 선택")

st.subheader("st.multiselect()")
interests = st.multiselect(
    "관심사를 선택하세요 (여러 개 가능)",
    ["AI/ML", "웹개발", "데이터분석", "디자인", "마케팅", "창업"],
    default=["AI/ML"]
)
if interests:
    st.write(f"선택된 관심사: **{', '.join(interests)}**")

st.divider()

# 체크박스와 토글
st.header("5. 체크박스와 토글")

col1, col2 = st.columns(2)

with col1:
    st.subheader("st.checkbox()")
    # YOUR CODE HERE - st.checkbox()를 사용하여 약관 동의 받기
    # agree = st.checkbox("이용약관에 동의합니다")
    newsletter = st.checkbox("뉴스레터를 받겠습니다", value=True)
    
    if agree:
        st.success("✅ 약관에 동의했습니다")

with col2:
    st.subheader("st.toggle()")
    notifications = st.toggle("알림 활성화", value=True)
    dark_mode = st.toggle("다크 모드")
    
    st.write(f"알림: **{'ON' if notifications else 'OFF'}**")
    st.write(f"다크 모드: **{'ON' if dark_mode else 'OFF'}**")

st.divider()

# 날짜와 시간
st.header("6. 날짜와 시간")

col1, col2 = st.columns(2)

with col1:
    st.subheader("st.date_input()")
    birthday = st.date_input("생년월일", datetime.date(2000, 1, 1))
    st.write(f"선택된 날짜: **{birthday}**")

with col2:
    st.subheader("st.time_input()")
    meeting_time = st.time_input("회의 시간", datetime.time(14, 30))
    st.write(f"선택된 시간: **{meeting_time}**")

st.divider()

# 버튼
st.header("7. 버튼")

col1, col2, col3 = st.columns(3)

with col1:
    # YOUR CODE HERE - st.button()을 사용하여 기본 버튼 생성
    # if st.button("기본 버튼", use_container_width=True):
    #     st.info("기본 버튼이 클릭되었습니다!")
    pass

with col2:
    if st.button("Primary 버튼", type="primary", use_container_width=True):
        st.success("Primary 버튼이 클릭되었습니다!")

with col3:
    if st.button("🗑️ 삭제", use_container_width=True):
        st.warning("삭제 버튼이 클릭되었습니다!")

st.divider()

# 파일 업로드
st.header("8. 파일 업로드")

st.subheader("st.file_uploader()")
# YOUR CODE HERE - st.file_uploader()를 사용하여 파일 업로드
# uploaded_file = st.file_uploader(
#     "파일을 업로드하세요",
#     type=["txt", "csv", "json", "py"],
#     help="텍스트 파일만 지원됩니다"
# )

if uploaded_file is not None:
    st.success(f"✅ 파일 업로드 완료: **{uploaded_file.name}**")
    st.write(f"파일 크기: {uploaded_file.size} bytes")


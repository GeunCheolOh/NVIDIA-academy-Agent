import streamlit as st
import time
import pandas as pd
import numpy as np

st.set_page_config(page_title="고급 기능", page_icon="🚀", layout="wide")

st.title("🚀 고급 기능")
st.write("Streamlit의 고급 기능들을 학습합니다.")

st.divider()

# 프로그레스와 스피너
st.header("1. 로딩 표시")

col1, col2 = st.columns(2)

with col1:
    st.subheader("st.spinner()")
    if st.button("Spinner 시작", use_container_width=True):
        # YOUR CODE HERE - with st.spinner()를 사용하여 로딩 표시
        # with st.spinner("작업 중입니다..."):
        #     time.sleep(2)
        st.success("완료되었습니다!")

with col2:
    st.subheader("st.progress()")
    if st.button("Progress 시작", use_container_width=True):
        # YOUR CODE HERE - st.progress()를 사용하여 진행바 생성
        # progress_bar = st.progress(0)
        # for percent_complete in range(100):
        #     time.sleep(0.01)
        #     progress_bar.progress(percent_complete + 1)
        st.success("완료되었습니다!")

st.divider()

# Status 컨테이너
st.header("2. st.status() - 상태 표시")

if st.button("작업 실행", type="primary"):
    # YOUR CODE HERE - with st.status()를 사용하여 상태 표시
    # with st.status("작업 진행 중...", expanded=True) as status:
    #     st.write("1단계: 데이터 로딩 중...")
    #     time.sleep(1)
    #     st.write("✅ 데이터 로딩 완료")
    #     
    #     st.write("2단계: 데이터 처리 중...")
    #     time.sleep(1)
    #     st.write("✅ 데이터 처리 완료")
    #     
    #     st.write("3단계: 결과 저장 중...")
    #     time.sleep(1)
    #     st.write("✅ 결과 저장 완료")
    #     
    #     status.update(label="작업 완료!", state="complete", expanded=False)
    pass

st.divider()

# Toast 알림
st.header("3. st.toast() - 알림 메시지")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("Info 알림", use_container_width=True):
        # YOUR CODE HERE - st.toast()를 사용하여 알림 표시
        # st.toast("정보 알림입니다!", icon="ℹ️")
        pass

with col2:
    if st.button("Success 알림", use_container_width=True):
        st.toast("성공적으로 완료되었습니다!", icon="✅")

with col3:
    if st.button("Warning 알림", use_container_width=True):
        st.toast("주의가 필요합니다!", icon="⚠️")

with col4:
    if st.button("Error 알림", use_container_width=True):
        st.toast("오류가 발생했습니다!", icon="❌")

st.caption("Toast는 화면 우측 하단에 잠깐 나타났다 사라지는 알림입니다.")

st.divider()

# Balloons와 Snow
st.header("4. 축하 효과")

col1, col2 = st.columns(2)

with col1:
    if st.button("🎈 풍선!", use_container_width=True):
        st.balloons()

with col2:
    if st.button("❄️ 눈!", use_container_width=True):
        st.snow()

st.caption("축하 이벤트나 특별한 순간에 사용할 수 있는 애니메이션 효과입니다.")

st.divider()

# Download 버튼
st.header("5. st.download_button() - 다운로드")

# CSV 다운로드
df = pd.DataFrame({
    '이름': ['김철수', '이영희', '박지민'],
    '나이': [25, 30, 28],
    '직업': ['개발자', '디자이너', '기획자']
})

csv = df.to_csv(index=False).encode('utf-8')

col1, col2 = st.columns(2)

with col1:
    st.subheader("CSV 다운로드")
    st.dataframe(df)
    # YOUR CODE HERE - st.download_button()을 사용하여 다운로드 버튼 생성
    # st.download_button(
    #     label="📥 CSV 다운로드",
    #     data=csv,
    #     file_name='sample_data.csv',
    #     mime='text/csv',
    #     use_container_width=True
    # )

with col2:
    st.subheader("텍스트 다운로드")
    text_content = """안녕하세요!
이것은 샘플 텍스트 파일입니다.
Streamlit으로 생성되었습니다."""
    
    st.text_area("내용", text_content, height=100)
    st.download_button(
        label="📥 TXT 다운로드",
        data=text_content,
        file_name='sample.txt',
        mime='text/plain',
        use_container_width=True
    )

st.divider()

# Form
st.header("6. st.form() - 폼 제출")

st.write("Form을 사용하면 여러 입력을 한 번에 제출할 수 있습니다.")

# YOUR CODE HERE - with st.form()을 사용하여 폼 생성
# with st.form("user_form"):
#     st.subheader("사용자 정보 입력")
#     
#     col1, col2 = st.columns(2)
#     
#     with col1:
#         name = st.text_input("이름")
#         email = st.text_input("이메일")
#     
#     with col2:
#         age = st.number_input("나이", min_value=0, max_value=120, value=25)
#         job = st.selectbox("직업", ["개발자", "디자이너", "기획자", "기타"])
#     
#     message = st.text_area("메시지")
#     
#     submitted = st.form_submit_button("제출", type="primary", use_container_width=True)
#     
#     if submitted:
#         st.success("폼이 제출되었습니다!")
#         st.json({
#             "이름": name,
#             "이메일": email,
#             "나이": age,
#             "직업": job,
#             "메시지": message
#         })

st.divider()

# Echo
st.header("7. st.echo() - 코드와 결과 함께 표시")

st.write("st.echo()를 사용하면 코드를 실행하면서 동시에 표시할 수 있습니다.")

with st.echo():
    # 이 코드는 실행되면서 동시에 화면에 표시됩니다
    import pandas as pd
    
    data = pd.DataFrame({
        'x': [1, 2, 3, 4, 5],
        'y': [10, 20, 30, 40, 50]
    })
    
    st.line_chart(data.set_index('x'))

st.divider()

# Help
st.header("8. st.help() - 도움말 표시")

st.write("함수나 객체의 도움말을 표시할 수 있습니다.")

if st.checkbox("st.dataframe() 도움말 보기"):
    st.help(st.dataframe)

st.divider()

# 페이지 설정 정보
st.header("9. 페이지 설정 옵션")

st.write("""
**st.set_page_config()**로 페이지 전체 설정을 할 수 있습니다:

```python
st.set_page_config(
    page_title="앱 제목",
    page_icon="🚀",
    layout="wide",  # "centered" 또는 "wide"
    initial_sidebar_state="expanded",  # "auto", "expanded", "collapsed"
    menu_items={
        'Get Help': 'https://www.example.com/help',
        'Report a bug': "https://www.example.com/bug",
        'About': "# 내 멋진 앱!"
    }
)
```

⚠️ 이 함수는 스크립트 맨 위에서 **한 번만** 호출해야 합니다.
""")

st.divider()

# 실용적인 조합 예제
st.header("10. 실용 예제: 데이터 분석 워크플로우")

if st.button("🚀 분석 시작", type="primary"):
    with st.status("데이터 분석 진행 중...", expanded=True) as status:
        # 1단계: 데이터 생성
        st.write("📊 1단계: 데이터 생성 중...")
        progress = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress.progress(i + 1)
        
        data = pd.DataFrame(
            np.random.randn(100, 3),
            columns=['A', 'B', 'C']
        )
        st.write("✅ 데이터 생성 완료")
        
        # 2단계: 분석
        st.write("🔍 2단계: 데이터 분석 중...")
        with st.spinner("분석 중..."):
            time.sleep(1)
        st.write("✅ 분석 완료")
        
        # 3단계: 시각화
        st.write("📈 3단계: 시각화 생성 중...")
        time.sleep(0.5)
        st.line_chart(data)
        st.write("✅ 시각화 완료")
        
        status.update(label="분석 완료!", state="complete", expanded=False)
    
    st.balloons()
    st.toast("모든 작업이 완료되었습니다!", icon="🎉")
    
    # 결과 다운로드
    csv = data.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 결과 다운로드",
        data=csv,
        file_name='analysis_result.csv',
        mime='text/csv',
        type="primary"
    )


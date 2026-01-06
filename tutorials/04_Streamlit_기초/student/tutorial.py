import streamlit as st

# 페이지 설정
st.set_page_config(page_title="기본 컴포넌트", page_icon="📝")

# 제목과 헤더
st.title("📝 Streamlit 기본 컴포넌트")
st.header("1. 텍스트 표시")
st.subheader("다양한 텍스트 스타일")

# 일반 텍스트 출력
st.write("**st.write()**: 가장 범용적인 출력 함수입니다.")
st.markdown("**st.markdown()**: *마크다운* 문법을 지원합니다.")
st.caption("st.caption(): 작은 글씨로 표시되는 부가 설명입니다.")

st.divider()

# 특별한 메시지 표시
st.header("2. 메시지 박스")

# YOUR CODE HERE - st.columns(2)를 사용하여 2개의 컬럼 생성
# col1, col2 = ...

with col1:
    # YOUR CODE HERE - st.success()와 st.info()를 사용하여 메시지 표시
    # st.success("✅ st.success(): 성공 메시지")
    # st.info(...)
    pass

with col2:
    # YOUR CODE HERE - st.warning()과 st.error()를 사용하여 메시지 표시
    # st.warning(...)
    # st.error(...)
    pass

st.divider()

# 코드 표시
st.header("3. 코드 표시")

code = '''def hello():
    print("Hello, Streamlit!")
    return "환영합니다!"'''

st.code(code, language='python')

st.divider()

# 데이터 표시
st.header("4. 데이터 표시")

import pandas as pd
import numpy as np

data = pd.DataFrame({
    '이름': ['김철수', '이영희', '박지민'],
    '나이': [25, 30, 28],
    '직업': ['개발자', '디자이너', '기획자']
})

col1, col2 = st.columns(2)

with col1:
    st.subheader("st.dataframe() - 동적 테이블")
    # YOUR CODE HERE - st.dataframe()을 사용하여 데이터프레임 표시
    # st.dataframe(data, use_container_width=True)

with col2:
    st.subheader("st.table() - 정적 테이블")
    st.table(data)

st.divider()

# JSON 표시
st.header("5. JSON 데이터")

json_data = {
    "name": "Streamlit Tutorial",
    "version": "1.0",
    "features": ["widgets", "layout", "chat"]
}

# YOUR CODE HERE - st.json()을 사용하여 JSON 데이터 표시
# st.json(...)

st.divider()

# 메트릭 표시
st.header("6. 메트릭 카드")

col1, col2, col3 = st.columns(3)

# YOUR CODE HERE - col1.metric(), col2.metric(), col3.metric()을 사용하여 메트릭 표시
# col1.metric("온도", "25°C", "1.2°C")
# col2.metric(...)
# col3.metric(...)


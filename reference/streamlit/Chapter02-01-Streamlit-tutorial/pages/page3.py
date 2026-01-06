import streamlit as st
import numpy as np
import pandas as pd

# 사이드바에 제목 추가
st.sidebar.header("설정")

# 사이드바에 컨트롤 추가
display_mode = st.sidebar.radio("표시 모드", ["기본", "상세", "요약"])
temperature = st.sidebar.slider("온도 설정", 0.0, 1.0, 0.5)
use_cache = st.sidebar.checkbox("캐시 사용", value=True)

# 사이드바에 버튼 추가
if st.sidebar.button("적용"):
    st.success("설정이 적용되었습니다!")
    
col1, col2 = st.columns(2)  # 화면을 두 개의 동일한 크기 컬럼으로 나눔

with col1:
    st.header("첫 번째 컬럼")
    st.image("https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.svg")
    st.write("왼쪽 컬럼의 내용입니다.")

with col2:
    st.header("두 번째 컬럼")
    st.write("오른쪽 컬럼의 내용입니다.")
    chart_data = pd.DataFrame(np.random.randn(20, 1), columns=["데이터"])
    st.line_chart(chart_data)

# 비율을 조정할 수도 있습니다
col1, col2, col3 = st.columns([1, 2, 1])  # 비율 1:2:1로 세 개의 컬럼 생성

tab1, tab2, tab3 = st.tabs(["차트", "데이터", "설정"])

with tab1:
    st.header("차트")
    chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["A", "B", "C"])
    st.line_chart(chart_data)

with tab2:
    st.header("데이터")
    st.dataframe(chart_data)

with tab3:
    st.header("설정")
    st.write("차트 설정을 변경할 수 있습니다.")
    chart_type = st.radio("차트 유형", ["선 그래프", "막대 그래프", "영역 그래프"])
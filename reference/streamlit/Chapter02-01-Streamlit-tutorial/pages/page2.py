import streamlit as st
import pandas as pd
import numpy as np

# 간단한 데이터프레임 표시
data = pd.DataFrame({
    "이름": ["김철수", "이영희", "박지민", "최동욱"],
    "나이": [24, 31, 19, 27],
    "직업": ["학생", "개발자", "디자이너", "교사"]
})
st.dataframe(data)

# 정적 테이블
st.table(data)

# 차트 그리기
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=["A", "B", "C"]
)
st.line_chart(chart_data)
st.bar_chart(chart_data)
        

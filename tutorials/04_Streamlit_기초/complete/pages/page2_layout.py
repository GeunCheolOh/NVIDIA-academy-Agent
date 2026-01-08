import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="레이아웃", page_icon="📐", layout="wide")

st.title("📐 레이아웃 구성")
st.write("Streamlit의 다양한 레이아웃 구성 요소를 학습합니다.")

st.divider()

# 사이드바
st.header("1. st.sidebar - 사이드바")

with st.sidebar:
    st.header("⚙️ 설정 패널")
    
    st.subheader("모델 설정")
    model = st.selectbox("모델 선택", ["GPT-4", "GPT-3.5", "Claude"])
    temperature = st.slider("Temperature", 0.0, 2.0, 0.7, 0.1)
    
    st.divider()
    
    st.subheader("표시 옵션")
    show_details = st.checkbox("상세 정보 표시", value=True)
    
    st.divider()
    
    if st.button("설정 적용", type="primary", use_container_width=True):
        st.success("설정이 적용되었습니다!")

st.info("👈 왼쪽 사이드바를 확인해보세요!")
st.write(f"선택된 모델: **{model}**, Temperature: **{temperature}**")

st.divider()

# 컬럼
st.header("2. st.columns() - 컬럼 레이아웃")

st.subheader("2-1. 동일한 비율의 컬럼")
col1, col2, col3 = st.columns(3)

with col1:
    st.info("**첫 번째 컬럼**")
    st.write("1:1:1 비율")
    st.metric("방문자", "1,234", "+12%")

with col2:
    st.info("**두 번째 컬럼**")
    st.write("동일한 너비")
    st.metric("조회수", "5,678", "+8%")

with col3:
    st.info("**세 번째 컬럼**")
    st.write("균등 분할")
    st.metric("댓글", "89", "-3%")

st.subheader("2-2. 다른 비율의 컬럼")
col1, col2 = st.columns([2, 1])

with col1:
    st.warning("**넓은 컬럼 (2)**")
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['A', 'B', 'C']
    )
    st.line_chart(chart_data)

with col2:
    st.warning("**좁은 컬럼 (1)**")
    st.write("2:1 비율로 설정")
    st.write("차트와 설명을 나란히 배치")

st.divider()

# 탭
st.header("3. st.tabs() - 탭 레이아웃")

tab1, tab2, tab3, tab4 = st.tabs(["📊 차트", "📋 데이터", "⚙️ 설정", "ℹ️ 정보"])

with tab1:
    st.subheader("차트 보기")
    chart_type = st.radio("차트 종류", ["선 그래프", "막대 그래프", "영역 그래프"], horizontal=True)
    
    data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['매출', '비용', '이익']
    )
    
    if chart_type == "선 그래프":
        st.line_chart(data)
    elif chart_type == "막대 그래프":
        st.bar_chart(data)
    else:
        st.area_chart(data)

with tab2:
    st.subheader("데이터 테이블")
    st.dataframe(data, use_container_width=True)
    st.caption(f"총 {len(data)}개 행")

with tab3:
    st.subheader("차트 설정")
    show_legend = st.checkbox("범례 표시", value=True)
    chart_height = st.slider("차트 높이", 200, 600, 400)
    st.info(f"설정 - 범례: {show_legend}, 높이: {chart_height}px")

with tab4:
    st.subheader("정보")
    st.write("이 탭 레이아웃은 여러 뷰를 하나의 공간에 구성하는데 유용합니다.")
    st.write("사용자가 원하는 탭을 선택하여 내용을 볼 수 있습니다.")

st.divider()

# Expander
st.header("4. st.expander() - 확장 가능한 섹션")

with st.expander("📚 자세한 설명 보기"):
    st.write("""
    **Expander**는 많은 내용을 숨겨두고 필요할 때만 펼쳐볼 수 있게 해줍니다.
    
    주요 사용 사례:
    - FAQ 섹션
    - 상세 설명
    - 디버그 정보
    - 긴 코드 블록
    """)
    
    code = '''def process_data(data):
    # 데이터 처리 로직
    result = data.apply(lambda x: x * 2)
    return result'''
    
    st.code(code, language='python')

with st.expander("⚙️ 고급 설정", expanded=True):
    st.write("이 expander는 기본적으로 열려있습니다 (expanded=True)")
    
    col1, col2 = st.columns(2)
    with col1:
        max_retries = st.number_input("최대 재시도", 1, 10, 3)
    with col2:
        timeout = st.number_input("타임아웃(초)", 1, 60, 10)

st.divider()

# 구분선
st.header("5. st.divider() - 구분선")

st.write("st.divider()를 사용하면 섹션을 명확히 구분할 수 있습니다.")
st.divider()
st.write("위에 구분선이 표시됩니다.")

st.markdown("---")
st.write("st.markdown('---')도 비슷한 효과를 냅니다.")

st.divider()

# 컨테이너
st.header("6. st.container() - 컨테이너")

container = st.container(border=True)
container.write("이것은 테두리가 있는 컨테이너입니다.")
container.metric("컨테이너 내부", "42", "+5")

st.write("컨테이너는 요소들을 그룹화하는데 유용합니다.")


import streamlit as st
import pandas as pd

# 제목
st.title("2025년 5월 기준 연령별 인구 현황 분석")

# 데이터 불러오기
file_path = "202505_202505_연령별인구현황_월간.csv"
df = pd.read_csv(file_path, encoding="euc-kr")

# 원본 데이터 표시
st.subheader("📄 원본 데이터")
st.dataframe(df)

# 총인구수 기준 상위 5개 행정구역 선택
top5_df = df.sort_values(by='총인구수', ascending=False).head(5)

# 연령별 컬럼 선택 및 전처리
age_columns = [col for col in df.columns if col.startswith('2025년05월_계_')]
age_only = [col.replace('2025년05월_계_', '') for col in age_columns]

# 시각화용 데이터 구성
plot_data = top5_df[['행정구역(읍면동)별'] + age_columns].copy()
plot_data.columns = ['지역'] + age_only
plot_data = plot_data.set_index('지역').T

# 시각화
st.subheader("📊 연령별 인구 분포 (상위 5개 지역)")
st.line_chart(plot_data)

# 출처 및 안내
st.caption("출처: 통계청 인구 현황 데이터 (2025년 5월 기준)")

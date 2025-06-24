import streamlit as st
import pandas as pd

def app():
    st.title('대한민국 연령대별 인구 분포 (상위 5개 행정구역 기준)')

    # 데이터 불러오기 ('euc-kr' 인코딩 사용)
    df = pd.read_csv('202505_202505_연령별인구현황_월간.csv', encoding='euc-kr')

    # 행정구역 정제
    df['행정구역'] = df['행정구역'].astype(str).str.split(' ').str[0]

    # 열 이름 정제
    new_columns = []
    for col in df.columns:
        if '2025년05월_계_' in col:
            new_columns.append(col.replace('2025년05월_계_', ''))
        elif '2025년05월_남_' in col:
            new_columns.append('남_' + col.replace('2025년05월_남_', ''))
        elif '2025년05월_여_' in col:
            new_columns.append('여_' + col.replace('2025년05월_여_', ''))
        else:
            new_columns.append(col)
    df.columns = new_columns

    # 숫자형 변환
    numeric_cols = [col for col in df.columns if col != '행정구역']
    for col in numeric_cols:
        df[col] = df[col].astype(str).str.replace(',', '', regex=False).astype(int)

    # 상위 5개 지역 추출
    top5_regions = df.sort_values(by='총인구수', ascending=False).head(5)['행정구역'].tolist()
    df_top5 = df[df['행정구역'].isin(top5_regions)].copy()

    # -----------------------------
    # 📊 전체 인구 기준 연령 분포
    # -----------------------------
    st.write("---")
    st.header("원본 데이터")
    st.dataframe(df)

    st.write("---")
    st.header("상위 5개 행정구역의 연령대별 총인구 분포")
    df_total = df_top5.melt(id_vars=['행정구역'], 
                            value_vars=[col for col in df_top5.columns if col.isdigit()],
                            var_name='연령', 
                            value_name='인구수')
    df_total['연령'] = df_total['연령'].astype(int)
    total_pivot = df_total.pivot_table(index='연령', columns='행정구역', values='인구수')
    st.line_chart(total_pivot)

    # -----------------------------
    # 👩‍🦰👨‍🦱 성별 인구 분포
    # -----------------------------
    st.write("---")
    st.header("상위 5개 행정구역의 연령대별 성별 인구 분포")

    gender_cols = [col for col in df_top5.columns if col.startswith('남_') or col.startswith('여_')]
    df_gender = df_top5.melt(id_vars=['행정구역'], 
                             value_vars=gender_cols, 
                             var_name='성별연령', 
                             value_name='인구수')

    # 성별과 연령 분리
    df_gender['성별'] = df_gender['성별연령'].str.extract(r'(남|여)')
    df_gender['연령'] = df_gender['성별연령'].str.extract(r'(\d+)').astype(int)
    df_gender = df_gender.drop(columns='성별연령')

    # 사용자 선택: 성별
    selected_gender = st.radio("성별을 선택하세요", ('남', '여'))

    df_selected = df_gender[df_gender['성별'] == selected_gender]
    gender_pivot = df_selected.pivot_table(index='연령', columns='행정구역', values='인구수')
    st.line_chart(gender_pivot)

if __name__ == '__main__':
    app()

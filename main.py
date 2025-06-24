import streamlit as st
import pandas as pd

# 열 이름 정리 함수
def 정제_열이름(df, 접두사):
    새로운_열 = []
    for 열 in df.columns:
        if 열.startswith(접두사):
            label = 열.replace(접두사, '')
            if '총인구수' in label:
                새로운_열.append('총인구수')
            elif '연령구간인구수' in label:
                새로운_열.append('연령구간인구수')
            else:
                새로운_열.append(label)
        else:
            새로운_열.append(열)
    df.columns = 새로운_열
    return df

# 숫자형 변환 함수
def 숫자_형변환(df):
    숫자열 = [열 for 열 in df.columns if 열 != '행정구역']
    for 열 in 숫자열:
        df[열] = df[열].astype(str).str.replace(',', '', regex=False).astype(int)
    return df

def app():
    st.title("📊 대한민국 연령대별 인구 분포 (상위 5개 행정구역 기준)")

    # 1. 전체 인구 파일 불러오기
    df_전체 = pd.read_csv('202505_202505_연령별인구현황_월간.csv', encoding='euc-kr')
    df_전체['행정구역'] = df_전체['행정구역'].astype(str).str.split(' ').str[0]
    df_전체 = 정제_열이름(df_전체, '2025년05월_계_')
    df_전체 = 숫자_형변환(df_전체)

    # 2. 성별 인구 파일 불러오기
    df_성별 = pd.read_csv('202505_202505_연령별인구현황_월간 (1).csv', encoding='euc-kr')
    df_성별['행정구역'] = df_성별['행정구역'].astype(str).str.split(' ').str[0]

    열목록 = []
    for 열 in df_성별.columns:
        if 열.startswith('2025년05월_남_'):
            열목록.append('남_' + 열.replace('2025년05월_남_', ''))
        elif 열.startswith('2025년05월_여_'):
            열목록.append('여_' + 열.replace('2025년05월_여_', ''))
        else:
            열목록.append(열)
    df_성별.columns = 열목록
    df_성별 = 숫자_형변환(df_성별)

    # 3. 총인구 기준 상위 5개 행정구역 추출
    상위5 = df_전체.sort_values(by='총인구수', ascending=False).head(5)['행정구역'].tolist()
    df_전체_상위5 = df_전체[df_전체['행정구역'].isin(상위5)].copy()
    df_성별_상위5 = df_성별[df_성별['행정구역'].isin(상위5)].copy()

    # 4. 전체 인구 시각화
    st.subheader("🔹 상위 5개 행정구역의 연령대별 총인구 분포")
    df_전체_변환 = df_전체_상위5.melt(
        id_vars=['행정구역', '총인구수', '연령구간인구수'],
        var_name='연령',
        value_name='인구수'
    )
    df_전체_변환['연령'] = df_전체_변환['연령'].str.extract(r'(\d+)')
    df_전체_변환 = df_전체_변환.dropna(subset=['연령'])
    df_전체_변환['연령'] = df_전체_변환['연령'].astype(int)
    피벗_전체 = df_전체_변환.pivot_table(index='연령', columns='행정구역', values='인구수')
    st.line_chart(피벗_전체)

    # 5. 성별 인구 시각화
    st.subheader("🔹 상위 5개 행정구역의 연령대별 성별 인구 분포")
    성별_선택 = st.radio("성별 선택", options=['남', '여'], horizontal=True)

    # '남_00' 또는 '여_00' 열만 필터링
    선택열 = [열 for 열 in df_성별_상위5.columns if 열.startswith(성별_선택 + '_') and 열.replace(성별_선택 + '_', '').isdigit()]
    df_선택 = df_성별_상위5[['행정구역'] + 선택열].copy()

    df_성별변환 = df_선택.melt(id_vars=['행정구역'],
                             var_name='연령',
                             value_name='인구수')
    df_성별변환['연령'] = df_성별변환['연령'].str.extract(r'(\d+)')
    df_성별변환 = df_성별변환.dropna(subset=['연령'])
    df_성별변환['연령'] = df_성별변환['연령'].astype(int)
    피벗_성별 = df_성별변환.pivot_table(index='연령', columns='행정구역', values='인구수')
    st.line_chart(피벗_성별)

    # 6. 원본 데이터 보기
    with st.expander("📄 원본 데이터 보기"):
        st.write("전체 인구 데이터")
        st.dataframe(df_전체)
        st.write("성별 인구 데이터")
        st.dataframe(df_성별)

if __name__ == '__main__':
    app()


import streamlit as st
import pandas as pd

def 정제_열이름(df, 접두사):
    """열 이름에서 접두사 제거하고 나이만 남기기"""
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

def 숫자_형변환(df):
    """쉼표 제거 후 숫자형 변환"""
    숫자열 = [열 for 열 in df.columns if 열 != '행정구역']
    for 열 in 숫자열:
        df[열] = df[열].astype(str).str.replace(',', '', regex=False).astype(int)
    return df

def app():
    st.title("📊 대한민국 연령대별 인구 분포 (상위 5개 행정구역 기준)")

    # ⬇️ 전체 인구 파일
    df_전체 = pd.read_csv('202505_202505_연령별인구현황_월간.csv', encoding='euc-kr')
    df_전체['행정구역'] = df_전체['행정구역'].astype(str).str.split(' ').str[0]
    df_전체 = 정제_열이름(df_전체, '2025년05월_계_')
    df_전체 = 숫자_형변환(df_전체)

    # ⬇️ 성별 인구 파일
    df_성별 = pd.read_csv('202505_202505_연령별인구현황_월간 (1).csv', encoding='euc-kr')
    df_성별['행정구역'] = df_성별['행정구역'].astype(str).str.split(' ').str[0]

    # 열 이름 정제 (남/여)
    열목록 = []
    for 열 in df_성별.columns:
        if 열.startswith('2025년05월_남_'):
            열목록.append('남_' + 열.replace('2025년05월_남_', ''))
        elif 열.startswith('2025년05월

import streamlit as st
st.title('나의 첫 웹앱 by 제인킴')
st.write('우와! 이게 된다고?!!!')
import streamlit as st

# MBTI별 직업 추천 데이터
mbti_jobs = {
    "INTJ": ["전략 컨설턴트", "데이터 과학자", "시스템 분석가"],
    "INTP": ["연구원", "프로그래머", "이론 물리학자"],
    "ENTJ": ["경영 컨설턴트", "프로젝트 매니저", "변호사"],
    "ENTP": ["창업가", "마케팅 디렉터", "광고 기획자"],
    "INFJ": ["상담가", "작가", "심리학자"],
    "INFP": ["예술가", "사회복지사", "교사"],
    "ENFJ": ["인사 관리자", "정치가", "교육자"],
    "ENFP": ["기획자", "기자", "공공 관계 전문가"],
    "ISTJ": ["회계사", "공무원", "법률 전문가"],
    "ISFJ": ["간호사", "초등학교 교사", "행정 보조"],
    "ESTJ": ["운영 관리자", "은행원", "감독관"],
    "ESFJ": ["서비스 매니저", "상담사", "세일즈 담당자"],
    "ISTP": ["기술자", "파일럿", "응급 구조사"],
    "ISFP": ["디자이너", "수의사", "요리사"],
    "ESTP": ["영업 대표", "구조대원", "이벤트 플래너"],
    "ESFP": ["연예인", "방송인", "관광 가이드"]
}

# 페이지 제목
st.title("MBTI 기반 직업 추천기")

# 설명 텍스트
st.write("아래에서 당신의 MBTI를 선택하면, 해당 성격 유형에 어울리는 직업을 추천해드립니다.")

# 사용자 입력: MBTI 선택
mbti_list = list(mbti_jobs.keys())
selected_mbti = st.selectbox("당신의 MBTI를 선택하세요:", sorted(mbti_list))

# 결과 출력
if selected_mbti:
    st.subheader(f"{selected_mbti} 유형에 어울리는 직업 추천")
    for job in mbti_jobs[selected_mbti]:
        st.markdown(f"- {job}")

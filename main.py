import streamlit as st
import random

st.set_page_config(
    page_title="MBTI 진로 추천",
    page_icon="🚀",
    layout="wide"
)

# -------------------
# 스타일
# -------------------
st.markdown("""
<style>
.main {
    background: linear-gradient(135deg,#667eea 0%,#764ba2 100%);
}

.title {
    text-align:center;
    color:white;
    font-size:3rem;
    font-weight:800;
    margin-bottom:10px;
}

.subtitle{
    text-align:center;
    color:white;
    font-size:1.2rem;
    margin-bottom:30px;
}

.result-card{
    background:white;
    padding:25px;
    border-radius:20px;
    box-shadow:0 10px 30px rgba(0,0,0,0.2);
    animation:fadeIn 0.8s;
}

.job-card{
    background:linear-gradient(135deg,#f6f9fc,#ffffff);
    border-left:6px solid #6c63ff;
    padding:15px;
    margin:10px 0;
    border-radius:15px;
    font-size:20px;
    font-weight:600;
}

.mbti-box{
    background:rgba(255,255,255,0.15);
    padding:15px;
    border-radius:15px;
    color:white;
    text-align:center;
}

@keyframes fadeIn{
    from{
        opacity:0;
        transform:translateY(20px);
    }
    to{
        opacity:1;
        transform:translateY(0);
    }
}
</style>
""", unsafe_allow_html=True)

# -------------------
# MBTI 데이터
# -------------------
mbti_jobs = {
    "INTJ": ["데이터 과학자", "AI 개발자", "연구원", "전략기획가", "건축가"],
    "INTP": ["프로그래머", "게임 개발자", "물리학자", "발명가", "시스템 분석가"],
    "ENTJ": ["CEO", "기업 컨설턴트", "프로젝트 매니저", "변호사", "정치인"],
    "ENTP": ["창업가", "마케터", "광고기획자", "PD", "발명가"],

    "INFJ": ["상담교사", "심리학자", "작가", "사회복지사", "교육기획자"],
    "INFP": ["작가", "웹툰 작가", "디자이너", "예술가", "콘텐츠 크리에이터"],
    "ENFJ": ["교사", "강사", "인사담당자", "상담사", "교육전문가"],
    "ENFP": ["유튜버", "광고기획자", "방송작가", "여행기획자", "마케터"],

    "ISTJ": ["공무원", "회계사", "품질관리자", "은행원", "행정전문가"],
    "ISFJ": ["간호사", "초등교사", "사회복지사", "보건교사", "사서"],
    "ESTJ": ["경영자", "군인", "경찰관", "행정관리자", "영업관리자"],
    "ESFJ": ["승무원", "교사", "간호사", "이벤트 기획자", "호텔리어"],

    "ISTP": ["정비사", "파일럿", "엔지니어", "드론 전문가", "소방관"],
    "ISFP": ["그래픽 디자이너", "사진작가", "플로리스트", "패션 디자이너", "음악가"],
    "ESTP": ["기업가", "스포츠 선수", "영업전문가", "경찰관", "응급구조사"],
    "ESFP": ["연예인", "방송인", "행사기획자", "유튜버", "관광가이드"]
}

descriptions = {
    "INTJ":"전략적 사고와 분석력이 뛰어난 유형",
    "INTP":"창의적 문제 해결을 좋아하는 유형",
    "ENTJ":"리더십과 추진력이 강한 유형",
    "ENTP":"새로운 아이디어를 즐기는 혁신가",

    "INFJ":"통찰력과 공감 능력이 뛰어난 유형",
    "INFP":"이상적이고 창의적인 유형",
    "ENFJ":"사람을 이끄는 따뜻한 리더",
    "ENFP":"열정과 상상력이 풍부한 유형",

    "ISTJ":"성실하고 책임감 있는 유형",
    "ISFJ":"배려심 많고 헌신적인 유형",
    "ESTJ":"체계적이고 실용적인 리더",
    "ESFJ":"사교적이고 협력적인 유형",

    "ISTP":"도전과 실습을 좋아하는 유형",
    "ISFP":"감각적이고 예술적인 유형",
    "ESTP":"활동적이고 모험적인 유형",
    "ESFP":"즐거움을 만드는 에너지 넘치는 유형"
}

# -------------------
# 헤더
# -------------------
st.markdown(
    "<div class='title'>🚀 MBTI 진로 탐험대 🚀</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='subtitle'>나의 MBTI를 선택하고 미래 직업을 찾아보세요!</div>",
    unsafe_allow_html=True
)

# -------------------
# 선택
# -------------------
mbti = st.selectbox(
    "🧠 MBTI를 선택하세요",
    list(mbti_jobs.keys())
)

# -------------------
# 결과
# -------------------
if st.button("✨ 직업 추천 받기", use_container_width=True):

    jobs = mbti_jobs[mbti]
    random.shuffle(jobs)

    st.balloons()

    st.markdown(
        f"""
        <div class='result-card'>
            <h1 style='text-align:center;'>🎯 {mbti}</h1>
            <p style='text-align:center;font-size:20px;'>
            {descriptions[mbti]}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    st.subheader("🌟 추천 직업")

    for job in jobs:
        st.markdown(
            f"""
            <div class='job-card'>
            🚀 {job}
            </div>
            """,
            unsafe_allow_html=True
        )

    st.success("💡 MBTI는 참고 자료일 뿐! 다양한 경험을 통해 자신의 적성을 찾아보세요.")

# -------------------
# 하단
# -------------------
st.markdown("---")
st.markdown(
    "<center>🎓 진로 탐색은 가능성을 발견하는 첫걸음입니다.</center>",
    unsafe_allow_html=True
)

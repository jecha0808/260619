import streamlit as st

# 1. 페이지 기본 설정 및 디자인 (CSS)
st.set_page_config(
    page_title="미래를 찾는 MBTI 진로 탐색",
    page_icon="🚀",
    layout="centered"
)

# 예쁜 UI를 위한 커스텀 CSS injection
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .title-container {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .job-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #667eea;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .recommend-title {
        color: #764ba2;
        font-weight: bold;
    }
    </style>
""", unsafe_allowed_html=True)

# 2. 상단 타이틀 배너
st.markdown("""
    <div class="title-container">
        <h1>🚀 내 성격에 딱 맞는 직업은?</h1>
        <p style="font-size: 1.2rem; margin-top: 0.5rem;">MBTI로 알아보는 재미있는 나의 미래 진로 탐색</p>
    </div>
""", unsafe_allowed_html=True)

# 3. 데이터 정의 (4가지 성격 그룹별 직업 데이터)
mbti_jobs = {
    # 분석가형 (NT)
    "INTJ": {"title": "📐 전략적인 설계자", "jobs": ["AI 연구원", "데이터 과학자", "투자 분석가", "소프트웨어 아키텍트"], "desc": "논리적이고 독립적이며, 복잡한 문제를 해결하는 시스템을 만드는 것을 좋아해요."},
    "INTP": {"title": "💡 호기심 많은 사색가", "jobs": ["컴퓨터 프로그래머", "대학 교수", "연구원", "게임 디자이너"], "desc": "아이디어가 풍부하고 분석적이며, 새로운 지식을 탐구하고 혁신을 일으키는 것을 즐겨요."},
    "ENTJ": {"title": "👑 대담한 통솔자", "jobs": ["경영 CEO", "프로젝트 매니저", "정치인", "경영 컨설턴트"], "desc": "철저하게 계획하고 사람들을 이끌며, 목표를 달성하는 카리스마를 가지고 있어요."},
    "ENTP": {"title": "🔥 뜨거운 논쟁을 즐기는 변론가", "jobs": ["창업가(스타트업)", "마케팅 디렉터", "영화 감독", "변호사"], "desc": "도전적인 과제를 좋아하고 호기심이 많아, 새로운 아이디어를 제안하는 일에 탁월해요."},
    
    # 외교관형 (NF)
    "INFJ": {"title": "🌟 선의의 옹호자", "jobs": ["심리 상담사", "작가", "교사/학습 코치", "환경 운동가"], "desc": "사람들의 성장을 돕고 사회에 긍정적인 영향을 주는 의미 있는 일을 선호해요."},
    "INFP": {"title": "🎨 열정적인 중재자", "jobs": ["일러스트레이터", "소설가/웹툰 작가", "정신건강 의학과 의사", "인사담당자"], "desc": "예술적 감수성이 풍부하고 자신의 가치관을 진정성 있게 표현하는 일을 좋아해요."},
    "ENFJ": {"title": "🤝 정의로운 사회운동가", "jobs": ["비영리단체 운영자", "아나운서/PD", "커리어 코치", "외교관"], "desc": "타인의 마음을 잘 이해하고 영감을 주며, 함께 협동하여 더 나은 세상을 만듭니다."},
    "ENFP":

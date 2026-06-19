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

# 3. 데이터 정의 (괄호 매칭 오류를 방지하기 위해 깔끔하게 정리)
mbti_jobs = {
    "INTJ": {"title": "📐 전략적인 설계자", "jobs": ["AI 연구원", "데이터 과학자", "투자 분석가", "소프트웨어 아키텍트"], "desc": "논리적이고 독립적이며, 복잡한 문제를 해결하는 시스템을 만드는 것을 좋아해요."},
    "INTP": {"title": "💡 호기심 많은 사색가", "jobs": ["컴퓨터 프로그래머", "대학 교수", "연구원", "게임 디자이너"], "desc": "아이디어가 풍부하고 분석적이며, 새로운 지식을 탐구하고 혁신을 일으키는 것을 즐겨요."},
    "ENTJ": {"title": "👑 대담한 통솔자", "jobs": ["경영 CEO", "프로젝트 매니저", "정치인", "경영 컨설턴트"], "desc": "철저하게 계획하고 사람들을 이끌며, 목표를 달성하는 카리스마를 가지고 있어요."},
    "ENTP": {"title": "🔥 뜨거운 논쟁을 즐기는 변론가", "jobs": ["창업가(스타트업)", "마케팅 디렉터", "영화 감독", "변호사"], "desc": "도전적인 과제를 좋아하고 호기심이 많아, 새로운 아이디어를 제안하는 일에 탁월해요."},
    "INFJ": {"title": "🌟 선의의 옹호자", "jobs": ["심리 상담사", "작가", "교사/학습 코치", "환경 운동가"], "desc": "사람들의 성장을 돕고 사회에 긍정적인 영향을 주는 의미 있는 일을 선호해요."},
    "INFP": {"title": "🎨 열정적인 중재자", "jobs": ["일러스트레이터", "소설가/웹툰 작가", "정신건강 의학과 의사", "인사담당자"], "desc": "예술적 감수성이 풍부하고 자신의 가치관을 진정성 있게 표현하는 일을 좋아해요."},
    "ENFJ": {"title": "🤝 정의로운 사회운동가", "jobs": ["비영리단체 운영자", "아나운서/PD", "커리어 코치", "외교관"], "desc": "타인의 마음을 잘 이해하고 영감을 주며, 함께 협동하여 더 나은 세상을 만듭니다."},
    "ENFP": {"title": "✨ 재기발랄한 활동가", "jobs": ["콘텐츠 크리에이터", "이벤트 기획자", "광고 카피라이터", "여행 작가"], "desc": "자유롭고 창의적이며, 사람들에게 즐거움을 주고 소통하는 일에서 에너지를 얻어요."},
    "ISTJ": {"title": "📊 청렴결백한 논리주의자", "jobs": ["회계사", "공무원", "품질 관리원", "사법관"], "desc": "매우 책임감이 강하고 사실에 기반하여 일을 정확하고 철저하게 처리하는 능력이 있어요."},
    "ISFJ": {"title": "🛡️ 용감한 수호자", "jobs": ["간호사", "초등 교사", "사회복지사", "박물관 큐레이터"], "desc": "차분하고 따뜻하며, 타인을 세심하게 배려하고 안전하게 지켜주는 일에 보람을 느낍니다."},
    "ESTJ": {"title": "👔 엄격한 관리자", "jobs": ["경찰/군 장교", "은행원", "물류 관리자", "학교 행정가"], "desc": "조직적이고 규칙을 중요하게 생각하며, 일의 효율성을 높이고 관리하는 데 탁월해요."},
    "ESFJ": {"title": "💖 사교적인 외교관", "jobs": ["승무원", "호텔리어", "초등/유치원 교사", "HR(인사) 매니저"], "desc": "사람들을 환대하고 친절하게 도우며, 조직 안에서 화합과 조화를 이끌어냅니다."},
    "ISTP": {"title": "🔧 만능 재주꾼", "jobs": ["엔지니어/정비사", "파일럿", "데이터 분석가", "범죄 프로파일러"], "desc": "관찰력이 뛰어나고 도구를 잘 다루며, 위기 상황에서 냉철하게 문제를 해결해요."},
    "ISFP": {"title": "🎨 호기심 많은 예술가", "jobs": ["패션 디자이너", "파티시에", "작곡가", "동물 사육사"], "desc": "현재를 즐기며 예술적 감각이 뛰어나고, 따뜻한 마음으로 세상을 아름답게 꾸밉니다."},
    "ESTP": {"title": "⚡ 수완 좋은 활동가", "jobs": ["소방관", "스포츠 에이전트", "영업 마케터", "투자 분석가"], "desc": "행동력이 넘치고 현실적인 문제를 빠르게 해결하며, 스릴 있고 역동적인 일을 좋아해요."},
    "ESFP": {"title": "🎉 자유로운 영혼의 연예인", "jobs": ["뮤지컬 배우/연예인", "이벤트 MC", "여행 가이드", "홍보 전문가"], "desc": "스타일과 매력이 넘치며, 사람들의 이목을 집중시키고 분위기를 밝게 만드는 재능이 있어요."}
}

# 4. 사용자 입력 UI
st.write("### 👇 나의 MBTI를 선택해보세요!")

mbti_list = sorted(list(mbti_jobs.keys()))
selected_mbti = st.selectbox("나의 성격 유형은 무엇인가요?", mbti_list, index=0)

st.markdown("---")

# 5. 결과 출력 화면
if selected_mbti:
    info = mbti_jobs[selected_mbti]
    
    # 풍선 효과 애니메이션
    st.balloons()
    
    # 결과 헤더
    st.markdown(f"### 🎉 당신은 **{selected_mbti} ({info['title']})** 이군요!")
    st.info(f"💡 **성격 특징:** {info['desc']}")
    
    st.write("#### 🔍 추천하는 대표 직업군")
    
    # 2열(Column) 구조 배치
    cols = st.columns(2)
    for idx, job in enumerate(info['jobs']):
        with cols[idx % 2]:
            st.markdown(f"""
                <div class="job-card">
                    <h4 class="recommend-title">✨ {job}</h4>
                    <p style="margin: 0; color: #555; font-size: 0.9rem;">이 직업은 당신의 성격적 장점을 잘 발휘할 수 있는 분야입니다.</p>
                </div>
            """, unsafe_allowed_html=True)
            
    # 하단 격려 메시지
    st.success("🌟 MBTI는 진로 탐색을 위한 참고용일 뿐이에요! 여러분의 가능성은 무궁무진합니다.")

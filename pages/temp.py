import streamlit as st
import pandas as pd
import random

# Page 설정
st.set_page_config(page_title="우리 반 날씨 맞추기 퀴즈", page_icon="🌤️", layout="centered")

# 1. 데이터 로드 및 전처리
@st.cache_data
def load_data():
    df = pd.read_csv("ta_20260619190504.csv")
    df.columns = df.columns.str.strip()
    df['날짜'] = df['날짜'].astype(str).str.replace(r'\s+', '', regex=True)
    df['날짜'] = pd.to_datetime(df['날짜'], errors='coerce')
    df = df.dropna(subset=['평균기온(℃)', '최저기온(℃)', '최고기온(℃)'])
    df['연도'] = df['날짜'].dt.year
    df['월'] = df['날짜'].dt.month
    df['일'] = df['날짜'].dt.day
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"데이터 파일 로드 오류: {e}")
    st.stop()

# 2. 고정된 메인 타이틀
st.title("🌤️ 내 기억 속 가장 극단적인 날씨는?")
st.markdown("""
우리 반 친구들의 기억력을 시험해보는 날씨 퀴즈입니다!  
특정 날짜를 선택하고, **우리가 살아온 시대(2010년~2026년)** 중 그날 가장 더웠던 해나 추웠던 해를 맞춰보세요!
""")
st.divider()

# 3. 사이드바 입력값 받아오기
st.sidebar.header("⚙️ 문제 세팅")
mode = st.sidebar.radio(
    "어떤 문제를 풀 의향이신가요?",
    ["🔥 가장 더웠던 해 맞추기", "❄️ 가장 추웠던 해 맞추기"]
)
is_hot_mode = "더웠던" in mode

target_month = st.sidebar.selectbox("월 선택", list(range(1, 13)), index=7) # 기본값 8월
max_days = 30 if target_month in [4, 6, 9, 11] else (29 if target_month == 2 else 31)
target_day = st.sidebar.selectbox("일 선택", list(range(1, max_days + 1)), index=0) # 기본값 1일

# 4. 퀴즈 상태 관리
current_quiz_id = f"{target_month}_{target_day}_{is_hot_mode}"

if "quiz_id" not in st.session_state or st.session_state["quiz_id"] != current_quiz_id:
    filtered_df = df[(df['월'] == target_month) & (df['일'] == target_day) & (df['연도'] >= 2010)]
    
    if not filtered_df.empty:
        if is_hot_mode:
            sorted_df = filtered_df.sort_values(by='최고기온(℃)', ascending=False)
            target_col = '최고기온(℃)'
        else:
            sorted_df = filtered_df.sort_values(by='최저기온(℃)', ascending=True)
            target_col = '최저기온(℃)'
            
        correct_year = int(sorted_df.iloc[0]['연도'])
        correct_temp = sorted_df.iloc[0][target_col]
        
        # 보기 4개 만들기
        top_years = sorted_df.head(4)['연도'].astype(int).tolist()
        while len(top_years) < 4:
            random_year = random.choice(filtered_df['연도'].unique())
            if random_year not in top_years:
                top_years.append(int(random_year))
        random.shuffle(top_years)
        
        # 🔥 [수정] 정답 연도를 절대 유출하지 않는 중1 맞춤형 사건 힌트!
        if correct_year == 2018:
            hint_text = "💡 힌트: 대구보다 서울이 더 덥다고 난리 났던 역대급 서프리카 폭염의 해! 방탄소년단(BTS)이 빌보드 앨범 차트에서 처음으로 1위를 한 해이기도 해요."
        elif correct_year == 2020:
            hint_text = "💡 힌트: 전 세계적으로 코로나19가 대유행하기 시작해서 학교도 제대로 못 가고 온라인 수업을 들었던 기억 속의 첫 해입니다."
        elif correct_year == 2021:
            hint_text = "💡 힌트: 넷플릭스 드라마 '오징어 게임'이 전 세계적으로 엄청난 대유행을 일으켰던 해입니다!"
        elif correct_year == 2022:
            hint_text = "💡 힌트: 겨울에 카타르 월드컵이 열려서 대한민국이 기적으로 16강에 진출해 '중요한 건 꺾이지 않는 마음(중꺾마)'이라는 유행어가 돌던 해입니다."
        elif correct_year == 2023:
            hint_text = "💡 힌트: 비교적 최근이에요! 기후 변화로 인해 전 세계가 '지구 온난화'를 넘어 '지구 열대화' 시대에 진입했다고 선포된 작년 직전 해입니다."
        elif correct_year == 2024:
            hint_text = "💡 힌트: 파리 올림픽이 개최되었던 해입니다! 삐약이 신유빈 선수나 사격 김예지 선수가 화제가 되었던 기억이 나나요?"
        elif correct_year >= 2025:
            hint_text = "💡 힌트: 정말 엄청나게 최근입니다. 여러분이 초등학교 고학년이거나 중학생이 된 후의 아주 생생한 기억입니다!"
        elif correct_year <= 2012:
            hint_text = "💡 힌트: 2010년대 극초반입니다. 싸이의 '강남스타일'이 전 세계를 휩쓸며 전 국민이 말춤을 추던 시절입니다."
        else:
            hint_text = "💡 힌트: 2010년대 중후반기입니다. 여러분이 아장아장 걷거나 유치원에 다니며 세상을 배우고 있던 아주 어릴 적 시절입니다."

        # 세션에 고정 저장
        st.session_state["quiz_id"] = current_quiz_id
        st.session_state["correct_year"] = correct_year
        st.session_state["correct_temp"] = correct_temp
        st.session_state["options"] = top_years
        st.session_state["hint_text"] = hint_text
        st.session_state["answered"] = False

# 5. 화면에 문제 표시
st.subheader(f"📅 {target_month}월 {target_day}일의 날씨 퀴즈")
mode_text = "가장 더웠던(최고기온 높은) 해" if is_hot_mode else "가장 추웠던(최저기온 낮은) 해"
st.markdown(f"### Q. **2010년~2026년 중** 서울에서 이날 **{mode_text}**는 언제였을까요?")

options_str = [f"{y}년" for y in st.session_state["options"]]
user_choice = st.radio("정답이라고 생각하는 연도를 선택하세요:", options_str, key="user_choice_radio")

col1, col2 = st.columns([1, 4])
with col1:
    submit_btn = st.button("정답 확인하기", type="primary")
with col2:
    show_hint = st.checkbox("💡 힌트 보기")

if show_hint:
    st.info(st.session_state["hint_text"])

if submit_btn:
    st.session_state["answered"] = True

# 정답 확인 결과 레이아웃
if st.session_state["answered"]:
    selected_year = int(st.session_state["user_choice_radio"].replace("년", ""))
    
    if selected_year == st.session_state["correct_year"]:
        st.success(f"🎉 **정답입니다!! 너희들 기억력 진짜 좋다!**")
        st.balloons()
    else:
        st.error(f"😢 **아쉽게도 틀렸습니다!** 아래 그래프를 보면서 정답을 확인해봐요.")
        
    st.markdown(f"""
    **🔍 정답 해설:**
    * **역대 기록:** {st.session_state['correct_year']}년 {target_month}월 {target_day}일
    * **그날의 기온:** {st.session_state['correct_temp']} ℃
    """)
    
    # 6. 통계 및 그래프 시각화
    st.divider()
    st.subheader(f"📊 역대 {target_month}월 {target_day}일 기온 트렌드 (1907-2026)")
    st.markdown("퀴즈는 최근 15년 데이터로 냈지만, **100년 전부터 기온이 어떻게 변해왔는지** 그래프로 확인해 보세요!")
    
    chart_df = df[(df['월'] == target_month) & (df['일'] == target_day)].sort_values(by='연도')
    chart_data = chart_df.set_index('연度' if '연度' in df.columns else '연도')[['평균기온(℃)', '최저기온(℃)', '최고기온(℃)']]
    st.line_chart(chart_data)
    
    # 순위 표
    st.subheader(f"🔝 2010년 이후 {target_month}월 {target_day}일 기온 순위 Top 3")
    recent_chart_df = chart_df[chart_df['연도'] >= 2010]
    if is_hot_mode:
        rank_df = recent_chart_df.sort_values(by='최고기온(℃)', ascending=False).head(3)
    else:
        rank_df = recent_chart_df.sort_values(by='최저기온(℃)', ascending=True).head(3)
        
    rank_df['순위'] = ["1위 (정답)", "2위", "3위"]
    display_df = rank_df[['순위', '연도', '평균기온(℃)', '최저기온(℃)', '최고기온(℃)']].set_index('순위')
    st.dataframe(display_df, use_container_width=True)

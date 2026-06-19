import streamlit as st
import pandas as pd
import random

# Page 설정
st.set_page_config(page_title="서울 역대 날씨 맞추기 퀴즈", page_icon="🌤️", layout="centered")

# 1. 데이터 로드 및 전처리 (캐싱 처리로 속도 향상)
@st.cache_data
def load_data():
    # 파일 읽기
    df = pd.read_csv("ta_20260619190504.csv")
    
    # 열 이름 공백 제거
    df.columns = df.columns.str.strip()
    
    # 날짜 열의 \t 문자 제거 및 datetime 변환
    df['날짜'] = df['날짜'].astype(str).str.replace(r'\s+', '', regex=True)
    df['날짜'] = pd.to_datetime(df['날짜'], errors='coerce')
    
    # 결측치 제거 (평균, 최저, 최고 기온이 없는 행 제외)
    df = df.dropna(subset=['평균기온(℃)', '최저기온(℃)', '최고기온(℃)'])
    
    # 분석에 필요한 연, 월, 일 열 추가
    df['연도'] = df['날짜'].dt.year
    df['월'] = df['날짜'].dt.month
    df['일'] = df['날짜'].dt.day
    
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"데이터 파일을 불러오는 중 오류가 발생했습니다. 파일명을 확인해 주세요. 오차: {e}")
    st.stop()

# 2. 앱 타이틀 및 설명
st.title("🌤️ 내 기억 속 가장 극단적인 날씨는?")
st.markdown("""
1907년부터 2026년까지의 서울 기온 데이터를 바탕으로 출제되는 퀴즈입니다!  
특정 날짜를 선택하고, 그날 **가장 더웠던 해** 혹은 **가장 추웠던 해**를 맞춰보세요.
""")

st.divider()

# 3. 사이드바 - 문제 세팅 및 옵션
st.sidebar.header("⚙️ 문제 세팅")

# 모드 선택 (가장 더운 날 vs 가장 추운 날)
mode = st.sidebar.radio(
    "어떤 문제를 풀 의향이신가요?",
    ["🔥 가장 더웠던 해 맞추기 (최고기온 기준)", "❄️ 가장 추웠던 해 맞추기 (최저기온 기준)"]
)
is_hot_mode = "더웠던" in mode

# 날짜 선택
target_month = st.sidebar.selectbox("월 선택", list(range(1, 13)), index=7) # 기본값 8월
# 월별 일수 동적 조절
max_days = 31
if target_month in [4, 6, 9, 11]: max_days = 30
elif target_month == 2: max_days = 29

target_day = st.sidebar.selectbox("일 선택", list(range(1, max_days + 1)), index=0) # 기본값 1일

# 세션 상태(Session State)를 활용해 날짜나 모드가 바뀌면 퀴즈를 초기화
state_key = f"{target_month}_{target_day}_{is_hot_mode}"
if "current_quiz" not in st.session_state or st.session_state.get("quiz_key") != state_key:
    # 해당 날짜 데이터 필터링
    filtered_df = df[(df['월'] == target_month) & (df['일'] == target_day)]
    
    if filtered_df.empty:
        st.warning("선택한 날짜에 해당하는 데이터가 부족합니다.")
        st.stop()
        
    # 기온 순으로 정렬하여 정답 및 보기 추출
    if is_hot_mode:
        sorted_df = filtered_df.sort_values(by='최고기온(℃)', ascending=False)
        target_col = '최고기온(℃)'
    else:
        sorted_df = filtered_df.sort_values(by='최저기온(℃)', ascending=True)
        target_col = '최저기온(℃)'
        
    # 정답 연도 (1등)
    correct_year = int(sorted_df.iloc[0]['연도'])
    correct_temp = sorted_df.iloc[0][target_col]
    
    # 보기 생성 (상위 4개 연도를 무작위 셔플)
    top_years = sorted_df.head(4)['연도'].astype(int).tolist()
    # 만약 데이터가 너무 적어 4개가 안 채워지면 주변 연도 임의 추가
    while len(top_years) < 4:
        random_year = random.choice(filtered_df['연도'].unique())
        if random_year not in top_years:
            top_years.append(int(random_year))
            
    random.shuffle(top_years)
    
    # 힌트 준비 (정답 연도의 전후 시대적 배경을 유추할 수 있는 힌트 제공)
    if correct_year < 1950:
        hint = "힌트: 6·25 전쟁이 일어나기 전인 20세기 전반기 역사 속의 해입니다!"
    elif correct_year < 1980:
        hint = "힌트: 1950년대~1970년대 사이, 대한민국 근대화·산업화가 한창 진행되던 시절입니다."
    elif correct_year < 2000:
        hint = "힌트: 1980년대~1990년대 사이입니다. 응답하라 시리즈에 나올 법한 시절이네요!"
    else:
        hint = f"힌트: 2000년 이후 밀레니엄 시대입니다. 비교적 최근의 기억을 더듬어보세요! ({correct_year // 10 * 10}년대)"

    # 세션에 기록
    st.session_state["quiz_key"] = state_key
    st.session_state["correct_year"] = correct_year
    st.session_state["correct_temp"] = correct_temp
    st.session_state["options"] = top_years
    st.session_state["hint"] = hint
    st.session_state["submitted"] = False

# 4. 퀴즈 화면 구성
st.subheader(f"📅 {target_month}월 {target_day}일의 퀴즈")
st.markdown(f"### Q. 역대 서울에서 이날 **{mode.split()[1]}** 해는 언제였을까요?")

# 보기 보여주기 (문자열로 변환하여 라디오 버튼 생성)
options_str = [f"{y}년" for y in st.session_state["options"]]
user_choice = st.radio("연도를 선택하세요:", options_str, index=0)

# 열 레이아웃을 이용해 버튼 배치
col1, col2 = st.columns([1, 4])

with col1:
    submit_btn = st.button("정답 확인하기", type="primary")
with col2:
    # 힌트 버튼 토글 기능 구현
    show_hint = st.checkbox("💡 힌트 보기")

if show_hint:
    st.info(st.session_state["hint"])

# 정답 확인 로직
if submit_btn or st.session_state["submitted"]:
    st.session_state["submitted"] = True
    selected_year = int(user_choice.replace("년", ""))
    
    if selected_year == st.session_state["correct_year"]:
        st.success(f"🎉 **정답입니다!!**")
        st.balloons()
    else:
        st.error(f"😢 **아쉽게도 틀렸습니다!** 정답을 아래에서 확인하고 기후 변화 흐름을 살펴보세요.")
        
    st.markdown(f"""
    **정답 및 날씨 정보:**
    * **정답 연도:** {st.session_state['correct_year']}년
    * **그날의 기온:** {st.session_state['correct_temp']} ℃
    """)
    
    # 5. 결과 시각화 및 통계 자료 제공
    st.divider()
    st.subheader(f"📊 역대 {target_month}월 {target_day}일 기온 변화 추이")
    
    # 해당 날짜의 역대 전체 데이터 가져오기
    chart_df = df[(df['월'] == target_month) & (df['일'] == target_day)].sort_values(by='연도')
    
    # 선 그래프 시각화 (Streamlit 내장 차트 사용)
    # 기온 구분을 위해 최고/최저/평균 선택 혹은 일괄 표시
    chart_data = chart_df.set_index('연도')[['평균기온(℃)', '최저기온(℃)', '최고기온(℃)']]
    st.line_chart(chart_data)
    
    st.caption("💡 그래프를 통해 연도가 흐를수록 기온의 변동 폭과 전반적인 상승/하강 추세를 확인해 볼 수 있습니다.")
    
    # 역대 순위 Top 3 표 제공
    st.subheader(f"🔝 역대 {target_month}월 {target_day}일 기온 순위 보기")
    if is_hot_mode:
        rank_df = chart_df.sort_values(by='최고기온(℃)', ascending=False).head(3)
    else:
        rank_df = chart_df.sort_values(by='최저기온(℃)', ascending=True).head(3)
        
    rank_df['순위'] = [f"{i}위" for i in range(1, 4)]
    display_df = rank_df[['순위', '연도', '평균기온(℃)', '최저기온(℃)', '최고기온(℃)']].set_index('순위')
    st.dataframe(display_df, use_container_width=True)

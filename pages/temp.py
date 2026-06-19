import streamlit as st
import pandas as pd
import random

# Page 설정
st.set_page_config(page_title="서울 역대 날씨 맞추기 퀴즈", page_icon="🌤️", layout="centered")

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
1907년부터 2026년까지의 서울 기온 데이터를 바탕으로 출제되는 퀴즈입니다!  
특정 날짜를 선택하고, 그날 **가장 더웠던 해** 혹은 **가장 추웠던 해**를 맞춰보세요.
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

# 4. 퀴즈 상태 관리 (새로고침 시 데이터 유지)
current_quiz_id = f"{target_month}_{target_day}_{is_hot_mode}"

if "quiz_id" not in st.session_state or st.session_state["quiz_id"] != current_quiz_id:
    filtered_df = df[(df['월'] == target_month) & (df['일'] == target_day)]
    
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
        
        # 힌트 설정
        if correct_year < 1950:
            hint_text = "힌트: 6·25 전쟁이 일어나기 전인 20세기 전반기 역사 속의 해입니다!"
        elif correct_year < 1980:
            hint_text = "힌트: 1950년대~1970년대 사이, 대한민국 근대화·산업화가 한창 진행되던 시절입니다."
        elif correct_year < 2000:
            hint_text = "힌트: 1980년대~1990년대 사이입니다. 대중문화의 황금기 시절이네요!"
        else:
            hint_text = f"힌트: 2000년 이후 스마트폰 보급기 이후의 시대입니다. ({correct_year // 10 * 10}년대)"

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
st.markdown(f"### Q. 역대 서울에서 이날 **{mode_text}**는 언제였을까요?")

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
        st.success(f"🎉 **정답입니다!! 대단하시네요!**")
        st.balloons()
    else:
        st.error(f"😢 **아쉽게도 틀렸습니다!** 다른 연도를 골라보거나 아래 통계를 확인해 보세요.")
        
    st.markdown(f"""
    **🔍 정답 해설:**
    * **역대 기록:** {st.session_state['correct_year']}년 {target_month}월 {target_day}일
    * **그날의 기온:** {st.session_state['correct_temp']} ℃
    """)
    
    # 6. 통계 및 그래프 시각화 (오타 수정된 부분 🛠️)
    st.divider()
    st.subheader(f"📊 역대 {target_month}월 {target_day}일 기온 트렌드 (1907-2026)")
    
    chart_df = df[(df['월'] == target_month) & (df['일'] == target_day)].sort_values(by='연도')
    
    # '연度' -> '연도'로 올바르게 수정 완료!
    chart_data = chart_df.set_index('연도')[['평균기온(℃)', '최저기온(℃)', '최고기온(℃)']]
    st.line_chart(chart_data)
    
    # 순위 표
    st.subheader(f"🔝 역대 {target_month}월 {target_day}일 기온 순위 Top 3")
    if is_hot_mode:
        rank_df = chart_df.sort_values(by='최고기온(℃)', ascending=False).head(3)
    else:
        rank_df = chart_df.sort_values(by='최저기온(℃)', ascending=True).head(3)
        
    rank_df['순위'] = ["1위 (정답)", "2위", "3위"]
    display_df = rank_df[['순위', '연도', '평균기온(℃)', '최저기온(℃)', '최고기온(℃)']].set_index('순위')
    st.dataframe(display_df, use_container_width=True)

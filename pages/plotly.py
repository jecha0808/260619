import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px

st.set_page_config(
    page_title="Global Top10 Stocks Dashboard",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Global Market Cap Top 10 Stocks")
st.caption("최근 1년 주가 성과 비교 (기준값=100)")

stocks = {
    "NVIDIA": "NVDA",
    "Apple": "AAPL",
    "Alphabet": "GOOGL",
    "Microsoft": "MSFT",
    "Amazon": "AMZN",
    "TSMC": "TSM",
    "Saudi Aramco": "2222.SR",
    "Meta": "META",
    "Broadcom": "AVGO",
    "Tesla": "TSLA"
}

@st.cache_data(ttl=3600)
def load_data():
    result = pd.DataFrame()

    for name, ticker in stocks.items():
        try:
            data = yf.download(
                ticker,
                period="1y",
                auto_adjust=True,
                progress=False
            )

            if not data.empty:
                result[name] = data["Close"]

        except Exception:
            pass

    return result

df = load_data()

if df.empty:
    st.error("주가 데이터를 불러오지 못했습니다.")
    st.stop()

# 시작점을 100으로 정규화
normalized = df.div(df.iloc[0]).mul(100)

fig = px.line(
    normalized,
    x=normalized.index,
    y=normalized.columns,
    title="최근 1년 수익률 비교 (Start=100)"
)

fig.update_layout(
    height=700,
    xaxis_title="Date",
    yaxis_title="Normalized Price",
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)

# 성과 순위
performance = (
    normalized.iloc[-1] - 100
).sort_values(ascending=False)

st.subheader("🏆 최근 1년 수익률 순위")

rank_df = pd.DataFrame({
    "Company": performance.index,
    "Return (%)": performance.values.round(2)
})

st.dataframe(rank_df, use_container_width=True)

# 현재 가격
latest = df.iloc[-1].round(2)

st.subheader("💰 현재 주가")

price_df = pd.DataFrame({
    "Company": latest.index,
    "Price": latest.values
})

st.dataframe(price_df, use_container_width=True)

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
from src.utils import get_correlation  

# 1. Page Config
st.set_page_config(page_title="Market Mood Tracker", layout="wide")
st.title("📈 Market Mood vs. Price Correlation")
st.markdown("Analyzing how news sentiment impacts stock performance.")

# 2. Sidebar for Selection
ticker = st.sidebar.text_input("Enter Ticker (e.g., TD.TO, SHOP.TO, NVDA)", "TD.TO").upper()

# 3. Path Setup
sentiment_path = f"data/processed/{ticker}_sentiment.csv"
price_path = f"data/processed/{ticker}_prices.csv"

# 4. Main Logic
if os.path.exists(sentiment_path) and os.path.exists(price_path):
    df_s = pd.read_csv(sentiment_path)
    df_p = pd.read_csv(price_path)

    # Date formatting and sorting
    df_s['date'] = pd.to_datetime(df_s['date'], errors='coerce')
    df_p['Date'] = pd.to_datetime(df_p['Date'], utc=True, errors='coerce')
    df_s = df_s.sort_values('date')
    df_p = df_p.sort_values('Date')
    
    # --- Sentiment & Correlation Summary Metrics ---
    avg_sentiment = df_s['sentiment_score'].mean()
    correlation_val = get_correlation(df_s, df_p)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Avg Sentiment", f"{avg_sentiment:.2f}")
    col2.metric("Mood Correlation", f"{correlation_val:.2f}")
    col3.metric("Headlines", len(df_s))
    col4.metric("Current Mood", "Bullish 📈" if avg_sentiment > 0.05 else "Bearish 📉" if avg_sentiment < -0.05 else "Neutral ⚖️")

    if abs(correlation_val) > 0.5:
        st.success(f"🔥 **Strong Correlation Detected ({correlation_val})**: Market mood and price are highly synchronized.")
    elif abs(correlation_val) > 0.2:
        st.info(f"⚖️ **Moderate Correlation ({correlation_val})**: There is a visible trend, but other factors are at play.")
    else:
        st.warning(f"❄️ **Low Correlation ({correlation_val})**: News sentiment doesn't appear to be the primary driver for {ticker} currently.")

    # 5. Create Dual-Axis Chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_p['Date'], y=df_p['Close'], name="Stock Price", line=dict(color='royalblue', width=3)))
    fig.add_trace(go.Scatter(x=df_s['date'], y=df_s['sentiment_score'], name="News Sentiment", mode='markers+lines', marker=dict(size=10, color='firebrick'), yaxis="y2"))

    # 6. Layout Styling
    fig.update_layout(
        xaxis_title="Timeline",
        yaxis=dict(title=dict(text="Stock Price ($)", font=dict(color="royalblue")), tickfont=dict(color="royalblue")),
        yaxis2=dict(title=dict(text="Sentiment Score (-1 to 1)", font=dict(color="firebrick")), tickfont=dict(color="firebrick"), anchor="x", overlaying="y", side="right"),
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    st.plotly_chart(fig, use_container_width=True)

    # 7. Sentiment Table
    with st.expander("🔍 View Scanned Headlines"):
        st.dataframe(df_s[['date', 'mood', 'headline']], use_container_width=True)
else:
    st.warning(f"⚠️ Missing data files for {ticker}. Please run 'python main.py' first.")
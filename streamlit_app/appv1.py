# streamlit_app.py

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Set up the page configuration
st.set_page_config(page_title="Performance Chart", layout="wide")

# Sidebar for user input (optional)
st.sidebar.header("Settings")
start_date = st.sidebar.date_input("Start Date")
end_date = st.sidebar.date_input("End Date")
symbol = st.sidebar.text_input("Enter Symbol", value="AAPL")

# Main Title
st.title("Performance Chart")

# Sample Financial Data (or fetch your own)
@st.cache_data
def load_data():
    # You can fetch stock data using APIs like Yahoo Finance or Alpha Vantage.
    data = pd.read_csv(
        "https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv"
    )
    return data

data = load_data()

# Filter data based on user input (if applicable)
# Here, we're using the default sample data.
# Create a TradingView-like chart using Plotly
fig = go.Figure()

# Add Candlestick
fig.add_trace(
    go.Candlestick(
        x=data["Date"],
        open=data["AAPL.Open"],
        high=data["AAPL.High"],
        low=data["AAPL.Low"],
        close=data["AAPL.Close"],
        name="Price",
    )
)

# Add Moving Averages
data["SMA20"] = data["AAPL.Close"].rolling(window=20).mean()
data["SMA50"] = data["AAPL.Close"].rolling(window=50).mean()

fig.add_trace(
    go.Scatter(
        x=data["Date"],
        y=data["SMA20"],
        line=dict(color="blue", width=1),
        name="SMA 20",
    )
)

fig.add_trace(
    go.Scatter(
        x=data["Date"],
        y=data["SMA50"],
        line=dict(color="orange", width=1),
        name="SMA 50",
    )
)

# Layout for TradingView style
fig.update_layout(
    title=f"TradingView Style Chart - {symbol}",
    xaxis_title="Date",
    yaxis_title="Price",
    template="plotly_dark",
    xaxis_rangeslider_visible=False,
    height=600,
    margin=dict(l=40, r=40, t=40, b=40),
)

# Display the chart
st.plotly_chart(fig, use_container_width=True)

# Add placeholder for additional content
st.markdown(
    """
<div style="margin-top: 50px; padding: 20px; background-color: #f8f9fa; border-radius: 10px;">
    <h3 style="color: #007bff;">Additional Analytics</h3>
    <p style="color: #6c757d;">Placeholder for more details or charts.</p>
</div>
""",
    unsafe_allow_html=True,
)

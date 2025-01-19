import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time
from datetime import datetime
import os
import threading
import time
import random

# Sidebar
st.sidebar.title("Crypto Signal Application")
menu = st.sidebar.radio("Navigation", ["Orders", "Feedbacks", "Backtesting", "Notebook Save", "History"])

# Title
st.title("Enhanced SMA Crossover Strategy with Price Action")

# User inputs for SMA periods and timeframe
short_period = st.sidebar.number_input("Short SMA Period", min_value=1, value=10)
long_period = st.sidebar.number_input("Long SMA Period", min_value=1, value=50)
timeframe = st.sidebar.selectbox("Timeframe", ["1m", "5m", "15m", "1h", "1d"])

# Placeholder for cryptocurrency data (simulated)
st.subheader("Cryptocurrency Prices")
data = {
    "Time": pd.date_range(start="2023-01-01", periods=100, freq="H"),
    "Open": np.random.uniform(100, 150, 100),
    "High": np.random.uniform(150, 200, 100),
    "Low": np.random.uniform(50, 100, 100),
    "Close": np.random.uniform(100, 200, 100),
}
df = pd.DataFrame(data)

# Calculate SMAs
short_sma = df["Close"].rolling(window=short_period).mean()
long_sma = df["Close"].rolling(window=long_period).mean()

# Generate buy and sell signals
momentum = df["Close"].pct_change(periods=10)
buy_signal = (short_sma > long_sma) & (momentum > 0)
sell_signal = (short_sma < long_sma) & (momentum < 0)

df["Buy Signal"] = buy_signal
df["Sell Signal"] = sell_signal

# Create TradingView-like candlestick chart
fig = go.Figure()
fig.add_trace(go.Candlestick(
    x=df["Time"],
    open=df["Open"],
    high=df["High"],
    low=df["Low"],
    close=df["Close"],
    name="Candlesticks"
))

# Add buy signals
fig.add_trace(go.Scatter(
    x=df["Time"][buy_signal],
    y=df["Close"][buy_signal],
    mode="markers",
    marker=dict(color="green", size=10),
    name="Buy Signal"
))

# Add sell signals
fig.add_trace(go.Scatter(
    x=df["Time"][sell_signal],
    y=df["Close"][sell_signal],
    mode="markers",
    marker=dict(color="red", size=10),
    name="Sell Signal"
))

fig.update_layout(
    title="TradingView-style Chart",
    xaxis_title="Time",
    yaxis_title="Price",
    template="plotly_dark"
)

st.plotly_chart(fig, use_container_width=True)

# Real-time price tracking feature
if st.button("Buy") or st.button("Sell"):
    selected_coin = "Bitcoin (BTC)"  # In a real scenario, this should be dynamic
    
    # Track price movement in the sidebar
    price_tracking = st.sidebar.empty()  # Use st.empty() to dynamically update the sidebar
    
    last_price = df['Close'].iloc[-1]  # Get the last price from the data
    price_tracking.text(f"Tracking {selected_coin} Price Movement...")

    # Simulate price movement tracking by updating every second
    for _ in range(10):  # Limit for 10 seconds, you can adjust this to your needs
        current_price = df['Close'].iloc[-1] + np.random.uniform(-1, 1)  # Simulate price fluctuation
        price_change = current_price - last_price
        last_price = current_price
        price_tracking.text(f"{selected_coin} Current Price: ${current_price:.2f}\n"
                            f"Price Change: ${price_change:.2f} per second")
        time.sleep(1)  # Update every second
    price_tracking.text(f"Final {selected_coin} Price: ${current_price:.2f}")

# Right Sidebar for Cryptocurrencies
st.sidebar.subheader("Cryptocurrencies")
cryptos = ["Bitcoin (BTC)", "Ethereum (ETH)", "Cardano (ADA)", "Solana (SOL)", "Ripple (XRP)", "Dogecoin (DOGE)", "Polkadot (DOT)", "Litecoin (LTC)"]
selected_crypto = st.sidebar.selectbox("Cryptocurrency", cryptos)

# Feedback Section
if menu == "Feedbacks":
    st.subheader("Feedback")
    feedback = st.text_area("Please leave your feedback here:")
    if st.button("Submit"):
        st.write("Thank you for your feedback!")
        # Here, you can add functionality to store or process the feedback, such as saving it to a database or a file.



# Shared variables for price and position tracking

# Helper function to simulate BTC price updates
def get_live_price():
    """Simulate live price data (replace with real API calls)."""
    btc_price = round(random.uniform(25000, 35000), 2)  # Simulate BTC price
    usd_price = round(btc_price * 1, 2)  # Equivalent USD price
    return btc_price, usd_price

# Initialize session state for tracking
if "tracking_position" not in st.session_state:
    st.session_state.tracking_position = False
    st.session_state.position_type = None  # "buy" or "sell"
    st.session_state.btc_price = 0
    st.session_state.usd_price = 0

# Main Buy/Sell logic
if menu == "Trade":
    st.subheader("Trade BTC/USD")

    # Buy/Sell Buttons
    if st.button("Buy"):
        st.session_state.tracking_position = True
        st.session_state.position_type = "buy"

    if st.button("Sell"):
        st.session_state.tracking_position = True
        st.session_state.position_type = "sell"

    # Sidebar for live price tracking
    if st.session_state.tracking_position:
        with st.sidebar:
            st.write(f"**{'Buying' if st.session_state.position_type == 'buy' else 'Selling'} BTC/USD Position**")

            # Display live price updates
            price_display = st.empty()  # Placeholder for price data
            cancel_button = st.button("Cancel Position")

            # Price update loop (limited to avoid infinite loops in Streamlit)
            for _ in range(100):  # Update up to 100 times
                btc_price, usd_price = get_live_price()
                st.session_state.btc_price = btc_price
                st.session_state.usd_price = usd_price

                # Update price display
                price_display.write(
                    f"""
                    **BTC Price**: {btc_price} USD  
                    **USD Worth**: {usd_price} USD
                    """
                )
                time.sleep(1)  # Wait 1 second before the next update

                # Check if "Cancel Position" was clicked
                if cancel_button:
                    st.session_state.tracking_position = False
                    st.sidebar.empty()  # Clear the sidebar
                    st.success("Position cancelled successfully.")
                    break

    # Message if no position is being tracked
    if not st.session_state.tracking_position:
        st.write("No active positions.")


#-backtesting page  -------------

if menu == "Backtesting":
    st.subheader("Backtesting Your Strategy")
    
    # Simulate a simple backtest of a strategy (buy when short SMA > long SMA, sell when vice versa)
    starting_balance = st.number_input("Starting Balance", min_value=1, value=1000)
    balance = starting_balance
    position = 0  # No position initially
    transaction_history = []  # To store transaction details

    # Loop through the historical data to simulate the backtest
    for i in range(1, len(df)):
        if buy_signal[i] and position == 0:  # Buy condition (and not in position)
            position = balance / df["Close"].iloc[i]  # Buy at current price
            balance = 0
            transaction_history.append(f"Bought at {df['Time'].iloc[i]} for {df['Close'].iloc[i]:.2f}")
        
        elif sell_signal[i] and position > 0:  # Sell condition (and in position)
            balance = position * df["Close"].iloc[i]  # Sell at current price
            position = 0
            transaction_history.append(f"Sold at {df['Time'].iloc[i]} for {df['Close'].iloc[i]:.2f}")
    
    # Final balance calculation (if position is still open)
    if position > 0:
        balance = position * df["Close"].iloc[-1]
    
    # Display results
    st.write(f"Final Balance after Backtest: ${balance:.2f}")
    st.write("Transaction History:")
    for transaction in transaction_history:
        st.write(transaction)



history_file = "history.csv"

# Check if the history file exists, if not create a new DataFrame
if os.path.exists(history_file):
    history_df = pd.read_csv(history_file)  # Read existing history from file
else:
    # If the file doesn't exist, create an empty DataFrame with the necessary columns
    history_df = pd.DataFrame(columns=["Time", "Description", "Image"])


# History Page: Cards for Trades------------------------------------

# History Page: Cards for Trades
if menu == "History":
    st.subheader("Trade History")

    # Form to add a new trade
    with st.form("Add Trade"):
        trade_description = st.text_input("Trade Description")
        uploaded_image = st.file_uploader("Upload an image for the trade", type=["png", "jpg", "jpeg"])
        submitted = st.form_submit_button("Add Trade")

        if submitted and trade_description and uploaded_image:
            # Save image to local folder
            image_path = f"images/{uploaded_image.name}"
            os.makedirs("images", exist_ok=True)
            with open(image_path, "wb") as f:
                f.write(uploaded_image.getbuffer())

            # Append to trade history
            new_entry = {
                "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Description": trade_description,
                "Image": image_path,
            }
            new_entry_df = pd.DataFrame([new_entry])  # Convert new entry to DataFrame
            history_df = pd.concat([history_df, new_entry_df], ignore_index=True)  # Append new entry
            history_df.to_csv(history_file, index=False)
            st.success("Trade added successfully!")

    # Display trade cards
    if not history_df.empty:
        for _, row in history_df.iterrows():
            col1, col2 = st.columns([1, 3])
            with col1:
                st.image(row["Image"], use_container_width=True)  # Updated parameter
            with col2:
                st.write(f"**Description:** {row['Description']}")
                st.write(f"**Saved on:** {row['Time']}")
                if st.button(f"Delete {row['Description']}", key=row["Time"]):
                    # Delete the selected trade
                    history_df = history_df[history_df["Time"] != row["Time"]]
                    history_df.to_csv(history_file, index=False)
                    st.experimental_rerun()  # Refresh the page to reflect changes

#-- notebook page
if menu == "Notebook Save":
    st.subheader("Notebook")

    # Load trade history
    history_df = pd.read_csv(history_file) if os.path.exists(history_file) else pd.DataFrame(columns=["Time", "Description", "Image"])

    # Load notebook entries
    notebook_file = "notebook.csv"
    
    # Check if notebook file exists and is empty
    if not os.path.exists(notebook_file):
        notebook_df = pd.DataFrame(columns=["Time", "Reference Trade", "Note"])
        notebook_df.to_csv(notebook_file, index=False)
    elif os.stat(notebook_file).st_size == 0:
        notebook_df = pd.DataFrame(columns=["Time", "Reference Trade", "Note"])
        notebook_df.to_csv(notebook_file, index=False)
    else:
        notebook_df = pd.read_csv(notebook_file)

    # Form for notebook entry
    with st.form("Add Notebook Entry"):
        # Dropdown to select a trade from history
        trade_options = ["None"] + [f"{row['Time']} - {row['Description']}" for _, row in history_df.iterrows()]
        selected_trade = st.selectbox("Select a trade to refer to (or choose None):", trade_options)

        # Text area for notes
        note_text = st.text_area("Write your note:")

        # Submit button
        submitted = st.form_submit_button("Save Note")

        if submitted:
            if note_text.strip():  # Ensure note is not empty
                # Determine reference trade
                reference_trade = selected_trade if selected_trade != "None" else "General Note"

                # Save note
                new_note = {
                    "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Reference Trade": reference_trade,
                    "Note": note_text.strip(),
                }
                new_note_df = pd.DataFrame([new_note])
                notebook_df = pd.concat([notebook_df, new_note_df], ignore_index=True)
                notebook_df.to_csv(notebook_file, index=False)

                st.success("Note saved successfully!")
            else:
                st.error("Please enter some text in the note field.")

    # Display notebook entries
    if not notebook_df.empty:
        st.subheader("Saved Notes")
        for _, row in notebook_df.iterrows():
            st.write(f"**Time:** {row['Time']}")
            st.write(f"**Reference Trade:** {row['Reference Trade']}")
            st.write(f"**Note:** {row['Note']}")
            st.divider()  # Adds a visual separator between notes

import yfinance as yf
import pandas as pd
import streamlit as st
import json
from datetime import datetime
import random
import pytz
import holidays

hour = datetime.now().hour

# App
# Market hours
# Set NY timezone
# Set timezone to New York (for NYSE & NASDAQ)
ny_tz = pytz.timezone("America/New_York")
now = datetime.now(ny_tz)

# Define U.S. stock market holidays
us_holidays = holidays.US(years=now.year)

# Market trading hours
market_open_time = now.replace(hour=9, minute=30, second=0, microsecond=0)
market_close_time = now.replace(hour=16, minute=0, second=0, microsecond=0)

# Check if it's a weekend
if now.weekday() >= 5:  # Saturday (5) or Sunday (6)
    market_status = "🔴 Market Closed (Weekend)"

# Check if it's a U.S. holiday
elif now.strftime('%Y-%m-%d') in us_holidays:
    holiday_name = us_holidays.get(now.strftime('%Y-%m-%d'))
    market_status = f"🔴 Market Closed ({holiday_name})"

# Check if market is open based on trading hours
elif market_open_time <= now <= market_close_time:
    market_status = "🟢 Market Open"

# Otherwise, market is closed
else:
    market_status = "🔴 Market Closed"
greeting = "🌅 Good Morning" if hour < 12 else "🌇 Good Afternoon" if hour < 18 else "🌙 Good Evening"
quotes = [
    "“The stock market is filled with individuals who know the price of everything, but the value of nothing.” – Philip Fisher",
    "“An investment in knowledge pays the best interest.” – Benjamin Franklin",
    "“Risk comes from not knowing what you’re doing.” – Warren Buffett"
]

st.set_page_config(page_title=" Stock Price Viewer App", page_icon="💹", layout="wide")
st.sidebar.write(f"{greeting}!")
st.sidebar.markdown(f"**{market_status}**")
st.sidebar.title("🔍 Search for a Stock")

st.title(
    f"""Welcome to  Stock Price Viewer 💹
    """
)
if "ticker_name_select" not in st.session_state:
    st.session_state.ticker_name_select = None
# ticker symbol
with open("stock_names.json", 'r') as file:
    stock_names_dict = json.load(file)
ticker_name_list = list(stock_names_dict.keys())

st.session_state.ticker_name_select = st.sidebar.selectbox(label="Select the Company 🛒", 
                                                           options=ticker_name_list, )
st.sidebar.markdown("📊 **Try searching for MSFT, TSLA, or GOOG!**")
ticker_symbol = st.session_state.ticker_name_select


st.sidebar.markdown(f"💡 *{random.choice(quotes)}*")

# Sidebar footer
st.sidebar.markdown("---")  # Adds a separator
st.sidebar.markdown("⚡ Powered by [yFinance API](https://pypi.org/project/yfinance/)")

# Get the data on this ticker
ticker_data = yf.Ticker(stock_names_dict[st.session_state.ticker_name_select])

# Get the historical prices for this ticker
ticker_df = ticker_data.history(period="1d", start="2010-5-31", end="2025-01-31")
st.divider()
# Open High Low Close Volume Dividends Stock Splits
st.write(f"### 📈 {st.session_state.ticker_name_select} Stock Close Prices")
st.line_chart(ticker_df.Close)
st.write(f"### 📈 {st.session_state.ticker_name_select} Stock Volume Prices")
st.line_chart(ticker_df.Volume)

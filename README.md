# Backtesting Dashboard

## Overview
The **Backtesting Dashboard** is a web application designed for monitoring trading strategies, viewing  live cryptocurrency prices, accessing performance analytics, and reviewing trade logs. This project offers an intuitive interface tailored for traders and analysts.

---

## Features
- 📈 **Dashboard Overview** with performance highlights .
- 💰 **Live Cryptocurrency Prices** for key assets (e.g., Bitcoin, Ethereum).
- 📰 **Latest News** for market updates and insights.
- 📊 Strategy Overview and Performance Analytics.
- 🗒️ Detailed Trades Log.

---

## Installation

### Step 1: Clone the repository
```bash
git clone https://github.com/MustcodeQ/backtesting-dashboard.git
cd backtesting-dashboard
```
### Step 2: Create and activate a virtual environment
```bash
# Create virtual environment
python -m venv env

# Activate the environment
# For Windows:
env\Scripts\activate
# For MacOS/Linux:
source env/bin/activate
```
### Step 3: Install dependencies
```bash
pip install -r requirements.txt
```
### Step 4: Install additional dependencies
```bash
pip install django streamlit plotly
```
### Step 5: Run Django migrations
```bash
python manage.py migrate
```
### Step 6: Start the Django development server
```bash
python manage.py runserver
```
### Step 7: Run Streamlit for analytics
```bash
streamlit run analytics.py
```
### Step 8: Access the application
Open your browser and go to:
Django application: http://127.0.0.1:8000
Streamlit application: The Streamlit URL provided in the terminal.

## API Integratiion
To enable live cryptocurrency prices and latest news:

Obtain an API key for cryptocurrency prices (e.g., CoinGecko API or CoinMarketCap API).
Obtain an API key for news updates (e.g., NewsAPI).
Update the API keys in your Django project's settings or environment variables:
```bash
# Example: settings.py
CRYPTO_API_KEY = 'your-crypto-api-key'
NEWS_API_KEY = 'your-news-api-key'
```


## How It Works
The Dashboard provides a comprehensive overview of your trading activities.
API calls fetch real-time cryptocurrency prices and news, displayed dynamically.
Users can navigate through sections like Strategy Overview, Performance Analytics, and Trades Log for detailed insights.
The Streamlit application visualizes detailed analytics and graphs for strategy performance.

## Notes
⚠️ Without API keys, live data for cryptocurrency prices and news will not work.
Ensure proper configuration of environment variables for API keys.
The Streamlit app must run separately from the Django server.

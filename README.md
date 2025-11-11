Real-Time Stock Market Dashboard
    A web dashboard built with Streamlit to visualize near real-time stock market data from Yahoo Finance. It displays interactive candlestick charts, moving averages, and key financial metrics for any selected       stock.

Features
  Interactive Candlestick Charts: Visualizes stock price movements (Open, High, Low, Close) using Plotly.
  Key Financial Indicators: Automatically calculates and plots:
    20-Period Simple Moving Average (SMA)
    50-Period Exponential Moving Average (EMA)
  User-Friendly Interface:

  Enter any stock ticker (e.g., AAPL, RELIANCE.NS).
  Select different time intervals (1m, 5m, 15m, etc.).
  Global Market Support: Uses the yfinance library to fetch data for global stocks, including US (NASDAQ, NYSE) and Indian (NSE, BSE) markets.
  Near Real-Time Data: Leverages Streamlit's caching to fetch fresh data every 5 minutes without hitting API rate limits.

Technologies Used
    This project is built with the following technologies:
    Python: The core programming language.
    Streamlit: For building and serving the interactive web app.
    Pandas: For data manipulation and calculating financial indicators.
    Plotly: For creating rich, interactive visualizations.
    yfinance: For fetching live and historical stock market data.

Getting Started
    Follow these instructions to get a copy of the project running on your local machine.

  Prerequisites
      You must have Python 3.8+ installed on your system.

  Installation
      Clone the repository:

      Bash

      git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git
      cd YOUR_REPOSITORY_NAME
  (Replace YOUR_USERNAME and YOUR_REPOSITORY_NAME with your actual GitHub details)

  Install the required libraries: (It is highly recommended to use a virtual environment)

    Bash

    pip install streamlit pandas plotly yfinance
   Pro-tip: You can create a requirements.txt file for your repository by running:

    Bash
    pip freeze > requirements.txt
  This makes it easier for others to install dependencies by just running pip install -r requirements.txt.

How to Run
  Once the libraries are installed, run the following command in your terminal from the project's root directory:

    Bash
     streamlit run dashboard.py
  Your default web browser will automatically open, displaying your live stock dashboard!

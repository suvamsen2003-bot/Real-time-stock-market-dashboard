import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
from datetime import datetime

# --- CONFIG ---
# ⚠️ IMPORTANT: Replace with your own free API key from Alpha Vantage
# Get one here: https://www.alphavantage.co/support/#api-key
API_KEY = "A8SCYCE9HH72AHN0" 

# --- HELPER FUNCTIONS ---

@st.cache_data(ttl="5m") # Cache data for 5 minutes
def fetch_stock_data(symbol, interval):
    """
    Fetches stock data from Alpha Vantage API using the requests library.
    """
    url = 'https://www.alphavantage.co/query'
    params = {
        'function': 'TIME_SERIES_INTRADAY',
        'symbol': symbol,
        'interval': interval,
        'apikey': API_KEY
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status() # Raise an exception for bad status codes
        data = response.json()
        
        # The key for time series data, e.g., 'Time Series (5min)'
        time_series_key = f"Time Series ({interval})"
        
        if time_series_key not in data:
            st.error(f"Error: Could not find data for {symbol}.")
            # Provide more API error info if available
            st.info(f"API Note: {data.get('Note', 'No note in response.')}")
            if "Error Message" in data:
                st.error(f"API Error: {data['Error Message']}")
            return None
            
        return data[time_series_key]
        
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return None
    except KeyError:
        # Handle cases where the API response is not as expected
        st.error("Error: Unexpected data structure from API.")
        st.write(data) # Print the problematic data for debugging
        return None

def process_data(raw_data):
    """
    Processes raw JSON data into a clean Pandas DataFrame 
    and calculates financial indicators.
    """
    if raw_data is None:
        return pd.DataFrame()

    # Convert to DataFrame
    df = pd.DataFrame.from_dict(raw_data, orient='index')
    
    # Rename columns for clarity
    df.rename(columns={
        '1. open': 'Open',
        '2. high': 'High',
        '3. low': 'Low',
        '4. close': 'Close',
        '5. volume': 'Volume'
    }, inplace=True)
    
    # Convert index to datetime and columns to numeric
    df.index = pd.to_datetime(df.index)
    df = df.astype(float)
    
    # Sort by date (oldest to newest) for Plotly
    df.sort_index(ascending=True, inplace=True)
    
    # --- Calculate Financial Indicators ---
    # Simple Moving Average (SMA)
    df['SMA_20'] = df['Close'].rolling(window=20).mean()
    # Exponential Moving Average (EMA)
    df['EMA_50'] = df['Close'].ewm(span=50, adjust=False).mean()
    
    return df

def create_plot(df, symbol, interval):
    """
    Creates an interactive Plotly candlestick chart with moving averages.
    """
    fig = go.Figure()

    # Candlestick chart
    fig.add_trace(go.Candlestick(x=df.index,
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close'],
                    name='Candlestick'))

    # SMA Line
    fig.add_trace(go.Scatter(x=df.index, 
                             y=df['SMA_20'], 
                             mode='lines', 
                             name='20-Period SMA',
                             line=dict(color='yellow', width=1.5)))

    # EMA Line
    fig.add_trace(go.Scatter(x=df.index, 
                             y=df['EMA_50'], 
                             mode='lines', 
                             name='50-Period EMA',
                             line=dict(color='cyan', width=1.5)))

    # Update layout
    fig.update_layout(
        title=f'{symbol} Stock Price ({interval})',
        yaxis_title='Stock Price (USD)',
        xaxis_title='Date / Time',
        xaxis_rangeslider_visible=False, # Hides the range slider
        template='plotly_dark', # Use a dark theme
        legend_title="Indicators"
    )
    
    return fig

# --- UI & MAIN APP ---

# Set page config for a wider layout
st.set_page_config(layout="wide")

# --- SIDEBAR ---
st.sidebar.title("Stock Dashboard 📈")
ticker_symbol = st.sidebar.text_input("Enter Stock Ticker:", "AAPL").upper()
time_interval = st.sidebar.selectbox("Select Time Interval:", 
                                     ('5min', '1min', '15min', '30min', '60min'), 
                                     index=0) # Default to '5min'

# --- MAIN APP LOGIC ---
st.title(f"{ticker_symbol} Real-Time Dashboard")
st.write(f"Displaying data for the last 100 intervals at `{time_interval}` resolution.")


# Fetch, process, and display data
raw_data = fetch_stock_data(ticker_symbol, time_interval)

if raw_data:
    df = process_data(raw_data)
    
    if not df.empty:
        # Display the Plotly chart
        fig = create_plot(df, ticker_symbol, time_interval)
        st.plotly_chart(fig, use_container_width=True)
        
        # Display key indicators
        st.subheader("Financial Indicators (Latest)")
        try:
            latest_data = df.iloc[-1]
            
            # Create columns for metrics
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Latest Close", f"${latest_data['Close']:.2f}")
            col2.metric("Latest Volume", f"{latest_data['Volume']:,.0f}")
            col3.metric("20-Period SMA", f"${latest_data['SMA_20']:.2f}")
            col4.metric("50-Period EMA", f"${latest_data['EMA_50']:.2f}")
        except Exception as e:
            st.warning(f"Could not display metrics. Error: {e}")

        # Display recent data in a table
        st.subheader("Recent Data")
        # Show latest data first
        st.dataframe(df.tail(10).sort_index(ascending=False), use_container_width=True)
    
    else:
        st.warning("No data processed. This might be due to an API issue or an invalid ticker.")
else:
    st.warning("Failed to fetch data. Please check the ticker symbol and ensure your API key is correct and not rate-limited.")
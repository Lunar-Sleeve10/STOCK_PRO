import yfinance as yf
from datetime import datetime, timedelta

# Fetch stock data and historical prices
def get_stock_data(stock_symbol):
    stock = yf.Ticker(stock_symbol)
    
    # Real-time stock data
    stock_info = stock.info
    print("Stock Info:", stock_info)  # Debugging line
    
    real_time_data = {
        'symbol': stock_info.get('symbol'),
        'price': stock_info.get('regularMarketPrice'),
        'change_percent': stock_info.get('regularMarketChangePercent'),
    }

    # Fetch historical data for the last 7 days
    today = datetime.today().strftime('%Y-%m-%d')
    last_week = (datetime.today() - timedelta(days=7)).strftime('%Y-%m-%d')
    hist = stock.history(start=last_week, end=today, interval="1d")
    
    historical_prices = hist['Close'].tolist()
    historical_dates = hist.index.strftime('%Y-%m-%d').tolist()

    return {
        'real_time_data': real_time_data,
        'historical_prices': historical_prices,
        'historical_dates': historical_dates
    }

# Fetch Sensex or Nifty data
def get_sensex_data(index_symbol='^BSESN'):  # Sensex default symbol
    index = yf.Ticker(index_symbol)  # Use Ticker instead of TTicker
  # Use yf.Ticker(), not yf.TTicker()
    index_info = index.info
    print("Index Info:", index_info)  # Debugging line
    return {
        'symbol': index_info.get('symbol'),
        'price': index_info.get('regularMarketPrice'),
        'change_percent': index_info.get('regularMarketChangePercent'),
    }

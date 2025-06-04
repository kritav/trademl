import yfinance as yf
import pandas as pd

def download_data(tickers, start="2020-01-01", end="2024-12-31"):
    data = yf.download(tickers, start=start, end=end)['Adj Close']
    return data.dropna()
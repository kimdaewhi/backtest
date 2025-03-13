import yfinance as yf
import backtrader as bt
import pandas as pd

def fetch_data(ticker, start_date, end_date):
    """Yahoo Finance에서 데이터 가져와서 Backtrader용으로 변환"""
    df = yf.download(ticker, start=start_date, end=end_date)
    
    # Backtrader에 맞게 인덱스 정리
    df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
    df.columns = ['open', 'high', 'low', 'close', 'volume']
    df.index = pd.to_datetime(df.index)

    return df

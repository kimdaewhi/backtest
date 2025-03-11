import yfinance as yf
import pandas as pd
import os
from dotenv import load_dotenv

# ✅ .env 로드
load_dotenv()

def load_stock_data(ticker=None, start_date=None, end_date=None):
    """
    지정된 티커(ticker)와 기간(start_date ~ end_date)에 대한 주가 데이터를 yfinance에서 가져옴.

    :param ticker: 종목 코드 (예: "ORCL")
    :param start_date: 시작 날짜 (YYYY-MM-DD)
    :param end_date: 종료 날짜 (YYYY-MM-DD)
    :return: Pandas DataFrame (종가 포함)
    """
    if ticker is None:
        ticker = os.getenv("TICKER", "ORCL")
    if start_date is None:
        start_date = os.getenv("START_DATE", "2018-01-01")
    if end_date is None:
        end_date = os.getenv("END_DATE", "2021-01-01")

    df = yf.download(ticker, start=start_date, end=end_date)
    
    if df.empty:
        raise ValueError(f"❌ 데이터 로드 실패: {ticker} ({start_date} ~ {end_date})")

    df["Date"] = df.index.astype(str)  # ✅ datetime을 문자열로 변환
    return df

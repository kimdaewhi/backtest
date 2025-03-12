import yfinance as yf
import pandas as pd
import os
from dotenv import load_dotenv

# env 로드
load_dotenv()

def load_stock_data(ticker=None, start_date=None, end_date=None):
    """
    지정된 티커(ticker)와 기간(start_date ~ end_date)에 대한 주가 데이터를 yfinance에서 가져옴.

    :param ticker: 종목 코드 (예: "ORCL")
    :param start_date: 시작 날짜 (YYYY-MM-DD)
    :param end_date: 종료 날짜 (YYYY-MM-DD)
    :return: Pandas DataFrame (종가 포함)
    """
    if not ticker or not isinstance(ticker, str):
        raise ValueError("❌ 유효한 종목 코드를 입력하세요.")
    
    if not start_date or not isinstance(start_date, str):
        raise ValueError("❌ 유효한 시작 날짜를 입력하세요.")
    
    if not end_date or not isinstance(end_date, str):
        raise ValueError("❌ 유효한 종료 날짜를 입력하세요.")

    # yfinance에서 주가 데이터 가져오기
    df = yf.download(ticker, start=start_date, end=end_date)
    
    # 데이터가 없을 경우 예외 처리
    if df.empty:
        raise ValueError(f"❌ 데이터 로드 실패: {ticker} ({start_date} ~ {end_date})")

    # 날짜를 문자열로 변환하여 컬럼 추가
    df["Date"] = df.index.astype(str)  # datetime을 문자열로 변환(이유 : Streamlit에서 날짜 인식 오류)

    # DataFrame 반환
    return df

import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

class Config:
    TICKER = os.getenv("TICKER", "ORCL")                # 티커
    START_DATE = os.getenv("START_DATE", "2018-01-01")  # 시작일
    END_DATE = os.getenv("END_DATE", "2021-01-30")      # 종료일
    INITIAL_INVESTMENT = float(os.getenv("INITIAL_INVESTMENT", "5000")) # 초기 투자금
    AVG_PRICE = float(os.getenv("AVG_PRICE", "188.3962"))             # 평균 매수가
    SHARES = int(os.getenv("SHARES", "42"))                          # 보유 주식 수량
    CASH_BALANCE = float(os.getenv("CASH_BALANCE", "0"))            # 현금 잔고

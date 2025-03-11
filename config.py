import os
from dotenv import load_dotenv

# ✅ 환경 변수 로드
load_dotenv()

class Config:
    TICKER = os.getenv("TICKER", "ORCL")
    START_DATE = os.getenv("START_DATE", "2018-01-01")
    END_DATE = os.getenv("END_DATE", "2021-01-30")
    INITIAL_INVESTMENT = float(os.getenv("INITIAL_INVESTMENT", "5000"))
    AVG_PRICE = float(os.getenv("AVG_PRICE", "188.3962"))
    SHARES = int(os.getenv("SHARES", "42"))

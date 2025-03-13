import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 환경 변수 불러오기
TICKER = os.getenv("TICKER", "AAPL")
START_DATE = os.getenv("START_DATE", "2022-01-01")
END_DATE = os.getenv("END_DATE", "2024-01-01")
INITIAL_CASH = float(os.getenv("INITIAL_CASH", 10000))

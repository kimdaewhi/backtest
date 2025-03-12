import os
from dotenv import load_dotenv
import streamlit as st

@st.cache_resource
def load_env():
    load_dotenv()
    return {
        "TICKER": os.getenv("TICKER", "ORCL"),
        "START_DATE": os.getenv("START_DATE", ""),
        "END_DATE": os.getenv("END_DATE", ""),
        "INITIAL_INVESTMENT": float(os.getenv("INITIAL_INVESTMENT", "0")),
        "AVG_PRICE": float(os.getenv("AVG_PRICE", "0")),
        "SHARES": int(os.getenv("SHARES", "0")),
        "CASH_BALANCE": float(os.getenv("CASH_BALANCE", "0"))
    }

env_config = load_env()

class Config:
    TICKER = env_config["TICKER"]
    START_DATE = env_config["START_DATE"]
    END_DATE = env_config["END_DATE"]
    INITIAL_INVESTMENT = env_config["INITIAL_INVESTMENT"]
    AVG_PRICE = env_config["AVG_PRICE"]
    SHARES = env_config["SHARES"]
    CASH_BALANCE = env_config["CASH_BALANCE"]


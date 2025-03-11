import streamlit as st
import plotly.graph_objects as go
from utils.data_loader import load_stock_data
from strategy_factory import StrategyFactory
from config import Config

# ✅ 주가 데이터 로드
df = load_stock_data()
prices = df["Close"].values
dates = df["Date"].tolist()  # ✅ datetime을 문자열로 변환

# ✅ 전략 실행 (손절 후 재매수 & DCA)
strategy_names = ["stop_loss_rebuy", "dca"]
results = {}

for name in strategy_names:
    strategy = StrategyFactory.create_strategy(name, initial_investment=Config.INITIAL_INVESTMENT, avg_price=Config.AVG_PRICE ,shares=Config.SHARES)
    results[name] = strategy.run(prices)

# ✅ Plotly 그래프 시각화
fig = go.Figure()
for name, values in results.items():
    fig.add_trace(go.Scatter(x=dates, y=values, mode="lines", name=name))

st.title("Oracle (ORCL) Backtest Results")
st.plotly_chart(fig, use_container_width=True)

# ✅ 전략별 백테스트 성과 지표 테이블
st.subheader("Backtest Performance Metrics")
st.dataframe(results)

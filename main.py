import streamlit as st
import plotly.graph_objects as go
from utils.data_loader import load_stock_data
from strategy_factory import StrategyFactory
from config import Config

# 1. 주가 데이터 로드
df = load_stock_data(Config.TICKER, Config.START_DATE, Config.END_DATE)
prices = df["Close"].values
dates = df["Date"].tolist()  # ✅ datetime을 문자열로 변환

# 2. 전략 실행 (손절 후 재매수 & DCA), 다수의 전략 실행 가능
strategy_names = ["StopLossRebuyStrategy", "DcaStrategy"]
results = {}

# 3. 전략 오브젝트 생성 및 실행
for name in strategy_names:
    # Factory 클래스에 위임한 전략 생성. 파라미터는 환경 변수에 정의된 초기값 사용
    strategy = StrategyFactory.create_strategy(
        name, 
        initial_investment=Config.INITIAL_INVESTMENT,   # 초기 투자금
        avg_price=Config.AVG_PRICE,                     # 평균 매수가
        shares=Config.SHARES                            # 보유 주식 수량
    )
    results[strategy.chart_title] = strategy.run(prices)            # 전략 실행 결과를 Dictionary에 저장

# 4. Plotly 그래프 시각화(Plotly 사용법?)
fig = go.Figure()
for name, values in results.items():
    fig.add_trace(go.Scatter(x=dates, y=values, mode="lines", name=name))

# ✅ 축 제목 추가
fig.update_layout(
    xaxis_title="날짜",  # X축 제목
    yaxis_title="평가 금액",  # Y축 제목
    legend_title="전략 (Strategy)"
)

st.title(f"Backtest Results({Config.TICKER})")
st.plotly_chart(fig, use_container_width=True)

# ✅ 전략별 백테스트 성과 지표 테이블
st.subheader("Backtest Performance Metrics")
st.dataframe(results)

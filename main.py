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
        shares=Config.SHARES,                           # 보유 주식 수량
        cash_balance=Config.CASH_BALANCE                # 현금 잔고
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


# ✅ 4. 기본 정보 테이블 출력 (차트 아래)
st.subheader("📊 기본 정보")

curr_price = 144.18

# ✅ 현재 평가 금액 및 손익 계산
current_value = Config.SHARES * curr_price
profit_loss = current_value - (Config.SHARES * Config.AVG_PRICE)
profit_loss_pct = (profit_loss / (Config.SHARES * Config.AVG_PRICE)) * 100

# ✅ DataFrame으로 변환 후 출력
basic_info = {
    "항목": ["종목", "평균 매수가", "현재가", "수량", "평가금액", "손익"],
    "값": [
        Config.TICKER,
        f"${Config.AVG_PRICE:.2f}",
        f"${curr_price:.2f}",
        f"{Config.SHARES}주",
        f"${current_value:,.2f}",
        f"{profit_loss:+,.2f} USD ({profit_loss_pct:+.2f}%)"
    ]
}
st.dataframe(basic_info)

# ✅ 전략별 백테스트 성과 지표 테이블
st.subheader("Backtest Performance Metrics")
st.dataframe(results)

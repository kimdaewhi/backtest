import numpy as np
import pandas as pd
import yfinance as yf
import streamlit as st
import plotly.graph_objects as go

# ✅ Oracle (ORCL) 주가 데이터 불러오기
ticker = "ORCL"
start_date = "2018-01-01"
end_date = "2018-01-30"

df = yf.download(ticker, start=start_date, end=end_date)
dates = df.index.astype(str)  # ✅ datetime을 문자열로 변환
prices = df["Close"].values

# ✅ 기본 투자 정보
current_price = 148.79
avg_price = 188.3962
shares = 42
initial_investment = avg_price * shares

def stop_loss_and_rebuy(prices, stop_loss_pct=-10, rebuy_gain_pct=5):
    """
    손절 후 일정 수준 반등하면 재매수하는 전략.

    :param prices: 과거 주가 데이터 (list)
    :param stop_loss_pct: 손절 기준 (ex: -10% → 10% 하락 시 손절)
    :param rebuy_gain_pct: 재매수 기준 (ex: 5% → 손절 후 5% 상승 시 재매수)
    :return: 포트폴리오 가치 변화 리스트
    """

    capital = initial_investment  # 초기 투자금 (현금)
    holding = True  # 주식 보유 상태 여부
    buy_price = avg_price  # 최초 매수가
    portfolio_values = []  # 포트폴리오 가치 추적 리스트
    stop_price = avg_price * (1 + stop_loss_pct / 100)  # 손절 기준 가격
    rebuy_price = None  # 재매수 가격 초기화
    shares_held = shares  # 현재 보유 주식 수량

    for price in prices:
        if holding:
            # 📌 보유 중인 경우 → 포트폴리오 가치는 "주식 보유량 * 현재 가격"
            portfolio_value = shares_held * price
            portfolio_values.append(portfolio_value)

            # 📌 손절 조건 충족 시 매도 (현금화)
            if price <= stop_price:
                holding = False  # 보유 상태 해제
                capital = shares_held * price  # 손절 후 남은 자본 (현금화)
                shares_held = 0  # 주식 보유량 초기화
                
                buy_price = price  # 📌 손절 후 매도한 가격을 새로운 기준으로 설정
                rebuy_price = buy_price * (1 + rebuy_gain_pct / 100)  # 📌 최신 buy_price 기준으로 반등 가격 설정
                
        else:
            # 📌 현금 보유 상태 → 포트폴리오 가치는 그대로 유지
            portfolio_values.append(capital)

            # 📌 반등 조건 충족 시 재매수
            if rebuy_price is not None and price >= rebuy_price:
                holding = True  # 다시 보유 상태로 변경
                shares_held = capital / price  # 📌 남은 자본으로 가능한 최대 개수 매수
                capital = 0  # 현금 소진
                
                buy_price = price  # 📌 새로운 매수가 업데이트!
                stop_price = buy_price * (1 + stop_loss_pct / 100)  # 📌 새로운 손절 가격 업데이트
                rebuy_price = buy_price * (1 + rebuy_gain_pct / 100)  # 📌 새로운 재매수 가격 업데이트

        # 📌 매일 포트폴리오 가치를 기록 (정확한 `buy_price` 반영)
        if holding:
            portfolio_value = shares_held * price
        else:
            portfolio_value = capital  # 현금 상태에서는 변동 없음

        portfolio_values.append(portfolio_value)

    return portfolio_values


# ✅ 분할 매수 전략(DCF)
def dca_strategy(prices, num_buys=4, dip_threshold=5, additional_funds_per_buy=1000):
    """
    개선된 Dollar-Cost Averaging (DCA) 전략
    :param prices: 과거 주가 데이터 (list)
    :param num_buys: 추가 매수 횟수
    :param dip_threshold: 추가 매수할 주가 하락률 기준 (ex: 5% 하락 시 추가 매수)
    :param additional_funds_per_buy: 매수할 때마다 추가 투자할 예수금
    :return: 포트폴리오 가치 변화 리스트
    """

    total_funds_invested = initial_investment  # 총 투자금 (초기 + 추가 매수)
    current_shares = initial_investment / avg_price  # 초기 보유 주식 수량
    portfolio_values = []  # 포트폴리오 가치 기록
    last_buy_price = avg_price  # 최초 매수가 기준

    for price in prices:
        # 주가가 일정 수준(-dip_threshold%) 하락할 때마다 추가 매수
        if (price / last_buy_price - 1) * 100 <= -dip_threshold and num_buys > 0:
            # 새로운 매수
            new_shares = additional_funds_per_buy / price  # 하락한 가격 기준으로 매수
            current_shares += new_shares
            total_funds_invested += additional_funds_per_buy  # 총 투자금 증가
            last_buy_price = price  # 최근 매수가 업데이트
            num_buys -= 1  # 남은 추가 매수 횟수 차감

        # 현재 포트폴리오 가치를 기록
        portfolio_values.append(current_shares * price)

    return portfolio_values

# ✅ 전략 실행
holding_values = np.squeeze((prices / avg_price) * initial_investment).tolist()  # ✅ 리스트 내부 리스트 문제 해결
stop_loss_results = np.squeeze(stop_loss_and_rebuy(prices)).tolist()  # ✅ 1차원 리스트로 변환
dca_results = np.squeeze(dca_strategy(prices)).tolist()  # ✅ 1차원 리스트로 변환

# ✅ 수익률 계산 함수
def calculate_metrics(portfolio_values, initial_investment):
    returns = np.array(portfolio_values) / initial_investment - 1
    max_drawdown = np.max(np.maximum.accumulate(portfolio_values) - portfolio_values)
    sharpe_ratio = np.mean(returns) / np.std(returns) * np.sqrt(252) if np.std(returns) > 0 else 0
    cagr = (portfolio_values[-1] / initial_investment) ** (1 / ((len(portfolio_values)) / 252)) - 1
    calmar_ratio = cagr / max_drawdown if max_drawdown != 0 else 0
    downside_returns = returns[returns < 0]
    sortino_ratio = np.mean(returns) / np.std(downside_returns) * np.sqrt(252) if np.std(downside_returns) > 0 else 0
    
    return {
        "평균 수익률 (%)": np.mean(returns) * 100,
        "중앙값 수익률 (%)": np.median(returns) * 100,
        "최대 수익률 (%)": np.max(returns) * 100,
        "최소 수익률 (%)": np.min(returns) * 100,
        "수익률 표준편차 (%)": np.std(returns) * 100,
        "평균 MDD (%)": max_drawdown / initial_investment * 100,
        "Sharpe Ratio": sharpe_ratio,
        "CAGR (연평균 수익률, %)": cagr * 100,
        "Calmar Ratio": calmar_ratio,
        "Sortino Ratio": sortino_ratio,
    }

# ✅ 백테스트 성과 계산
results = {
    "전략": ["Buy & Hold", "Stop Loss & Rebuy", "DCA"],
    "지표": [
        calculate_metrics(holding_values, initial_investment),
        calculate_metrics(stop_loss_results, initial_investment),
        calculate_metrics(dca_results, initial_investment)
    ]
}

df_results = pd.DataFrame(results["지표"], index=results["전략"]).round(2)

# ✅ Plotly 그래프 (정상적으로 표시됨)
fig = go.Figure([
    go.Scatter(x=dates, y=holding_values, mode="lines", name="Buy & Hold"),
    go.Scatter(x=dates, y=stop_loss_results, mode="lines", name="Stop Loss & Rebuy"),
    go.Scatter(x=dates, y=dca_results, mode="lines", name="Dollar-Cost Averaging (DCA)")
])

st.title("Oracle (ORCL) Backtest Results")
st.plotly_chart(fig, use_container_width=True)  # ✅ Streamlit에 Plotly 그래프 표시

# ✅ Plotly 테이블 추가
fig_table = go.Figure(data=[go.Table(
    header=dict(values=["전략"] + list(df_results.columns), align="center"),
    cells=dict(
        values=[df_results.index] + [df_results[col] for col in df_results.columns],
        align="center"
    )
)])

st.subheader("Backtest Performance Metrics")
st.plotly_chart(fig_table, use_container_width=True)  # ✅ Streamlit에서 테이블 표시

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

# 1. Oracle (ORCL) 주가 데이터 불러오기
ticker = "ORCL"
start_date = "2018-01-01"  # 과거 1년 데이터
end_date = "2021-01-01"

df = yf.download(ticker, start=start_date, end=end_date)
prices = df["Close"].values  # 종가 사용
dates = df.index

# 2. 기본 투자 정보 설정
current_price = 148.79   # 현재 가격
avg_price = 188.3962     # 평균 매수가
shares = 42              # 보유 수량
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



# 4. 분할 매수 전략 (DCA)
# def dca_strategy(prices, num_buys=4, dip_threshold=5):
#     """
#     Dollar-Cost Averaging (DCA) 전략 구현
#     :param prices: 과거 주가 데이터 (list)
#     :param num_buys: 추가 매수 횟수
#     :param dip_threshold: 추가 매수할 주가 하락률 기준
#     :return: 포트폴리오 가치 변화 리스트
#     """

#     capital = initial_investment  # 초기 투자금
#     cash_per_buy = capital / num_buys  # 각 매수 시 사용할 현금
#     current_shares = 0  # 현재 보유 주식 수량
#     portfolio_values = []  # 포트폴리오 가치 기록

#     last_buy_price = avg_price  # 최초 매수가 기준

#     for price in prices:
#         # 주가가 일정 수준(-dip_threshold%) 하락할 때만 추가 매수
#         if (price / last_buy_price - 1) * 100 <= -dip_threshold and num_buys > 0:
#             new_shares = cash_per_buy / price  # 주가가 떨어질수록 더 많은 주식 매수
#             current_shares += new_shares
#             last_buy_price = price  # 최근 매수가 업데이트
#             num_buys -= 1  # 남은 추가 매수 횟수 차감

#         portfolio_values.append(current_shares * price)  # 현재 포트폴리오 가치 업데이트

#     return portfolio_values


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



# 5. 존버 전략
holding_values = (prices / avg_price) * initial_investment

# 6. 전략 비교 실행
stop_loss_results = stop_loss_and_rebuy(prices)
dca_results = dca_strategy(prices)

# 7. 데이터 시각화
plt.figure(figsize=(12, 6))
plt.plot(dates, holding_values, label="Buy & Hold")
plt.plot(dates, stop_loss_results[:len(dates)], label="Stop Loss & Rebuy")
plt.plot(dates, dca_results[:len(dates)], label="Dollar-Cost Averaging(DCA)")

plt.title(f"Oracle (ORCL) Backtest results: Past Year ({start_date} ~ {end_date})") 
plt.xlabel("Date")
plt.ylabel("Portfolio Value")
plt.legend()
plt.grid()
plt.show()

# 8. 백테스트 결과를 데이터프레임으로 출력
df_results = pd.DataFrame({
    "Date": dates,
    "Holding": holding_values[:len(dates)],
    "Stop Loss & Rebuy": stop_loss_results[:len(dates)],
    "DCA": dca_results[:len(dates)]
})
import ace_tools as tools
tools.display_dataframe_to_user(name="Backtest Results (Historical Data)", dataframe=df_results)

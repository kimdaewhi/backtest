import pandas as pd
from strategies.base_strategy import BaseStrategy

class StopLossRebuyStrategy(BaseStrategy):
    """손절 후 일정 수준 반등하면 재매수하는 전략"""

    @property
    def chart_title(self) -> str:
        return "Stop Loss & Rebuy Strategy"

    def __init__(self, initial_investment, avg_price, shares, cash_balance, stop_loss_pct=-10, rebuy_gain_pct=5, max_shares_per_buy=10):
        """
        손절 후 재매수 전략 초기화
        :param initial_investment: 초기 투자금
        :param avg_price: 평균 매수가
        :param shares: 초기 보유 주식 수량
        :param cash_balance: 현금 잔고
        :param stop_loss_pct: 손절 기준 (%) (예: -10%)
        :param rebuy_gain_pct: 재매수 기준 (%) (예: 5%)
        :param max_shares_per_buy: 한 번에 매수할 최대 주식 개수
        """
        self.initial_investment = initial_investment
        self.avg_price = avg_price
        self.shares = shares
        self.stop_loss_pct = stop_loss_pct
        self.rebuy_gain_pct = rebuy_gain_pct
        self.cash_balance = cash_balance
        self.max_shares_per_buy = max_shares_per_buy

    def run(self, prices) -> pd.Series:
        """손절 후 일정 수준 반등하면 재매수하는 전략 실행"""

        # ✅ 리스트 입력을 Pandas Series로 변환
        if not isinstance(prices, pd.Series):
            prices = pd.Series(prices.squeeze())

        capital = self.shares * self.avg_price  # 초기 투자금
        holding = True  # 주식 보유 여부
        portfolio_values = []  # 포트폴리오 가치 기록 리스트
        stop_price = self.avg_price * (1 + self.stop_loss_pct / 100)  # 초기 손절가
        rebuy_price = None  # 재매수 가격 초기화
        shares_held = self.shares  # 초기 보유 주식 수량

        print("\n📊 [매매 로그]")
        print("----------------------------------------------------")

        for i, price in enumerate(prices):
            date = prices.index[i]  # 날짜 정보
            portfolio_value = shares_held * price  # ✅ 주식 평가 금액만 반영

            if holding:
                portfolio_values.append(portfolio_value)

                if price <= stop_price:
                    # 📌 손절: 주식 매도 후 현금 증가
                    sell_value = shares_held * price  # 매도 금액
                    profit = sell_value - (shares_held * self.avg_price)  # 손익 계산

                    self.cash_balance += sell_value  # 예수금 증가
                    capital = 0  # ✅ 주식 매도 후 보유 주식 평가 금액 = 0
                    shares_held = 0  # 주식 없음
                    rebuy_price = price * (1 + self.rebuy_gain_pct / 100)  # 재매수 가격 설정
                    holding = False

                    print(
                        f"[{date}] 🟥 손절 매도 | 가격: ${price:.2f}, 수량: {self.shares}주 | "
                        f"매도 금액: ${sell_value:,.2f} | 손익: {profit:+,.2f} USD"
                    )

            else:
                portfolio_values.append(portfolio_value)

                if rebuy_price is not None and price >= rebuy_price:
                    # 📌 재매수: 예수금으로 주식 구매
                    max_shares = min(self.max_shares_per_buy, self.cash_balance // price)  # 최대 매수 제한 적용
                    buy_value = max_shares * price  # 총 매수 금액

                    if max_shares > 0:
                        holding = True
                        shares_held += max_shares
                        self.cash_balance -= buy_value  # 예수금 감소
                        capital = shares_held * price  # ✅ 주식 평가 금액만 반영
                        stop_price = price * (1 + self.stop_loss_pct / 100)  # 손절가 설정
                        rebuy_price = price * (1 + self.rebuy_gain_pct / 100)  # 재매수 가격 설정

                        print(
                            f"[{date}] 🟩 재매수 | 가격: ${price:.2f}, 수량: {max_shares}주 | "
                            f"매수 금액: ${buy_value:,.2f} | 남은 예수금: ${self.cash_balance:,.2f}"
                        )

        return pd.Series(portfolio_values, index=prices.index)  # ✅ 정상 작동!

import pandas as pd
from strategies.base_strategy import BaseStrategy

class StopLossRebuyStrategy(BaseStrategy):
    """일부 손절 후 일정 수준 반등하면 재매수하는 전략"""

    @property
    def chart_title(self) -> str:
        return "Stop Loss & Rebuy Strategy"

    def __init__(
        self, initial_investment, avg_price, shares, cash_balance,
        stop_loss_pct=-10, rebuy_gain_pct=5, sell_ratio=0.3, buy_ratio=0.2
    ):
        """
        손절 후 일부 재매수 전략 초기화

        :param initial_investment: 초기 투자금
        :param avg_price: 평균 매수가
        :param shares: 초기 보유 주식 수량
        :param cash_balance: 현금 잔고
        :param stop_loss_pct: 손절 기준 (%) (예: -10%)
        :param rebuy_gain_pct: 재매수 기준 (%) (예: 5%)
        :param sell_ratio: 손절 시 매도 비율 (예: 30%)
        :param buy_ratio: 재매수 시 매수 비율 (예: 20%)
        """
        self.initial_investment = initial_investment
        self.avg_price = avg_price
        self.shares = shares
        self.cash_balance = cash_balance
        self.stop_loss_pct = stop_loss_pct
        self.rebuy_gain_pct = rebuy_gain_pct
        self.sell_ratio = sell_ratio
        self.buy_ratio = buy_ratio

    def run(self, prices) -> pd.Series:
        """손절 후 일부 매도, 재매수하는 전략 실행"""

        # ✅ 리스트 입력을 Pandas Series로 변환
        if not isinstance(prices, pd.Series):
            prices = pd.Series(prices.squeeze())

        portfolio_values = []  # 포트폴리오 가치 기록 리스트
        stop_price = self.avg_price * (1 + self.stop_loss_pct / 100)  # 초기 손절가
        rebuy_price = self.avg_price * (1 + self.rebuy_gain_pct / 100)  # 초기 추매 가격
        shares_held = self.shares  # 보유 주식 수량

        print("\n📊 [매매 로그]")
        print("----------------------------------------------------")

        for i, price in enumerate(prices):
            date = prices.index[i]  # 날짜 정보
            portfolio_value = shares_held * price  # ✅ 주식 평가 금액만 반영

            # ✅ 손절 조건 (일부 매도)
            if price <= stop_price and shares_held > 0:
                shares_to_sell = int(shares_held * self.sell_ratio)  # 손절 시 매도할 수량
                if shares_to_sell > 0:
                    sell_value = shares_to_sell * price  # 매도 금액
                    profit = sell_value - (shares_to_sell * self.avg_price)  # 손익 계산

                    self.cash_balance += sell_value  # 예수금 증가
                    shares_held -= shares_to_sell  # 보유 주식 감소

                    stop_price = price * (1 + self.stop_loss_pct / 100)  # 손절가 재설정
                    rebuy_price = price * (1 + self.rebuy_gain_pct / 100)  # 재매수가 재설정

                    print(
                        f"[{date}] 🟥 일부 손절 매도 | 가격: ${price:.2f}, 수량: {shares_to_sell}주 | "
                        f"매도 금액: ${sell_value:,.2f} | 손익: {profit:+,.2f} USD | 남은 예수금: ${self.cash_balance:,.2f}"
                    )

            # ✅ 추가 매수 조건 (일부 매수)
            elif price >= rebuy_price and self.cash_balance > 0:
                available_cash = self.cash_balance * self.buy_ratio  # 매수 가능 금액
                shares_to_buy = int(available_cash // price)  # 매수 가능한 주식 수
                buy_value = shares_to_buy * price  # 총 매수 금액

                if shares_to_buy > 0 and buy_value <= self.cash_balance:
                    self.cash_balance -= buy_value  # 예수금 감소
                    new_avg_price = ((self.avg_price * shares_held) + buy_value) / (shares_held + shares_to_buy)  
                    shares_held += shares_to_buy  # 보유 주식 증가

                    self.avg_price = new_avg_price  # 평균 매수가 업데이트
                    stop_price = self.avg_price * (1 + self.stop_loss_pct / 100)  # 손절가 재설정
                    rebuy_price = self.avg_price * (1 + self.rebuy_gain_pct / 100)  # 재매수가 재설정

                    print(
                        f"[{date}] 🟩 일부 추가 매수 | 가격: ${price:.2f}, 수량: {shares_to_buy}주 | "
                        f"매수 금액: ${buy_value:,.2f} | 남은 예수금: ${self.cash_balance:,.2f} | 평균 매수가: ${self.avg_price:.2f}"
                    )

            portfolio_values.append(portfolio_value)  # ✅ 포트폴리오 평가금 반영

        return pd.Series(portfolio_values, index=prices.index)  # ✅ 정상 작동!

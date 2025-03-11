import pandas as pd
from strategies.base_strategy import BaseStrategy

class StopLossRebuyStrategy(BaseStrategy):
    """손절 후 일정 수준 반등하면 재매수하는 전략"""

    def __init__(self, initial_investment, avg_price, shares, stop_loss_pct=-10, rebuy_gain_pct=5):
        self.initial_investment = initial_investment
        self.avg_price = avg_price  # 초기 매수가
        self.shares = shares  # 초기 보유 주식 수량
        self.stop_loss_pct = stop_loss_pct  # 손절 기준 (예: -10%)
        self.rebuy_gain_pct = rebuy_gain_pct  # 재매수 기준 (예: 5%)

    def run(self, prices) -> pd.Series:
        """손절 후 일정 수준 반등하면 재매수하는 전략 실행"""

        # ✅ 리스트 입력을 Pandas Series로 변환 (2D → 1D 변환 추가)
        if not isinstance(prices, pd.Series):
            prices = pd.Series(prices.squeeze())  # ✅ 2D → 1D 변환 후 Series 생성

        capital = self.initial_investment  # 초기 투자금 (현금)
        holding = True  # 주식 보유 여부
        portfolio_values = []  # 포트폴리오 가치 기록 리스트
        stop_price = self.avg_price * (1 + self.stop_loss_pct / 100)  # 손절 가격
        rebuy_price = None  # 재매수 가격 초기화
        shares_held = self.shares  # 초기 보유 주식 수량

        for price in prices:
            if holding:
                portfolio_value = shares_held * price
                portfolio_values.append(portfolio_value)

                if price <= stop_price:
                    holding = False
                    capital = shares_held * price
                    shares_held = 0
                    rebuy_price = price * (1 + self.rebuy_gain_pct / 100)

            else:
                portfolio_values.append(capital)

                if rebuy_price is not None and price >= rebuy_price:
                    holding = True
                    shares_held = capital / price
                    capital = 0
                    stop_price = price * (1 + self.stop_loss_pct / 100)
                    rebuy_price = price * (1 + self.rebuy_gain_pct / 100)

        return pd.Series(portfolio_values, index=prices.index)  # ✅ 정상 작동!


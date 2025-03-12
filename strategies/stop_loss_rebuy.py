import pandas as pd
from strategies.base_strategy import BaseStrategy

class StopLossRebuyStrategy(BaseStrategy):
    """손절 후 일정 수준 반등하면 재매수하는 전략"""

    @property
    def chart_title(self) -> str:
        return "Stop Loss & Rebuy Strategy"

    def __init__(self, initial_investment, avg_price, shares, cash_balance, stop_loss_pct=-10, rebuy_gain_pct=5):
        """
        손절 후 재매수 전략 초기화
        :param initial_investment: 초기 투자금
        :param avg_price: 평균 매수가
        :param shares: 초기 보유 주식 수량
        :param cash_balance: 현금 잔고
        :param stop_loss_pct: 손절 기준 (%) (예: -10%)
        :param rebuy_gain_pct: 재매수 기준 (%) (예: 5%)
        """
        self.initial_investment = initial_investment
        self.avg_price = avg_price
        self.shares = shares
        self.stop_loss_pct = stop_loss_pct
        self.rebuy_gain_pct = rebuy_gain_pct
        self.cash_balance = cash_balance

    def run(self, prices) -> pd.Series:
        """손절 후 일정 수준 반등하면 재매수하는 전략 실행"""

        # ✅ 리스트 입력을 Pandas Series로 변환 (2D → 1D 변환 추가)
        if not isinstance(prices, pd.Series):
            prices = pd.Series(prices.squeeze())  # ✅ 2D → 1D 변환 후 Series 생성

        capital = self.initial_investment  # 초기 투자금 (현금)
        holding = True  # 주식 보유 여부
        portfolio_values = []  # 포트폴리오 가치 기록 리스트
        stop_price = self.avg_price * (1 + self.stop_loss_pct / 100)  # 손절가가 초기 매수가격 기준으로 설정
        rebuy_price = None  # 재매수 가격 초기화
        shares_held = self.shares  # 초기 보유 주식 수량

        for price in prices:
            if holding:
                # 주식 보유중이라면 평가 금액 계산 및 추가
                portfolio_value = shares_held * price
                portfolio_values.append(portfolio_value)

                if price <= stop_price:
                    # 손절가가 도달 시, 주식을 현금으로 전환
                    holding = False         # 이걸 다 파는거야...?
                    capital += shares_held * price  # 매도 후 현금 증가
                    cash_balance = capital  # 예수금 업데이트
                    shares_held = 0         # 보유 주식 : 0
                    rebuy_price = price * (1 + self.rebuy_gain_pct / 100)   # 재매수 가격 설정(5% 상승)

            else:
                # 주식 보유중이 아니라면 현금을 주식으로 전환
                portfolio_values.append(capital)

                if rebuy_price is not None and price >= rebuy_price:
                    # 주가가 재매수 가격 도달 시, 매수 진행
                    total_available = capital + cash_balance  # 매수 가능한 총 자산
                    shares_to_buy = total_available / price  # 매수 가능 주식 수 계산

                    if shares_to_buy > 0:  # 매수 가능한 경우만 실행
                        holding = True
                        capital -= shares_to_buy * price  # 예수금에서 매수 금액 차감
                        shares_held += shares_to_buy  # 보유 주식 업데이트
                        stop_price = price * (1 + self.stop_loss_pct / 100)  # 새로운 손절가 설정
                        rebuy_price = price * (1 + self.rebuy_gain_pct / 100)  # 새로운 재매수가 설정

        return pd.Series(portfolio_values, index=prices.index)  # ✅ 정상 작동!


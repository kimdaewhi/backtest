import pandas as pd
from strategies.base_strategy import BaseStrategy

class DcaStrategy(BaseStrategy):
    """Dollar-Cost Averaging (DCA) 전략"""

    @property
    def chart_title(self) -> str:
        return "DCA Strategy"

    def __init__(self, initial_investment, avg_price, shares, cash_balance, num_buys=4, dip_threshold=5, additional_funds_per_buy=1000):
        """
        DCA 전략 초기화
        :param initial_investment: 초기 투자금
        :param avg_price: 평균 매수가
        :param shares: 초기 보유 주식 수량
        :param cash_balance: 현금 잔고
        :param num_buys: 추가 매수 횟수
        :param dip_threshold: 추가 매수할 주가 하락률 기준 (%)
        :param additional_funds_per_buy: 매수할 때마다 추가 투자할 예수금
        """
        self.initial_investment = initial_investment
        self.avg_price = avg_price
        self.shares = shares
        self.num_buys = num_buys
        self.dip_threshold = dip_threshold
        self.additional_funds_per_buy = additional_funds_per_buy

    def run(self, prices) -> pd.Series:
        """DCA 전략 실행"""
        if not isinstance(prices, pd.Series):
            prices = pd.Series(prices.squeeze())  # 리스트 → Pandas Series 변환

        total_funds_invested = self.initial_investment  # 총 투자금
        current_shares = self.shares  # 현재 보유 주식 수량
        portfolio_values = []
        last_buy_price = self.avg_price  # 최초 매수가 기준

        for price in prices:
            # 📌 주가가 일정 수준(-dip_threshold%) 하락하면 추가 매수
            if (price / last_buy_price - 1) * 100 <= -self.dip_threshold and self.num_buys > 0:
                new_shares = self.additional_funds_per_buy / price  # ✅ 하락한 가격 기준으로 매수
                current_shares += new_shares
                total_funds_invested += self.additional_funds_per_buy  # ✅ 총 투자금 증가
                last_buy_price = price  # ✅ 최근 매수가 업데이트
                self.num_buys -= 1  # ✅ 남은 추가 매수 횟수 차감

            # 📌 현재 포트폴리오 가치를 기록
            portfolio_values.append(current_shares * price)

        return pd.Series(portfolio_values, index=prices.index)

import backtrader as bt

class SMACrossover(bt.Strategy):
    params = (("short_period", 10), ("long_period", 50))

    def __init__(self):
        self.sma_short = bt.indicators.SimpleMovingAverage(period=self.params.short_period)
        self.sma_long = bt.indicators.SimpleMovingAverage(period=self.params.long_period)

    def next(self):
        if self.sma_short[0] > self.sma_long[0] and self.sma_short[-1] <= self.sma_long[-1]:
            self.buy()  # 골든 크로스 (매수)
        elif self.sma_short[0] < self.sma_long[0] and self.sma_short[-1] >= self.sma_long[-1]:
            self.sell()  # 데드 크로스 (매도)

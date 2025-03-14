import backtrader as bt

class SMACrossover(bt.Strategy):
    params = dict(short_period=10, long_period=50)

    def __init__(self):
        self.sma_short = bt.indicators.SimpleMovingAverage(period=self.params.short_period)
        self.sma_long = bt.indicators.SimpleMovingAverage(period=self.params.long_period)
        self.trades = []  # ✅ 매매 기록 저장 리스트 추가

    def next(self):
        if self.sma_short[0] > self.sma_long[0] and self.sma_short[-1] <= self.sma_long[-1]:
            print("🔴[골든 크로스 발생] 매수")
            self.buy()
            self.trades.append({"date": self.datas[0].datetime.date(0), "price": self.data.close[0], "type": "buy"})  # ✅ 매매 기록 저장

        elif self.sma_short[0] < self.sma_long[0] and self.sma_short[-1] >= self.sma_long[-1]:
            print("🔵[데드 크로스 발생] 매도")
            self.sell()
            self.trades.append({"date": self.datas[0].datetime.date(0), "price": self.data.close[0], "type": "sell"})  # ✅ 매매 기록 저장

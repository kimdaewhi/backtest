import backtrader as bt
from utils.data_loader import fetch_data
from utils.plot import plot_backtest_results  # ✅ 추가
from strategy_factory import get_strategy
from config import STRATEGY_CONFIGS

def run_backtest(strategy_name):
    if strategy_name not in STRATEGY_CONFIGS:
        print(f"❌ {strategy_name} 설정을 찾을 수 없습니다.")
        return

    strategy_config = STRATEGY_CONFIGS[strategy_name]
    ticker = strategy_config["ticker"]
    start_date = strategy_config["start_date"]
    end_date = strategy_config["end_date"]
    initial_cash = strategy_config["initial_cash"]
    strategy_params = strategy_config.get("params", {})

    cerebro = bt.Cerebro()
    cerebro.broker.set_cash(initial_cash)

    df = fetch_data(ticker, start_date, end_date)
    data = bt.feeds.PandasData(dataname=df)

    strategy = get_strategy(strategy_name)
    if strategy is None:
        print(f"❌ {strategy_name} 전략을 찾을 수 없습니다.")
        return

    cerebro.addstrategy(strategy, **strategy_params)
    cerebro.adddata(data)

    # 🔥 실행 후 전략 객체 가져오기
    strat = cerebro.run()[0]  # ✅ 실행 후 전략 객체 받아오기

    # 📊 체결된 거래 내역 가져오기 (변경됨!)
    trades = []
    if hasattr(strat, "trades") and strat.trades:  # ✅ 전략이 거래 데이터를 저장하고 있는 경우만
        for trade in strat.trades:
            trades.append({
                # "date": bt.num2date(trade["date"]),  # ✅ datetime 변환 필수
                "date": trade["date"], 
                "price": trade["price"],
                "type": trade["type"]
            })

    # ✅ SMA 계산
    short_sma = df['close'].rolling(strategy_params['short_period']).mean()
    long_sma = df['close'].rolling(strategy_params['long_period']).mean()

    # 📊 차트 표시
    plot_backtest_results(df, trades, short_sma, long_sma)

if __name__ == "__main__":
    run_backtest("sma_crossover")

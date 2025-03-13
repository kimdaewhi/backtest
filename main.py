import backtrader as bt
from utils.data_loader import fetch_data
from strategy_factory import get_strategy
from config import STRATEGY_CONFIGS  # ✅ 전략별 설정 불러오기

def run_backtest(strategy_name):
    if strategy_name not in STRATEGY_CONFIGS:
        print(f"❌ {strategy_name} 설정을 찾을 수 없습니다.")
        return

    # ✅ 전략별 개별 설정 불러오기
    strategy_config = STRATEGY_CONFIGS[strategy_name]
    ticker = strategy_config["ticker"]
    start_date = strategy_config["start_date"]
    end_date = strategy_config["end_date"]
    initial_cash = strategy_config["initial_cash"]
    strategy_params = strategy_config.get("params", {})

    cerebro = bt.Cerebro()
    cerebro.broker.set_cash(initial_cash)

    # 데이터 로드
    df = fetch_data(ticker, start_date, end_date)
    data = bt.feeds.PandasData(dataname=df)

    # 전략 동적 로딩 및 인스턴스 생성
    strategy = get_strategy(strategy_name)
    if strategy is None:
        print(f"❌ {strategy_name} 전략을 찾을 수 없습니다.")
        return

    cerebro.addstrategy(strategy, **strategy_params)  # ✅ 개별 전략별 params 전달
    cerebro.adddata(data)

    # 실행
    print(f"💰 초기 자본: {initial_cash}")
    cerebro.run()
    print(f"💰 최종 자본: {cerebro.broker.getvalue()}")

    # 차트 출력
    cerebro.plot()

if __name__ == "__main__":
    run_backtest("sma_crossover")  # ✅ 전략 이름만 전달하면 설정 자동 적용!

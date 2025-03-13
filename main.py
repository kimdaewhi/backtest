import backtrader as bt
from utils.data_loader import fetch_data
import config
from strategy_factory import get_strategy

def run_backtest(strategy_name):
    cerebro = bt.Cerebro()

    # 초기 자본 설정
    cerebro.broker.set_cash(config.INITIAL_CASH)

    # 데이터 로드
    df = fetch_data(config.TICKER, config.START_DATE, config.END_DATE)
    data = bt.feeds.PandasData(dataname=df)

    # 전략 가져오기
    strategy = get_strategy(strategy_name)
    if strategy is None:
        print(f"❌ {strategy_name} 전략을 찾을 수 없습니다.")
        return

    # Cerebro에 전략 추가
    cerebro.addstrategy(strategy)

    # 데이터 추가
    cerebro.adddata(data)

    # 실행
    print(f"💰 초기 자본: {config.INITIAL_CASH}")
    cerebro.run()
    print(f"💰 최종 자본: {cerebro.broker.getvalue()}")

    # 차트 출력
    cerebro.plot()



if __name__ == "__main__":
    run_backtest("sma_crossover")

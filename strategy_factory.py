import importlib
import backtrader as bt

def get_strategy(strategy_name):
    """ 전략 클래스 동적 로딩 """
    strategies_path = "strategies"  # 전략 파일이 있는 디렉토리
    strategy_file = f"{strategies_path}.{strategy_name}"  # ex) strategies.sma_crossover
    try:
        module = importlib.import_module(strategy_file)

        # `bt.Strategy`를 상속한 클래스를 자동으로 찾기
        strategy_class = None
        for attr in dir(module):
            obj = getattr(module, attr)
            if isinstance(obj, type) and issubclass(obj, bt.Strategy) and obj is not bt.Strategy:
                strategy_class = obj
                break  # 첫 번째 전략 클래스 발견 시 중단

        if strategy_class is None:
            raise AttributeError(f"⚠ {strategy_name} 전략을 찾을 수 없습니다.")

        return strategy_class  # Class 반환

    except (ModuleNotFoundError, AttributeError) as e:
        print(f"❌ 전략 {strategy_name}을(를) 찾을 수 없습니다: {e}")
        return None

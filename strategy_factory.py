from strategies.stop_loss_rebuy import StopLossRebuyStrategy
from strategies.dca_strategy import DcaStrategy

class StrategyFactory:
    """사용자가 선택한 전략을 생성하는 Factory 클래스"""

    @staticmethod
    def create_strategy(strategy_name, **kwargs):
        strategies = {
            "stop_loss_rebuy": StopLossRebuyStrategy,
            "dca": DcaStrategy
        }
        if strategy_name in strategies:
            return strategies[strategy_name](**kwargs)
        raise ValueError(f"지원하지 않는 전략: {strategy_name}")

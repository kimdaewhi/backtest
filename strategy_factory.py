from strategies.stop_loss_rebuy import StopLossRebuyStrategy
from strategies.dca_strategy import DcaStrategy

class StrategyFactory:
    """사용자가 선택한 전략을 생성하는 Factory 클래스"""

    @staticmethod
    def create_strategy(strategy_name, **kwargs):
        """
        사용자가 선택한 전략을 생성하는 Factory 메서드
        :param strategy_name: 전략 이름
        :param kwargs: 전략 생성에 필요한 추가 인자
        :return: 전략 오브젝트
        """

        # 이 부분은 하드 코딩을 피하기 위해 수정할 필요가 있음.
        # 특히 main.py에서 전략 실행 시 전략 이름을 하드 코딩하고 factory 내부에서 매핑하는 방식은 좋지 않음.
        strategies = {
            "stop_loss_rebuy": StopLossRebuyStrategy,
            "dca": DcaStrategy
        }

        if strategy_name in strategies:
            return strategies[strategy_name](**kwargs)
        raise ValueError(f"지원하지 않는 전략: {strategy_name}")

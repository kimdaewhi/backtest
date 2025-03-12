import importlib
import pkgutil
import inspect
from strategies.base_strategy import BaseStrategy

class StrategyFactory:
    """사용자가 선택한 전략을 동적으로 로드하는 Factory 클래스"""

    _strategies = {}  # ✅ 전략 저장 (딕셔너리)

    @classmethod
    def _discover_strategies(cls):
        """ strategies 폴더 내에서 자동으로 전략 클래스를 찾고 등록 """
        package_name = "strategies"
        for _, module_name, _ in pkgutil.iter_modules([package_name]):
            module = importlib.import_module(f"{package_name}.{module_name}")

            for name, obj in inspect.getmembers(module, inspect.isclass):
                if issubclass(obj, BaseStrategy) and obj is not BaseStrategy:
                    cls._strategies[name.lower()] = obj  # 전략 이름을 소문자로 변환하여 매핑

    @classmethod
    def create_strategy(cls, strategy_name, **kwargs):
        """
        사용자가 선택한 전략을 생성하는 Factory 메서드
        :param strategy_name: 전략 이름
        :param kwargs: 전략 생성에 필요한 추가 인자
        :return: 전략 오브젝트
        """
        if not cls._strategies:
            cls._discover_strategies()  # 전략 목록을 자동 로드

        strategy_class = cls._strategies.get(strategy_name.lower())
        if not strategy_class:
            raise ValueError(f"지원하지 않는 전략: {strategy_name}")

        return strategy_class(**kwargs)

from abc import ABC, abstractmethod
import pandas as pd

class BaseStrategy(ABC):
    """모든 전략이 따라야 하는 기본 인터페이스"""
    
    @abstractmethod
    def run(self, prices: pd.Series) -> pd.Series:
        pass

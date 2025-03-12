from abc import ABC, abstractmethod
import pandas as pd

class BaseStrategy(ABC):
    """모든 전략이 따라야 하는 기본 인터페이스"""

    @property
    @abstractmethod
    def chart_title(self) -> str:
        """차트 제목"""
        pass
    
    @abstractmethod
    def run(self, prices: pd.Series) -> pd.Series:
        """각 전략의 실행 메서드"""
        pass

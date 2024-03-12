from abc import ABC, abstractmethod


class CPDResult(ABC):
    """Abstract class for result containers for bench runs"""

    @abstractmethod
    def get_result_as_dict(self) -> dict:
        """Returns the result of the bench run as python dict"""
        pass

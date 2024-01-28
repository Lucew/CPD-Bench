from abc import ABC, abstractmethod

from cpdbench.control.CPDFullResult import CPDFullResult


class FrontendRenderer(ABC):
    """Abstract class for a frontend renderer which shows a CPDResult graphically."""

    @abstractmethod
    def show_results(self, results: CPDFullResult) -> None:
        """Show the results of a CPD run graphically - for example in a web browser or as pdf
        :param results: the run results
        """
        pass

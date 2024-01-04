from abc import abstractmethod, ABC
from numpy import ndarray


class CPDDataset(ABC):
    """
    Abstract class representing a dataset.
    """

    @abstractmethod
    def init(self) -> None:
        """
        Initialization method to prepare the dataset.
        Examples: Open a file, open a db connection etc.
        """
        pass

    @abstractmethod
    def get_signal(self) -> tuple[ndarray, list[int]]:
        """
        Returns the timeseries as numpy array.
        :return: A 2D ndarray containing the timeseries (time x feature)
        """
        pass
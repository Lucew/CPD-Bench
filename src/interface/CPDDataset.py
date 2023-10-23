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
    def get_length(self) -> int:
        """
        Returns the number of signals from a dataset.
        :return: number of signals
        """
        pass

    @abstractmethod
    def get_signal(self, signal_index: int) -> ndarray:
        """
        Returns the timeseries of a given signal.
        :param signal_index: index of the required signal
        :return: A 2D ndarray containing the timeseries (time x feature)
        """
        pass

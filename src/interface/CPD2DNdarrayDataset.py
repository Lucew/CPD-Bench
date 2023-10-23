from numpy import ndarray

from interface.CPDDataset import CPDDataset


class CPD2DNdarrayDataset(CPDDataset):

    def __init__(self, numpy_array):
        self.ndarray = numpy_array

    def init(self) -> None:
        pass

    def get_signal(self, signal_index: int) -> ndarray:
        return self.ndarray

    def get_length(self) -> int:
        return 1

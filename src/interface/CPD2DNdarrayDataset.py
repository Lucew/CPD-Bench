from numpy import ndarray

from interface.CPDDataset import CPDDataset


class CPD2DNdarrayDataset(CPDDataset):

    def __init__(self, numpy_array, ground_truths):
        self._ndarray = numpy_array
        self._ground_truths = ground_truths

    def init(self) -> None:
        pass

    def get_signal(self, signal_index: int) -> tuple[ndarray, list[int]]:
        return self._ndarray, self._ground_truths

    def get_length(self) -> int:
        return 1

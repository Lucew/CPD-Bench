from numpy import ndarray

from cpdbench.interface.CPDDataset import CPDDataset


class CPD2DNdarrayDataset(CPDDataset):

    def get_validation_preview(self) -> tuple[ndarray, list[int]]:
        return self._ndarray, self._ground_truths

    def __init__(self, numpy_array, ground_truths):
        self._ndarray = numpy_array
        self._ground_truths = ground_truths

    def init(self) -> None:
        pass

    def get_signal(self) -> tuple[ndarray, list[int]]:
        return self._ndarray, self._ground_truths

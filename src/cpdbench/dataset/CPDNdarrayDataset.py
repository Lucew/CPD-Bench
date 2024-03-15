from numpy import ndarray

from cpdbench.dataset.CPDDataset import CPDDataset


class CPDNdarrayDataset(CPDDataset):

    def get_validation_preview(self) -> tuple[ndarray, list[int]]:
        return self._validation_array, self._validation_ground_truths

    def __init__(self, numpy_array, ground_truths, validation_amount=-1):
        self._ndarray = numpy_array
        self._ground_truths = ground_truths
        if validation_amount == -1:
            self._validation_array = self._ndarray[:, :]
        else:
            self._validation_array = self._ndarray[:, 0:validation_amount]
        validation_array_length = self._validation_array.shape[1]
        self._validation_ground_truths = [el for el in self._ground_truths if el < validation_array_length]

    def init(self) -> None:
        pass

    def get_signal(self) -> tuple[ndarray, list[int]]:
        return self._ndarray, self._ground_truths

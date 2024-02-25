from numpy import ndarray, memmap

from cpdbench.dataset.CPDDataset import CPDDataset


class CPD2DFromFileDataset(CPDDataset):

    def __init__(self, file_path: str, dtype: str, ground_truths: list[int]):
        self.file_path = file_path
        self.dtype = dtype
        self._array = None
        self._ground_truths = ground_truths

    def init(self) -> None:
        self._array = memmap(self.file_path, self.dtype, mode='r')

    def get_signal(self) -> tuple[ndarray, list[int]]:
        return self._array, self._ground_truths

    def get_validation_preview(self) -> tuple[ndarray, list[int]]:
        return self._array, self._ground_truths

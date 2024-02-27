from numpy import ndarray, memmap

from cpdbench.dataset.CPDDataset import CPDDataset


class CPD2DFromFileDataset(CPDDataset):
    """Implementation of CPDDataset where the data source is large numpy array saved as file via memmap.
    With this implementation the framework can use very large datasets which are not completely loaded
    into the main memory. Instead numpy will lazy load all needed data points.
    """

    def __init__(self, file_path: str, dtype: str, ground_truths: list[int]):
        """Constructor
        :param file_path: The absolute or relative path to numpy file.
        :param dtype: The data type in which the numpy array was saved.
        :param ground_truths: The ground truth changepoints as integer list.
        """
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

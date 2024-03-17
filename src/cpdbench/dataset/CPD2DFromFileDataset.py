from numpy import ndarray, memmap

from cpdbench.dataset.CPDDataset import CPDDataset


class CPD2DFromFileDataset(CPDDataset):
    """Implementation of CPDDataset where the data source is large numpy array saved as file via memmap.
    With this implementation the framework can use very large datasets which are not completely loaded
    into the main memory. Instead, numpy will lazy load all needed data points.
    """

    def __init__(self, file_path: str, dtype: str, ground_truths: list[int], validation_amount=-1):
        """Constructor
        :param file_path: The absolute or relative path to numpy file.
        :param dtype: The data type in which the numpy array was saved.
        :param ground_truths: The ground truth changepoints as integer list.
        """
        self.file_path = file_path
        self.dtype = dtype
        self._array = None
        self._ground_truths = ground_truths
        self._validation_amount = validation_amount

    def init(self) -> None:
        self._array = memmap(self.file_path, self.dtype, mode='r')
        if self._validation_amount == -1:
            self._validation_array = self._array[:]
        else:
            self._validation_array = self._array[0:self._validation_amount]
        validation_array_length = self._validation_array.shape[0]
        self._validation_ground_truths = [el for el in self._ground_truths if el < validation_array_length]

    def get_signal(self) -> tuple[ndarray, list[int]]:
        return self._array, self._ground_truths

    def get_validation_preview(self) -> tuple[ndarray, list[int]]:
        return self._validation_array, self._validation_ground_truths

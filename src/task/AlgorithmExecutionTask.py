from collections.abc import Iterable

from numpy import ndarray

from interface.CPDDataset import CPDDataset
from task.Task import Task


class AlgorithmExecutionTask(Task):
    def __init__(self, function):
        self._function = function

    def validate_task(self) -> None:
        pass

    def validate_input(self, *args) -> None:
        pass

    def execute(self, data: ndarray) -> tuple[Iterable, Iterable]:
        alg_res_index, alg_res_scores = self._function(data)
        return alg_res_index, alg_res_scores

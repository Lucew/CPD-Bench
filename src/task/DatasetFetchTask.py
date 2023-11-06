from collections.abc import Iterable

from numpy import ndarray

from interface.CPDDataset import CPDDataset
from task.Task import Task


class DatasetFetchTask(Task):
    def __init__(self, function):
        self._function = function

    def validate_task(self) -> None:
        pass

    def validate_input(self, *args) -> None:
        pass

    def execute(self) -> CPDDataset:
        dataset: CPDDataset = self._function()
        dataset.init()
        return dataset

    def get_task_name(self) -> str:
        return "d:" + self._function.__name__

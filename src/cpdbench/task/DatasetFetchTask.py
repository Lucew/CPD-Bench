from cpdbench.exception import InputValidationException
from cpdbench.interface import CPDDataset
from cpdbench.task.Task import Task

import inspect

from cpdbench.utils.Utils import get_name_of_function


class DatasetFetchTask(Task):
    def __init__(self, function):
        self._function = function

    def validate_task(self) -> None:
        # Check number of args
        full_arg_spec = inspect.getfullargspec(self._function)
        if len(full_arg_spec.args) > 0:
            # Wrong number of arguments
            function_name = get_name_of_function(self._function)
            raise InputValidationException("The number of arguments for the dataset task '{0}' is {1} but should be 0."
                                           .format(function_name, len(full_arg_spec.args)))


    def validate_input(self, *args) -> None:
        pass

    def execute(self) -> CPDDataset:
        dataset: CPDDataset = self._function()
        dataset.init()
        return dataset

    def get_task_name(self) -> str:
        return "dataset:" + self._function.__name__

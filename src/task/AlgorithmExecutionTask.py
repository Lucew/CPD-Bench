from collections.abc import Iterable

from numpy import ndarray

from exception.InputValidationException import InputValidationException
from interface.CPDDataset import CPDDataset
from task.Task import Task

import inspect

class AlgorithmExecutionTask(Task):
    def __init__(self, function):
        self._function = function

    def validate_task(self) -> None:
        # Check number of args
        full_arg_spec = inspect.getfullargspec(self._function)
        if len(full_arg_spec.args) != 1:
            # Wrong number of arguments
            name_gen = (attr[1] for attr in inspect.getmembers(self._function) if attr[0] == "__name__")
            raise InputValidationException("The number of arguments for the algorithm task '{0}' is {1} but should be "
                                           "1: (signal)"
                                           .format(next(name_gen, ''), len(full_arg_spec.args)))

    def validate_input(self, *args) -> None:
        pass

    def execute(self, data: ndarray) -> tuple[Iterable, Iterable]:
        alg_res_index, alg_res_scores = self._function(data)
        return alg_res_index, alg_res_scores

    def get_task_name(self) -> str:
        return "a:" + self._function.__name__

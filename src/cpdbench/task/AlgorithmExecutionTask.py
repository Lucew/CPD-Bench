from collections.abc import Iterable

from numpy import ndarray

from cpdbench.exception.ValidationException import InputValidationException, AlgorithmValidationException
from cpdbench.task.Task import Task

import inspect

from cpdbench.utils.Utils import get_name_of_function


class AlgorithmExecutionTask(Task):
    def __init__(self, function, counter, param_dict=None):
        super().__init__(function, counter, param_dict)

    def validate_task(self) -> None:
        # Check number of args
        full_arg_spec = inspect.getfullargspec(self._function)
        if len(full_arg_spec.args) != 1:
            # Wrong number of arguments
            function_name = get_name_of_function(self._function)
            raise InputValidationException(f"The number of arguments for the algorithm task '{function_name}' "
                                           f"is {len(full_arg_spec.args)} but should be "
                                           "1: (signal)")

    def validate_input(self, data: ndarray) -> tuple[Iterable, Iterable]:
        try:
            alg_res_index, alg_res_scores = self._function(data)
        except Exception as e:
            raise AlgorithmValidationException(f"The validation of {get_name_of_function(self._function)} failed.") \
                from e
        else:
            return alg_res_index, alg_res_scores

    def execute(self, data: ndarray) -> tuple[Iterable, Iterable]:
        alg_res_index, alg_res_scores = self._function(data)
        return alg_res_index, alg_res_scores

    def get_task_name(self) -> str:
        return f"algorithm:{self._task_name}"

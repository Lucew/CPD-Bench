import inspect
from collections.abc import Iterable

from cpdbench.exception.ValidationException import InputValidationException, MetricValidationException
from cpdbench.task.Task import Task
from cpdbench.utils.Utils import get_name_of_function


class MetricExecutionTask(Task):
    def __init__(self, function, counter, param_dict=None):
        super().__init__(function, counter, param_dict)

    def execute(self, indexes: Iterable, scores: Iterable, ground_truths: Iterable) -> float:
        return self._function(indexes, scores, ground_truths)

    def validate_task(self) -> None:
        # Check number of args
        full_arg_spec = inspect.getfullargspec(self._function)
        if len(full_arg_spec.args) != 3:
            # Wrong number of arguments
            function_name = get_name_of_function(self._function)
            raise InputValidationException("The number of arguments for the metric task '{0}' is {1} but should be "
                                           "3: (indexes, scores, ground_truth)"
                                           .format(function_name, len(full_arg_spec.args)))

    def validate_input(self, indexes: Iterable, scores: Iterable, ground_truths: Iterable) -> float:
        try:
            res = self._function(indexes, scores, ground_truths)
        except Exception as e:
            raise MetricValidationException(f"The validation of {get_name_of_function(self._function)} failed.") \
                from e
        else:
            return res

    def get_task_name(self) -> str:
        return f"metric:{self._task_name}"

import inspect
from collections.abc import Iterable

from exception.InputValidationException import InputValidationException
from task.Task import Task


class MetricExecutionTask(Task):
    def __init__(self, function):
        self._function = function

    def execute(self, indexes: Iterable, scores: Iterable, ground_truths: Iterable) -> float:
        return self._function(indexes, scores, ground_truths)

    def validate_task(self) -> None:
        # Check number of args
        full_arg_spec = inspect.getfullargspec(self._function)
        if len(full_arg_spec.args) != 3:
            # Wrong number of arguments
            name_gen = (attr[1] for attr in inspect.getmembers(self._function) if attr[0] == "__name__")
            raise InputValidationException("The number of arguments for the metric task '{0}' is {1} but should be "
                                           "3: (indexes, scores, ground_truth)"
                                           .format(next(name_gen, ''), len(full_arg_spec.args)))

    def validate_input(self, *args) -> None:
        pass

    def get_task_name(self) -> str:
        return "m:" + self._function.__name__

from collections.abc import Iterable

from task.Task import Task


class MetricExecutionTask(Task):
    def __init__(self, function):
        self._function = function

    def execute(self, indexes: Iterable, scores: Iterable, ground_truths: Iterable) -> float:
        return self._function(indexes, scores, ground_truths)

    def validate_task(self) -> None:
        pass

    def validate_input(self, *args) -> None:
        pass
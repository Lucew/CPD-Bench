from typing import Callable

from cpdbench.task.AlgorithmExecutionTask import AlgorithmExecutionTask
from cpdbench.task.DatasetFetchTask import DatasetFetchTask
from cpdbench.task.MetricExecutionTask import MetricExecutionTask
from cpdbench.task.Task import TaskType, Task


class TaskFactory:
    """Abstract factory for creating task objects"""

    @staticmethod
    def create_task(function: Callable, task_type: TaskType) -> Task:
        """Creates a correct task object based on the given task type.
        :param function: the function to be executed as task
        :param task_type: the type of the task to be created
        :return: the constructed task object
        """
        if task_type == TaskType.DATASET_FETCH:
            return DatasetFetchTask(function)
        elif task_type == TaskType.ALGORITHM_EXECUTION:
            return AlgorithmExecutionTask(function)
        elif task_type == TaskType.METRIC_EXECUTION:
            return MetricExecutionTask(function)

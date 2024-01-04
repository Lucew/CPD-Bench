from typing import Callable

from cpdbench.task.AlgorithmExecutionTask import AlgorithmExecutionTask
from cpdbench.task.DatasetFetchTask import DatasetFetchTask
from cpdbench.task.MetricExecutionTask import MetricExecutionTask
from cpdbench.task.Task import TaskType


class TaskFactory:

    @staticmethod
    def create_task(function: Callable, task_type: TaskType):
        if task_type == TaskType.DATASET_FETCH:
            return DatasetFetchTask(function)
        elif task_type == TaskType.ALGORITHM_EXECUTION:
            return AlgorithmExecutionTask(function)
        elif task_type == TaskType.METRIC_EXECUTION:
            return MetricExecutionTask(function)

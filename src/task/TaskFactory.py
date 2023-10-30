from typing import Callable

from task.AlgorithmExecutionTask import AlgorithmExecutionTask
from task.DatasetFetchTask import DatasetFetchTask
from task.MetricExecutionTask import MetricExecutionTask
from task.Task import TaskType


class TaskFactory:

    @staticmethod
    def create_task(function: Callable, task_type: TaskType):
        if task_type == TaskType.DATASET_FETCH:
            return DatasetFetchTask(function)
        elif task_type == TaskType.ALGORITHM_EXECUTION:
            return AlgorithmExecutionTask(function)
        elif task_type == TaskType.METRIC_EXECUTION:
            return MetricExecutionTask(function)

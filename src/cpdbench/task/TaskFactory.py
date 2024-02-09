from typing import Callable
import inspect

from cpdbench.exception.UserParameterDoesNotExistException import UserParameterDoesNotExistException
from cpdbench.task.AlgorithmExecutionTask import AlgorithmExecutionTask
from cpdbench.task.DatasetFetchTask import DatasetFetchTask
from cpdbench.task.MetricExecutionTask import MetricExecutionTask
from cpdbench.task.Task import TaskType, Task
import cpdbench.utils.BenchConfig as BenchConfig
from cpdbench.utils.Utils import get_name_of_function
from functools import partial


def _generate_task_object(function: Callable, task_type: TaskType):
    if task_type == TaskType.DATASET_FETCH:
        return DatasetFetchTask(function)
    elif task_type == TaskType.ALGORITHM_EXECUTION:
        return AlgorithmExecutionTask(function)
    elif task_type == TaskType.METRIC_EXECUTION:
        return MetricExecutionTask(function)


class TaskFactory:
    """Abstract factory for creating task objects"""

    def __init__(self):
        self._user_config = BenchConfig.get_user_config()

    def create_tasks(self, function: Callable, task_type: TaskType) -> list[Task]:
        """Creates a correct task object based on the given task type.
        :param function: the function to be executed as task
        :param task_type: the type of the task to be created
        :return: the constructed task object
        """
        user_params = [param.name for param in inspect.signature(function).parameters.values() if param.kind ==
                       param.KEYWORD_ONLY]
        if user_params is None or len(user_params) == 0:
            return [_generate_task_object(function, task_type)]
        param_values = [{} for _ in range(self._user_config.get_number_of_executions(task_type))]
        for param in user_params:
            try:
                vals = self._user_config.get_user_param(param, task_type)
            except Exception as e:
                if str(e) == "Parameter not found":
                    raise UserParameterDoesNotExistException(param, get_name_of_function(function))
                else:
                    raise e
            else:
                for i in range(len(param_values)):
                    if len(param_values) == len(vals):
                        param_values[i].update({param: vals[i]})  # execution param
                    else:
                        param_values[i].update({param: vals[0]})  # global param

        tasks = []
        for param_dict in param_values:
            function_with_params = partial(function, **param_dict)
            tasks.append(_generate_task_object(function_with_params, task_type))
        return tasks

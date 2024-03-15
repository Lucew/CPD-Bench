from typing import Callable
import inspect

from cpdbench.exception.UserParameterDoesNotExistException import UserParameterDoesNotExistException
from cpdbench.task.AlgorithmExecutionTask import AlgorithmExecutionTask
from cpdbench.task.DatasetFetchTask import DatasetFetchTask
from cpdbench.task.MetricExecutionTask import MetricExecutionTask
from cpdbench.task.Task import TaskType, Task
import cpdbench.utils.BenchConfig as BenchConfig
from cpdbench.utils import Logger
from cpdbench.utils.Utils import get_name_of_function
from functools import partial


class TaskFactory:
    """Abstract factory for creating task objects"""

    def __init__(self):
        self._user_config = BenchConfig.get_user_config()
        self._logger = Logger.get_application_logger()
        self._task_counter = 0

    def create_task_from_function(self, function: Callable, task_type: TaskType) -> Task:
        """Creates one task for an unparametrized function.
        :param function: the function to be executed as task
        :param task_type: the type of the task to be created
        :return: the constructed task object
        """
        return self._generate_task_object(function, {}, task_type)

    def create_tasks_with_parameters(self, function: Callable, task_type: TaskType) -> list[Task]:
        """Creates correct task objects based on the given task type and the needed parameters defined in the user
        config. Because of this, this method can potentially output multiple tasks with the same function
        but different parameters.
        :param function: the function to be executed as task
        :param task_type: the type of the task to be created
        :return: the constructed task objects
        """
        all_params = [param.name for param in inspect.signature(function).parameters.values() if param.kind ==
                      param.KEYWORD_ONLY]
        try:
            global_params = [param for param in all_params if self._user_config.check_if_global_param(param)]
        except Exception as e:
            if "Parameter not found" in str(e):
                raise UserParameterDoesNotExistException(str(e).split()[-1], get_name_of_function(function))

        if all_params is None or len(all_params) == 0:
            # Easy case: no parameter
            task = self._generate_task_object(function,{}, task_type)
            self._logger.info(f"Created task {task.get_task_name()}")
            self._task_counter += 1
            return [task]
        global_params.sort()
        all_params.sort()
        if global_params == all_params:
            # Easy case: only global params
            param_values = [{}]
        else:
            param_values = [{} for _ in range(self._user_config.get_number_of_executions(task_type))]
        if len(param_values) == 0:
            param_values = [{}]

        for param in all_params:
            try:
                vals = self._user_config.get_user_param(param, task_type)
            except Exception as e:
                if str(e) == "Parameter not found":
                    raise UserParameterDoesNotExistException(param, get_name_of_function(function))
                else:
                    raise e
            else:
                for i in range(len(param_values)):
                    if param in global_params:
                        param_values[i].update({param: vals[0]})  # global param
                    else:
                        param_values[i].update({param: vals[i]})  # execution param

        tasks = []
        for param_dict in param_values:
            function_with_params = partial(function, **param_dict)
            task = self._generate_task_object(function_with_params, param_dict, task_type)
            self._task_counter += 1
            self._logger.info(f"Created task {task.get_task_name()} with following parameters: {str(param_dict)}")
            tasks.append(task)
        return tasks

    def _generate_task_object(self, function: Callable, param_dict: dict, task_type: TaskType):
        if task_type == TaskType.DATASET_FETCH:
            return DatasetFetchTask(function, self._task_counter, param_dict)
        elif task_type == TaskType.ALGORITHM_EXECUTION:
            return AlgorithmExecutionTask(function, self._task_counter, param_dict)
        elif task_type == TaskType.METRIC_EXECUTION:
            return MetricExecutionTask(function, self._task_counter, param_dict)

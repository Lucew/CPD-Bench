from abc import ABC, abstractmethod

from cpdbench.exception.ValidationException import ValidationException
from cpdbench.task.Task import TaskType
from cpdbench.task.TaskFactory import TaskFactory
from cpdbench.utils import Utils


class ExecutionController(ABC):

    def __init__(self, logger):
        self._logger = logger

    @abstractmethod
    def execute_run(self, methods: dict) -> any:
        pass

    def _create_tasks(self, methods):
        task_objects = {
            "datasets": [],
            "algorithms": [],
            "metrics": []
        }
        task_factory = TaskFactory()
        for dataset_function in methods["datasets"]:
            self._logger.debug(f"Creating and validating dataset task "
                               f"for {Utils.get_name_of_function(dataset_function)}")
            tasks = task_factory.create_tasks(dataset_function, TaskType.DATASET_FETCH)
            try:
                for task in tasks:
                    task.validate_task() #TODO: Validation + Task-Namen auf Listen anpassen
            except ValidationException as e:
                self._logger.exception(e)
            else:
                self._logger.debug(f'Validating {Utils.get_name_of_function(dataset_function)} has succeeded')
                task_objects["datasets"] += tasks

        for algorithm_function in methods["algorithms"]:
            self._logger.debug(f"Creating and validating algorithm task "
                               f"for {Utils.get_name_of_function(algorithm_function)}")
            tasks = task_factory.create_tasks(algorithm_function, TaskType.ALGORITHM_EXECUTION)
            try:
                for task in tasks:
                    task.validate_task()
            except ValidationException as e:
                self._logger.exception(e)
            else:
                self._logger.debug(f'Validating {Utils.get_name_of_function(algorithm_function)} has succeeded')
                task_objects["algorithms"] += tasks

        for metric_function in methods["metrics"]:
            self._logger.debug(f"Creating and validating metric task "
                               f"for {Utils.get_name_of_function(metric_function)}")
            tasks = task_factory.create_tasks(metric_function, TaskType.METRIC_EXECUTION)
            try:
                for task in tasks:
                    task.validate_task()
            except ValidationException as e:
                self._logger.exception(e)
            else:
                self._logger.debug(f'Validating {Utils.get_name_of_function(metric_function)} has succeeded')
                task_objects["metrics"] += tasks
        return task_objects

from abc import ABC, abstractmethod

from cpdbench.control.CPDResult import CPDResult
from cpdbench.exception.UserParameterDoesNotExistException import UserParameterDoesNotExistException
from cpdbench.exception.ValidationException import ValidationException
from cpdbench.task.Task import TaskType
from cpdbench.task.TaskFactory import TaskFactory
from cpdbench.utils import Utils


class ExecutionController(ABC):
    """Abstract base class for testbench run configurations.
    Each subclass has to give an execute_run() implementation with the actual run logic.
    """

    def __init__(self, logger):
        self._logger = logger

    @abstractmethod
    def execute_run(self, methods: dict) -> CPDResult:
        """Executes the run implemented by this class.
        :param methods: dictionary with all given input functions, grouped by function type.
        :return: A result object which can be handed to the user
        """
        pass

    def _create_tasks(self, methods: dict) -> dict:
        """Creates task objects from the entered function handles
        :param methods: A dictionary containing the function handles, grouped by function type
        :return: A dictionary of task objects, which were converted from the given handles
        """
        task_objects = {
            "datasets": [],
            "algorithms": [],
            "metrics": []
        }
        task_factory = TaskFactory()
        for dataset_function in methods["datasets"]:
            self._logger.debug(f"Creating and validating dataset task "
                               f"for {Utils.get_name_of_function(dataset_function)}")
            try:
                tasks = task_factory.create_tasks_with_parameters(dataset_function, TaskType.DATASET_FETCH)
            except UserParameterDoesNotExistException as e:
                self._logger.exception(e)
                self._logger.debug(f"Creating {Utils.get_name_of_function(dataset_function)} has failed")
                continue
            try:
                for task in tasks:
                    task.validate_task()
            except ValidationException as e:
                self._logger.exception(e)
            else:
                self._logger.debug(f'Validating and creating {Utils.get_name_of_function(dataset_function)} has succeeded')
                task_objects["datasets"] += tasks

        for algorithm_function in methods["algorithms"]:
            self._logger.debug(f"Creating and validating algorithm task "
                               f"for {Utils.get_name_of_function(algorithm_function)}")
            try:
                tasks = task_factory.create_tasks_with_parameters(algorithm_function, TaskType.ALGORITHM_EXECUTION)
            except UserParameterDoesNotExistException as e:
                self._logger.exception(e)
                self._logger.debug(f"Creating {Utils.get_name_of_function(algorithm_function)} has failed")
                continue
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
            try:
                tasks = task_factory.create_tasks_with_parameters(metric_function, TaskType.METRIC_EXECUTION)
            except UserParameterDoesNotExistException as e:
                self._logger.exception(e)
                self._logger.debug(f"Creating {Utils.get_name_of_function(metric_function)} has failed")
                continue
            try:
                for task in tasks:
                    task.validate_task()
            except ValidationException as e:
                self._logger.exception(e)
            else:
                self._logger.debug(f'Validating {Utils.get_name_of_function(metric_function)} has succeeded')
                task_objects["metrics"] += tasks
        return task_objects

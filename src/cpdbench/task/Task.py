from abc import ABC, abstractmethod
from enum import Enum
import functools
import uuid


class TaskType(Enum):
    """Enum of pre-defined task types needed for the CPDBench"""
    DATASET_FETCH = 1
    ALGORITHM_EXECUTION = 2
    METRIC_EXECUTION = 3


class Task(ABC):
    """Abstract class for a Task object which is a work package to be executed by the framework.
    A task has a name, can be validated, and executed, and can have some parameters.
    """

    def __init__(self, function, counter=0, param_dict=None):
        """General constructor for all task objects.
        :param function: The function handle to be executed as task content
        :param counter: A number which is appended to the task name. Useful if multiple tasks with the same name exist.
        :param param_dict: An optional parameter dictionary for the task
        """
        self._function = function
        if isinstance(function, functools.partial):
            self._function_name = function.func.__name__
        else:
            self._function_name = function.__name__
        self._task_name = self._function_name + ":" + str(counter)
        self._param_dict = param_dict

    @abstractmethod
    def execute(self, *args) -> any:
        """Executes the task. Can take an arbitrary number of arguments and can produce any result."""
        pass

    @abstractmethod
    def validate_task(self) -> None:
        """Validates the task statically by checking task details before running it.
        Throws an exception if the validation fails.
        """
        pass

    @abstractmethod
    def validate_input(self, *args) -> any:
        """Validates the task in combination with some input arguments.
        Throws an exception if the validation fails.
        """
        pass

    @abstractmethod
    def get_task_name(self) -> str:
        """Returns a descriptive name for the task.
        :return: task name as string
        """
        pass

    def get_param_dict(self) -> dict:
        """Returns the parameters this task contains.
        :return: the parameters as dictionary
        """
        return self._param_dict

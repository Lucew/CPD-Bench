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
    """Abstract class for a Task object which defines a list of operations.
    This task has a name, can be validated, and executed.
    """

    def __init__(self, function, counter=0, param_dict=None):
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
        # Validiert wird:
        # - Anzahl Params
        # (optional wenn Typing): Typen, Rückgabetyp //TODO
        pass

    @abstractmethod
    def validate_input(self, *args) -> any:
        """Validates the task in combination with some input arguments.
        Throws an exception if the validation fails.
        """
        # Validiert wird:
        # - Fehler, wenn Algorithmus aufgerufen wird?
        # - Fehler, wenn Metrik aufgerufen wird?
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

from abc import ABC, abstractmethod
from enum import Enum


class TaskType(Enum):
    DATASET_FETCH = 1
    ALGORITHM_EXECUTION = 2
    METRIC_EXECUTION = 3


class Task(ABC):

    @abstractmethod
    def execute(self, *args) -> any:
        pass

    @abstractmethod
    def validate_task(self) -> None:
        pass

    @abstractmethod
    def validate_input(self, *args) -> None:
        pass

    @abstractmethod
    def get_task_name(self) -> str:
        pass

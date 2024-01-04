from abc import ABC, abstractmethod


class ExecutionController(ABC):

    @abstractmethod
    def execute_run(self, methods: dict) -> any:
        pass

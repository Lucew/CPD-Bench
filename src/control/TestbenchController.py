from control.ExecutionController import ExecutionController
from control.TestrunController import TestrunController


class TestbenchController:
    def execute_testrun(self, datasets, algorithms, metrics):
        controller = TestrunController()
        function_map = {
            "datasets": datasets,
            "algorithms": algorithms,
            "metrics": metrics
        }
        controller.execute_run(function_map)


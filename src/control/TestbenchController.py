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
        result = controller.execute_run(function_map)
        print(result.get_result_as_dict())


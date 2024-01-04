import json
import logging

import numpy as np

from cpdbench.control.TestrunController import TestrunController


class ExtendedEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(ExtendedEncoder, self).default(obj)


class TestbenchController:
    def execute_testrun(self, datasets, algorithms, metrics):
        controller = TestrunController()
        function_map = {
            "datasets": datasets,
            "algorithms": algorithms,
            "metrics": metrics
        }
        result = controller.execute_run(function_map)
        self.output_result(result.get_result_as_dict())
        logging.shutdown()

    def output_result(self, result_dict: dict) -> None:
        json_string = json.dumps(result_dict, indent=4, cls=ExtendedEncoder)

        # file output
        with open('cpdbench-result.json', 'w') as file:
            file.write(json_string)

        # console output
        print(json_string)

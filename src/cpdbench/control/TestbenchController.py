import json
import logging
from enum import Enum

import numpy as np

from cpdbench.control.TestrunController import TestrunController
from cpdbench.control.ValidationRunController import ValidationRunController
from cpdbench.utils import BenchConfig, Logger


class TestrunType(Enum):
    """Types of predefined run configurations"""
    NORMAL_RUN = 1,
    VALIDATION_RUN = 2


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
    """Main controller for starting different types of test runs.
    This is the basic class which is executed after initialization of the framework.
    This controller then calls an ExecutionController implementation, which contains
    the actual logic of a run.
    """

    def execute_testrun(self, runtype: TestrunType, datasets: list, algorithms: list, metrics: list) -> None:
        """Prepares and runs the required testrun
        :param runtype: Type of testrun to run
        :param datasets: list of dataset functions
        :param algorithms: list of algorithm functions
        :param metrics: list of metric functions
        """
        if runtype == TestrunType.NORMAL_RUN:
            controller = TestrunController()
        else:
            controller = ValidationRunController()

        function_map = {
            "datasets": datasets,
            "algorithms": algorithms,
            "metrics": metrics
        }
        try:
            result = controller.execute_run(function_map)
        except Exception as e:
            Logger.get_application_logger().critical("Unexpected error occurred during bench run. CPDBench was aborted.")
            Logger.get_application_logger().critical(e)
            logging.shutdown()
        else:
            self._output_result(result.get_result_as_dict())
            Logger.get_application_logger().info("CDPBench has finished. The following config has been used:")
            Logger.get_application_logger().info(BenchConfig.get_complete_config())
            logging.shutdown()

    def _output_result(self, result_dict: dict) -> None:
        """Outputs a result dict correctly on console and in a file
        :param result_dict: the to be printed dict
        """
        json_string = json.dumps(result_dict, indent=4, cls=ExtendedEncoder)

        # file output
        with open(BenchConfig.result_file_name, 'w') as file:
            file.write(json_string)

        # console output
        print(json_string)

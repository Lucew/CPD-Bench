from control.TestbenchController import TestbenchController
from utils import Logger
from utils import Utils
from utils import BenchConfig


class CPDBench:

    def __init__(self):
        self._datasets = []
        self._algorithms = []
        self._metrics = []
        self._logger = None

    def start(self) -> None:
        BenchConfig.load_config()
        self._logger = Logger.get_application_logger()
        self._logger.debug('CPDBench object created')
        self._logger.info("Starting CPDBench")
        self._logger.info(f"Got {len(self._datasets)} datasets, {len(self._algorithms)} algorithms and "
                          f"{len(self._metrics)} metrics")
        bench = TestbenchController()
        bench.execute_testrun(self._datasets, self._algorithms, self._metrics)

    def dataset(self, function):
        #self._logger.debug(f'Got a dataset function: {Utils.get_name_of_function(function)}')
        self._datasets.append(function)
        return function

    def algorithm(self, function):
        #self._logger.debug(f'Got an algorithm function: {Utils.get_name_of_function(function)}')
        self._algorithms.append(function)
        return function

    def metric(self, function):
        #self._logger.debug(f'Got a metric function: {Utils.get_name_of_function(function)}')
        self._metrics.append(function)
        return function


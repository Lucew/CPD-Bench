from cpdbench.control.TestbenchController import TestbenchController
from cpdbench.utils import Logger, BenchConfig


class CPDBench:
    """Main class for accessing the CDPBench functions"""

    def __init__(self):
        self._datasets = []
        self._algorithms = []
        self._metrics = []
        self._logger = None

    def start(self, config_file: str = 'config.yml') -> None:
        """Start the execution of the CDPBench environment
        :param config_file: Path to the CDPBench configuration file; defaults to 'config.yml'
        """
        BenchConfig.load_config(config_file)
        self._logger = Logger.get_application_logger()
        self._logger.debug('CPDBench object created')
        self._logger.info("Starting CPDBench")
        self._logger.info(f"Got {len(self._datasets)} datasets, {len(self._algorithms)} algorithms and "
                          f"{len(self._metrics)} metrics")
        bench = TestbenchController()
        bench.execute_testrun(self._datasets, self._algorithms, self._metrics)

    def dataset(self, function):
        """Decorator for dataset functions which create CPDDataset objects"""

        # self._logger.debug(f'Got a dataset function: {Utils.get_name_of_function(function)}')
        self._datasets.append(function)
        return function

    def algorithm(self, function):
        """Decorator for algorithm functions which execute changepoint algorithms"""

        # self._logger.debug(f'Got an algorithm function: {Utils.get_name_of_function(function)}')
        self._algorithms.append(function)
        return function

    def metric(self, function):
        """Decorator for metric functions which evaluate changepoint results"""

        # self._logger.debug(f'Got a metric function: {Utils.get_name_of_function(function)}')
        self._metrics.append(function)
        return function

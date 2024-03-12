from cpdbench.control.CPDDatasetResult import CPDDatasetResult
import datetime

from cpdbench.control.CPDResult import CPDResult


class CPDFullResult(CPDResult):
    """Container for a complete run result with all datasets"""

    def __init__(self, datasets: list[str], algorithms: list[str], metrics: list[str]):
        """Construct a CPDFullResult object with basic metadata
        :param datasets: list of all dataset names as strings
        :param algorithms: list of all used changepoint algorithms as strings
        :param metrics: list of all metrics as strings
        """
        self._result = {}
        self._created = datetime.datetime.now()
        self._last_updated = self._created
        self._datasets = datasets
        self._algorithms = algorithms
        self._metrics = metrics
        self._errors = []
        self._parameters = {}
        self._runtimes = {}

    def add_dataset_result(self, dataset_result: CPDDatasetResult) -> None:
        """Adds a calculated dataset result to the FullResult
        :param dataset_result: the dataset result to add
        """
        self._result = self._result | dataset_result.get_result_as_dict()
        self._errors += dataset_result.get_errors_as_list()
        self._last_updated = datetime.datetime.now()
        self._parameters = self._parameters | dataset_result.get_parameters()
        self._runtimes = self._runtimes | dataset_result.get_runtimes()

    def get_result_as_dict(self) -> dict:
        """Returns the complete result with all dataset results and metadata as python dict
        :return: the result as python dict
        """
        return {
            "datasets": self._datasets,
            "algorithms": self._algorithms,
            "metrics": self._metrics,
            "created": self._created.strftime("%m/%d/%Y, %H:%M:%S"),
            "last_updated": self._last_updated.strftime("%m/%d/%Y, %H:%M:%S"),
            "parameters": self._parameters,
            "results": self._result,
            "runtimes": self._runtimes,
            "errors": self._errors
        }

import datetime
import traceback

from cpdbench.control.CPDResult import CPDResult


class CPDValidationResult(CPDResult):
    """Container for a validation run result."""

    def __init__(self, errors: list, datasets: list[str], algorithms: list[str], metrics: list[str]):
        """Construct a validation result object
        :param errors: list of occurred errors during validation
        :param datasets: list of all dataset names as strings
        :param algorithms: list of all used changepoint algorithms as strings
        :param metrics: list of all metrics as strings
        """
        self._errors = []
        for error in errors:
            self._errors.append(''.join(traceback.format_exception(None, error, error.__traceback__)))
        self._created = datetime.datetime.now()
        self._last_updated = self._created
        self._datasets = datasets
        self._algorithms = algorithms
        self._metrics = metrics

    def get_result_as_dict(self) -> dict:
        """Return the complete result with all dataset results and metadata as python dict
        :return: the result as python dict
        """
        return {
            "datasets": self._datasets,
            "algorithms": self._algorithms,
            "metrics": self._metrics,
            "created": self._created.strftime("%m/%d/%Y, %H:%M:%S"),
            "last_updated": self._last_updated.strftime("%m/%d/%Y, %H:%M:%S"),
            "errors": self._errors
        }

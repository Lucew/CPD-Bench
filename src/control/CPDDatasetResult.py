from enum import Enum

from exception.ResultSetInconsistentException import ResultSetInconsistentException
import traceback


class ErrorType(str, Enum):
    DATASET_ERROR = "DATASET_ERROR"
    ALGORITHM_ERROR = "ALGORITHM_ERROR"
    METRIC_ERROR = "METRIC_ERROR"


class CPDDatasetResult:
    def __init__(self, dataset, algorithms, metrics):
        self._dataset = dataset.get_task_name()
        self._algorithms = [a.get_task_name() for a in algorithms]
        self._metrics = [m.get_task_name() for m in metrics]

        self._indexes = {}
        # { "1" : { "alg1": [14, 124, 1] } }
        self._scores = {}
        self._metric_scores = {}
        # { "1" : { "alg1": { "metr1": 212 } } }
        for a in self._algorithms:
            self._metric_scores[a] = {}

        self._errors = []

    def add_algorithm_result(self, indexes, scores, algorithm):
        if algorithm not in self._algorithms:
            raise ResultSetInconsistentException()
        self._indexes[algorithm] = indexes
        self._scores[algorithm] = scores

    def add_metric_score(self, metric_score, algorithm, metric):
        if (algorithm not in self._algorithms
                or metric not in self._metrics):
            raise ResultSetInconsistentException()
        self._metric_scores[algorithm][metric] = metric_score

    def add_error(self, exception, error_type, algorithm=None, metric=None):
        self._errors.append((type(exception).__name__, ''.join(traceback.format_exception(None, exception,
                                                                                          exception.__traceback__)),
                             error_type, algorithm, metric))

    def get_result_as_dict(self):
        return {
            self._dataset: {
                "indexes": self._indexes,
                "scores": self._scores,
                "metric_scores": self._metric_scores
            }
        }

    def get_errors_as_list(self):
        return [
            {
                "dataset": self._dataset,
                "error_type": error[2],
                "algorithm": error[3],
                "metric": error[4],
                "exception_type": error[0],
                "trace_back": error[1]
            }
            for error in self._errors
        ]

    def get_algorithms(self):
        return self._algorithms

    def get_metrics(self):
        return self._metrics

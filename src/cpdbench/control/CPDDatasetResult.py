from enum import Enum

from cpdbench.exception.ResultSetInconsistentException import ResultSetInconsistentException
import traceback

from cpdbench.task.Task import Task


class ErrorType(str, Enum):
    """Enum for all error types which can occur during the CPDBench execution"""
    DATASET_ERROR = "DATASET_ERROR"
    ALGORITHM_ERROR = "ALGORITHM_ERROR"
    METRIC_ERROR = "METRIC_ERROR"


class CPDDatasetResult:
    """Container for all results of one single dataset including algorithm and metric results"""

    def __init__(self, dataset: Task, algorithms: list[Task], metrics: list[Task]):
        """Constructs a dataset result with the basic attributes
        :param dataset: task which created the dataset
        :param algorithms: list of all algorithm tasks
        :param metrics: list of all metric tasks
        """

        self._dataset = dataset.get_task_name()
        self._algorithms = [a.get_task_name() for a in algorithms]
        self._metrics = [m.get_task_name() for m in metrics]

        self._indexes = {}
        # { "1" : { "alg1": [14, 124, 1] } }
        self._scores = {}
        self._metric_scores = {}
        # { "1" : { "alg1": { "metr1": 212 } } }

        self._errors = []
        self._parameters = ({self._dataset: dataset.get_param_dict()}
                            | {task.get_task_name(): task.get_param_dict() for task in algorithms}
                            | {task.get_task_name(): task.get_param_dict() for task in metrics})

        self._dataset_runtime = -1
        self._algorithm_runtimes = {}
        for a in self._algorithms:
            self._metric_scores[a] = {}

    def add_dataset_runtime(self, runtime: float) -> None:
        self._dataset_runtime = runtime

    def add_algorithm_result(self, indexes: list[int], scores: list[float], algorithm: str, runtime: float) -> None:
        """Adds an algorithm result with indexes and confidence scores to the result container.
        :param indexes: list of calculated changepoint indexes
        :param scores: list of calculated confidence scores respective to the indexes list
        :param algorithm: name of the calculated algorithm
        :param runtime: runtime of the algorithm execution in seconds
        """

        if algorithm not in self._algorithms:
            raise ResultSetInconsistentException()
        self._indexes[algorithm] = indexes
        self._scores[algorithm] = scores
        self._algorithm_runtimes[algorithm] = {}
        self._algorithm_runtimes[algorithm]["runtime"] = runtime

    def add_metric_score(self, metric_score: float, algorithm: str, metric: str, runtime: float) -> None:
        """Adds a metric result of an algorithm/dataset to the result container.
        :param metric_score: calculated metric score as float
        :param algorithm: name of the calculated algorithm
        :param metric: name of the used metric
        :param runtime: runtime of the metric execution in seconds
        """

        if (algorithm not in self._algorithms
                or metric not in self._metrics):
            raise ResultSetInconsistentException()
        self._metric_scores[algorithm][metric] = metric_score
        self._algorithm_runtimes[algorithm][metric] = runtime

    def add_error(self, exception: Exception, error_type: ErrorType, algorithm: str = None, metric: str = None) -> None:
        """Adds a thrown error to the result container.
        :param exception: the thrown exception object
        :param error_type: the error type of the thrown exception
        :param algorithm: name of the algorithm where the exception occurred if applicable
        :param metric: name of the metric where the exception occurred if applicable
        """

        self._errors.append((type(exception).__name__, ''.join(traceback.format_exception(None, exception,
                                                                                          exception.__traceback__)),
                             error_type, algorithm, metric))

    def get_result_as_dict(self) -> dict:
        """Returns the result container formatted as dictionary.
        :returns: the complete results with indexes, scores and metric scores of one dataset as dict
        """

        return {
            self._dataset: {
                "indexes": self._indexes,
                "scores": self._scores,
                "metric_scores": self._metric_scores
            }
        }

    def get_errors_as_list(self) -> list:
        """Returns the list of errors occurred around the dataset.
        :returns: all errors of the dataset as python list
        """

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

    def get_parameters(self) -> dict:
        return self._parameters

    def get_runtimes(self) -> dict:
        result_dict = {
            self._dataset: self._algorithm_runtimes | {
                "runtime": self._dataset_runtime,
            }
        }
        return result_dict

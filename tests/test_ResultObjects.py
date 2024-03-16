import unittest

from cpdbench.control.CPDDatasetResult import CPDDatasetResult, ErrorType
from cpdbench.dataset.CPDNdarrayDataset import CPDNdarrayDataset
from cpdbench.exception.ResultSetInconsistentException import ResultSetInconsistentException
from cpdbench.task.Task import TaskType
from cpdbench.task.TaskFactory import TaskFactory
import numpy as np


def _generate_dummy_dataset():
    return CPDNdarrayDataset(np.zeros(3), [1])


def _dummy_algorithm_task(dataset):
    return [1], [1]


def _dummy_metric_task(indexes, confidences, gts):
    return 1.0


class TestResultObjects(unittest.TestCase):

    def setUp(self):
        self._task_factory = TaskFactory()
        self._dataset_dummy_task = self._task_factory.create_task_from_function(
            _generate_dummy_dataset, TaskType.DATASET_FETCH)
        self._algorithm_dummy_task = self._task_factory.create_task_from_function(
            _dummy_algorithm_task, TaskType.ALGORITHM_EXECUTION
        )
        self._metric_dummy_task = self._task_factory.create_task_from_function(
            _dummy_metric_task, TaskType.METRIC_EXECUTION
        )

    def test_empty_dataset_result(self):
        # arrange
        dataset_result = CPDDatasetResult(self._dataset_dummy_task, [], [])

        # act
        parameters_dict = dataset_result.get_parameters()
        runtimes_dict = dataset_result.get_runtimes()
        result_dict = dataset_result.get_result_as_dict()
        error_list = dataset_result.get_errors_as_list()

        # assert
        self.assertDictEqual(parameters_dict, {
            "dataset:_generate_dummy_dataset:0": {}
        })
        self.assertDictEqual(runtimes_dict, {
            "dataset:_generate_dummy_dataset:0": {}
        })
        self.assertDictEqual(result_dict, {
            "dataset:_generate_dummy_dataset:0": {
                "indexes": {},
                "metric_scores": {},
                "scores": {}
            }
        })
        self.assertListEqual(error_list, [])

    def test_dataset_result_add_dataset_runtime(self):
        # arrange
        dataset_result = CPDDatasetResult(self._dataset_dummy_task, [], [])

        # act
        dataset_result.add_dataset_runtime(42.42)
        dataset_result.add_dataset_runtime(5)
        result = dataset_result.get_runtimes()

        # assert
        self.assertDictEqual(result, {
            "dataset:_generate_dummy_dataset:0": {
                "runtime": 42.42
            }
        })

    def test_dataset_result_add_algorithm_result_throw_exception_when_algorithm_unknown(self):
        # arrange
        dataset_result = CPDDatasetResult(self._dataset_dummy_task, [], [])

        # act / assert
        self.assertRaises(ResultSetInconsistentException, dataset_result.add_algorithm_result,
                          [3], [1.0], "my_algorithm", 42)

    def test_dataset_result_add_algorithm_result(self):
        # arrange
        dataset_result = CPDDatasetResult(self._dataset_dummy_task,
                                          [self._algorithm_dummy_task], [])

        # act
        dataset_result.add_algorithm_result(
            [131, 313], [1.0, 0.45], "algorithm:_dummy_algorithm_task:0",
            1.56
        )

        # assert
        self.assertDictEqual(dataset_result.get_result_as_dict(), {
            "dataset:_generate_dummy_dataset:0": {
                "indexes": {
                    "algorithm:_dummy_algorithm_task:0": [131, 313]
                },
                "metric_scores": {
                    "algorithm:_dummy_algorithm_task:0": {}
                },
                "scores": {
                    "algorithm:_dummy_algorithm_task:0": [1.0, 0.45]
                }
            }
        })

    def test_dataset_result_add_metric_result_throw_exception_because_algorithm_result_is_missing(self):
        # arrange
        dataset_result = CPDDatasetResult(self._dataset_dummy_task,
                                          [self._algorithm_dummy_task],
                                          [self._metric_dummy_task])

        # act / assert
        self.assertRaises(ResultSetInconsistentException,
                          dataset_result.add_metric_score,
                          0.55, "algorithm:_dummy_algorithm_task:0", "metric:_dummy_metric_task:0", 1.56)

    def test_dataset_result_add_metric_result(self):
        # arrange
        dataset_result = CPDDatasetResult(self._dataset_dummy_task,
                                          [self._algorithm_dummy_task],
                                          [self._metric_dummy_task])
        dataset_result.add_algorithm_result(
            [131, 313], [1.0, 0.45], "algorithm:_dummy_algorithm_task:0",
            1.56
        )

        # act
        dataset_result.add_metric_score(0.55, "algorithm:_dummy_algorithm_task:0",
                                        "metric:_dummy_metric_task:0", 1.56)

        # assert
        self.assertDictEqual(dataset_result.get_result_as_dict(), {
            "dataset:_generate_dummy_dataset:0": {
                "indexes": {
                    "algorithm:_dummy_algorithm_task:0": [131, 313]
                },
                "metric_scores": {
                    "algorithm:_dummy_algorithm_task:0": {
                        "metric:_dummy_metric_task:0": 0.55
                    }
                },
                "scores": {
                    "algorithm:_dummy_algorithm_task:0": [1.0, 0.45]
                }
            }
        })

    def test_dataset_result_add_error(self):
        # arrange
        dataset_result = CPDDatasetResult(self._dataset_dummy_task,
                                          [self._algorithm_dummy_task],
                                          [self._metric_dummy_task])

        # act
        dataset_result.add_error(Exception(), ErrorType.DATASET_ERROR)

        # assert
        errors = dataset_result.get_errors_as_list()
        self.assertEqual(len(errors), 1)
        self.assertDictEqual(errors[0], {
            "dataset": "dataset:_generate_dummy_dataset:0",
            "error_type": ErrorType.DATASET_ERROR,
            "algorithm": None,
            "metric": None,
            "exception_type": "Exception",
            "trace_back": "Exception\n"
        })

    def test_dataset_result_get_errors_empty_list(self):
        # arrange
        dataset_result = CPDDatasetResult(self._dataset_dummy_task,
                                          [self._algorithm_dummy_task],
                                          [self._metric_dummy_task])

        # act
        errors = dataset_result.get_errors_as_list()

        # assert
        self.assertEqual(errors, [])

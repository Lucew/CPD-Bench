import unittest

from cpdbench.control.CPDDatasetResult import CPDDatasetResult
from cpdbench.dataset.CPD2DNdarrayDataset import CPD2DNdarrayDataset
from cpdbench.task.Task import TaskType
from cpdbench.task.TaskFactory import TaskFactory
import numpy as np


def _generate_dummy_dataset():
    return CPD2DNdarrayDataset(np.zeros(3), [1])


class TestResultObjects(unittest.TestCase):

    def setUp(self):
        self._task_factory = TaskFactory()
        self._dataset_dummy_task = self._task_factory.create_task_from_function(
            _generate_dummy_dataset, TaskType.DATASET_FETCH)

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


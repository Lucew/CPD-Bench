import unittest
from unittest.mock import MagicMock

from cpdbench.task.AlgorithmExecutionTask import AlgorithmExecutionTask
from cpdbench.task.DatasetFetchTask import DatasetFetchTask
from cpdbench.task.MetricExecutionTask import MetricExecutionTask
from cpdbench.task.Task import TaskType
from cpdbench.task.TaskFactory import TaskFactory
from cpdbench.utils import BenchConfig
from cpdbench.utils.UserConfig import UserConfig


class TestTaskFactory(unittest.TestCase):

    def setUp(self):
        BenchConfig.get_user_config = MagicMock(return_value=UserConfig(
            {
                "test": 435,
                "dataset-executions": [
                    {"abc": 35, "x": 675},
                    {"abc": 3532, "x": 3}
                ]
            }
        ))
        self._task_factory = TaskFactory()

    def test_create_task_from_function(self):
        # arrange
        def test_task():
            return 1
        task = MetricExecutionTask(test_task, 0, {})

        # act
        result = self._task_factory.create_task_from_function(test_task, TaskType.METRIC_EXECUTION)

        # assert
        self.assertEqual(result.get_task_name(), task.get_task_name())
        self.assertEqual(result.get_param_dict(), task.get_param_dict())
        self.assertEqual(type(result), type(task))

    def test_create_task_with_parameters_multiple(self):
        # arrange
        def test_task(*, test, abc):
            return 1

        task1 = DatasetFetchTask(test_task, 0, {
            "test": 435, "abc": 35
        })
        task2 = DatasetFetchTask(test_task, 1, {
            "test": 435, "abc": 3532
        })

        # act
        result = self._task_factory.create_tasks_with_parameters(test_task, TaskType.DATASET_FETCH)

        # assert
        self.assertEqual(len(result), 2)

        self.assertEqual(result[0].get_task_name(), task1.get_task_name())
        self.assertEqual(result[1].get_task_name(), task2.get_task_name())

        self.assertEqual(result[0].get_param_dict(), task1.get_param_dict())
        self.assertEqual(result[1].get_param_dict(), task2.get_param_dict())

        self.assertEqual(type(result[0]), type(task1))

    def test_create_task_with_parameters_one_task_only(self):
        # arrange
        def test_task(*, test):
            return 1

        task1 = DatasetFetchTask(test_task, 0, {
            "test": 435
        })

        # act
        result = self._task_factory.create_tasks_with_parameters(test_task, TaskType.DATASET_FETCH)

        # assert
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].get_task_name(), task1.get_task_name())
        self.assertEqual(result[0].get_param_dict(), task1.get_param_dict())
        self.assertEqual(type(result[0]), type(task1))

    def test_create_task_with_parameters_without_parameters(self):
        # arrange
        def test_task():
            return 1

        task1 = AlgorithmExecutionTask(test_task, 0, {})

        # act
        result = self._task_factory.create_tasks_with_parameters(test_task, TaskType.ALGORITHM_EXECUTION)

        # assert
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].get_task_name(), task1.get_task_name())
        self.assertEqual(result[0].get_param_dict(), task1.get_param_dict())
        self.assertEqual(type(result[0]), type(task1))

import unittest

from cpdbench.exception.ValidationException import InputValidationException, AlgorithmValidationException
from cpdbench.task.AlgorithmExecutionTask import AlgorithmExecutionTask
from cpdbench.task.DatasetFetchTask import DatasetFetchTask
from cpdbench.task.MetricExecutionTask import MetricExecutionTask


class TestTasks(unittest.TestCase):

    def test_DatasetFetchTask_correctValidation(self):
        # arrange
        def ds_task():
            return 1

        task = DatasetFetchTask(ds_task, 0, {})

        # act, assert
        task.validate_task()

    def test_DatasetFetchTask_correctValidation_exception(self):
        # arrange
        def ds_task(par):
            return 1

        task = DatasetFetchTask(ds_task, 0, {})

        # act, assert
        self.assertRaises(InputValidationException, task.validate_task)

    def test_AlgorithmExecutionTask_correctValidation(self):
        # arrange
        def ds_task(signa):
            return 1

        task = AlgorithmExecutionTask(ds_task, 0, {})

        # act, assert
        task.validate_task()

    def test_AlgorithmExecutionTask_correctValidation_exception(self):
        # arrange
        def ds_task(signal, sig):
            return 1

        def ds_task2():
            return 2

        task = AlgorithmExecutionTask(ds_task, 0, {})
        task2 = AlgorithmExecutionTask(ds_task2, 1, {})

        # act, assert
        self.assertRaises(InputValidationException, task.validate_task)
        self.assertRaises(InputValidationException, task2.validate_task)

    def test_MetricExecutionTask_correctValidation(self):
        # arrange
        def ds_task(a, b, c, *, d):
            return 1

        task = MetricExecutionTask(ds_task, 0, {})

        # act, assert
        task.validate_task()

    def test_MetricExecutionTask_correctValidation_exception(self):
        # arrange
        def ds_task(signal, sig):
            return 1

        def ds_task2(a, b, c, d):
            return 2

        task = MetricExecutionTask(ds_task, 0, {})
        task2 = MetricExecutionTask(ds_task2, 1, {})

        # act, assert
        self.assertRaises(InputValidationException, task.validate_task)
        self.assertRaises(InputValidationException, task2.validate_task)

    def test_DatasetFetchTask_get_task_name(self):
        # arrange
        def ds_task():
            return 1

        task = DatasetFetchTask(ds_task, 0, {})

        # act, assert
        self.assertEqual(task.get_task_name(), "dataset:ds_task:0")

    def test_AlgorithmExecutionTask_get_task_name(self):
        # arrange
        def ds_task():
            return 1

        task = AlgorithmExecutionTask(ds_task, 6, {})

        # act, assert
        self.assertEqual(task.get_task_name(), "algorithm:ds_task:6")

    def test_general_validateInput(self):
        # arrange
        def ds_task():
            raise KeyError

        task = AlgorithmExecutionTask(ds_task, 0, {})

        # act, assert
        self.assertRaises(AlgorithmValidationException, task.validate_input, None)

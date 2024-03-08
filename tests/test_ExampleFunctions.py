import unittest

from cpdbench.examples import ExampleMetrics


class TestExampleFunctions(unittest.TestCase):

    def test_metric_accuracy_in_allowed_windows(self):
        # act
        result = ExampleMetrics.metric_accuracy_in_allowed_windows(
            [35, 68, 866], [0.3, 0.8, 0.01],
            [37, 72], window_size=5
        )

        # assert
        self.assertEqual(result, 0.5)

    def test_metric_accuracy_in_allowed_windows_all_correct(self):
        # act
        result = ExampleMetrics.metric_accuracy_in_allowed_windows(
            [35, 68, 866], [0.3, 0.8, 0.01],
            [37, 72], window_size=10
        )

        # assert
        self.assertEqual(result, 1)

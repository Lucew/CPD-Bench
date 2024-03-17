import unittest

from cpdbench.task.Task import TaskType
from cpdbench.utils.UserConfig import UserConfig


class TestUserConfig(unittest.TestCase):

    def test_get_number_of_executions_empty_config(self):
        # arrange
        empty_config = UserConfig({})
        empty_config_2 = UserConfig({
            "metric-executions": None
        })

        # act, assert
        self.assertEqual(empty_config.get_number_of_executions(TaskType.DATASET_FETCH),
                         1)
        self.assertEqual(empty_config_2.get_number_of_executions(TaskType.ALGORITHM_EXECUTION),
                         1)

    def test_get_number_of_executions_normal_config(self):
        # arrange
        config = UserConfig({
            "dataset-executions": [
                {"window_size": 42, "x": 65},
                {"window_size": 42, "x": 56},
                {"window_size": 47, "x": 8},
            ]
        })

        # act, assert
        self.assertEqual(config.get_number_of_executions(TaskType.DATASET_FETCH),
                         3)

    def test_get_number_of_executions_inconsistent_config(self):
        # arrange
        config = UserConfig({
            "dataset-executions": [
                {"window_size": 42, "x": 65},
                {"window_size": 42},
                {"window_size": 47, "x": 8},
            ]
        })

        # act, assert
        self.assertEqual(config.get_number_of_executions(TaskType.DATASET_FETCH),
                         3)

    def test_get_user_param_global_param(self):
        # arrange
        config = UserConfig({
            "dataset-executions": [
                {"window_size": 42, "x": 65},
                {"window_size": 42},
                {"window_size": 47, "x": 8},
            ],
            "test": [24, 24]
        })

        # act, assert
        self.assertEqual(config.get_user_param("test", None),
                         [[24, 24]])

    def test_get_user_param_user_param(self):
        # arrange
        config = UserConfig({
            "dataset-executions": [
                {"window_size": 42, "x": 65},
                {"window_size": 42},
                {"window_size": 47, "x": 8},
            ],
            "test": [24, 24]
        })

        # act, assert
        self.assertEqual(config.get_user_param("window_size", TaskType.DATASET_FETCH),
                         [42, 42, 47])

    def test_get_user_param_inconsistent_param(self):
        # arrange
        config = UserConfig({
            "dataset-executions": [
                {"window_size": 42, "x": 65},
                {"window_size": 42},
                {"window_size": 47, "x": 8},
            ],
            "test": [24, 24]
        })

        # act, assert
        with self.assertRaises(Exception) as cm:
            config.get_user_param("x", TaskType.DATASET_FETCH)
        exc = cm.exception
        self.assertEqual(str(exc), "Parameter not found")

    def test_get_user_param_non_existing_param(self):
        # arrange
        config = UserConfig({
            "dataset-executions": [
                {"window_size": 42, "x": 65},
                {"window_size": 42},
                {"window_size": 47, "x": 8},
            ],
            "test": [24, 24]
        })

        # act, assert
        with self.assertRaises(Exception) as cm:
            config.get_user_param("x", TaskType.METRIC_EXECUTION)
        exc = cm.exception
        self.assertEqual(str(exc), "Parameter not found")

    def test_check_if_global_param_global_param(self):
        # arrange
        config = UserConfig({
            "dataset-executions": [
                {"window_size": 42, "x": 65},
                {"window_size": 42},
                {"window_size": 47, "x": 8},
            ],
            "test": [24, 24]
        })

        # act, assert
        self.assertEqual(config.check_if_global_param("test"), True)

    def test_check_if_global_param_user_param(self):
        # arrange
        config = UserConfig({
            "dataset-executions": [
                {"window_size": 42, "x": 65},
                {"window_size": 42},
                {"window_size": 47, "x": 8},
            ],
            "test": [24, 24]
        })

        # act, assert
        self.assertEqual(config.check_if_global_param("window_size"), False)

    def test_check_if_global_param_non_existing_param(self):
        # arrange
        config = UserConfig({
            "dataset-executions": [
                {"window_size": 42, "x": 65},
                {"window_size": 42},
                {"window_size": 47, "x": 8},
            ],
            "test": [24, 24]
        })

        # act, assert
        with self.assertRaises(Exception) as cm:
            config.check_if_global_param("y")
        exc = cm.exception
        self.assertEqual(str(exc), "Parameter not found: y")

    def test_check_if_global_param_both_global_and_execution(self):
        # arrange
        config = UserConfig({
            "dataset-executions": [
                {"window_size": 42, "x": 65},
                {"window_size": 42},
                {"window_size": 47, "x": 8},
            ],
            "x": [24, 24]
        })

        # act, assert
        with self.assertRaises(Exception) as cm:
            config.check_if_global_param("x")
        exc = cm.exception
        self.assertEqual(str(exc), "Parameter both global and execution")

    def test_check_if_global_param_no_execution_params(self):
        # arrange
        config = UserConfig({
            "x": [24, 24],
            "y": 75
        })

        # act, assert
        self.assertEqual(config.check_if_global_param("x"), True)

    def test_validate_user_config_all_correct(self):
        # arrange
        config = UserConfig({
            "z": [24, 24],
            "y": 75,
            "dataset-executions": [
                {"window_size": 42, "x": 5},
                {"window_size": 42, "x": 5}
            ]
        })

        # act, assert
        config.validate_user_config()

    def test_validate_user_config_empty(self):
        # arrange
        config = UserConfig()

        # act, assert
        config.validate_user_config()

    def test_validate_user_config_execution_params_declared_wrong(self):
        # arrange
        config = UserConfig({
            "z": [24, 24],
            "y": 75,
            "dataset-executions": [
                {"window_size": 42, "x": 5},
                {"window_size": 42, "x": 5}
            ],
            "algorithm-executions": 64
        })

        # act, assert
        with self.assertRaises(Exception) as cm:
            config.validate_user_config()
        exc = cm.exception
        self.assertEqual(str(exc), "execution params not declared correctly")

    def test_validate_user_config_execution_params_declared_wrong2(self):
        # arrange
        config = UserConfig({
            "z": [24, 24],
            "y": 75,
            "dataset-executions": [
                {"window_size": 42, "x": 5},
                {"window_size": 42, "x": 5}
            ],
            "algorithm-executions": [65, 314]
        })

        # act, assert
        with self.assertRaises(Exception) as cm:
            config.validate_user_config()
        exc = cm.exception
        self.assertEqual(str(exc), "execution params not declared correctly")

    def test_validate_user_config_param_not_found_in_all_configurations(self):
        # arrange
        config = UserConfig({
            "z": [24, 24],
            "y": 75,
            "dataset-executions": [
                {"window_size": 42, "x": 5},
                {"window_size": 42}
            ]
        })

        # act, assert
        with self.assertRaises(Exception) as cm:
            config.validate_user_config()
        exc = cm.exception
        self.assertEqual(str(exc), "Parameter not found in all configurations: x")

    def test_validate_user_config_params_defined_as_both_global_and_execution(self):
        # arrange
        config = UserConfig({
            "x": [24, 24],
            "y": 75,
            "dataset-executions": [
                {"window_size": 42, "x": 5},
                {"window_size": 42, "x": 6}
            ]
        })

        # act, assert
        with self.assertRaises(Exception) as cm:
            config.validate_user_config()
        exc = cm.exception
        self.assertEqual(str(exc), "Parameter x both global and execution")


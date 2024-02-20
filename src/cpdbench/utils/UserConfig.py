from cpdbench.task.Task import TaskType


def _get_path_to_execution_array(task_type: TaskType) -> str:
    if task_type == TaskType.DATASET_FETCH:
        return "dataset-executions"
    elif task_type == TaskType.ALGORITHM_EXECUTION:
        return "algorithm-executions"
    else:
        return "metric-executions"


class UserConfig:
    def __init__(self, user_params: dict) -> None:
        self._user_param_dict = user_params

    def get_number_of_executions(self, tasks_type: TaskType) -> int:
        execution_yaml = self._user_param_dict[_get_path_to_execution_array(tasks_type)]
        if execution_yaml is None:
            return 0
        return len(execution_yaml)

    def get_user_param(self, param_name: str, task_type: TaskType) -> list:
        global_param = self._user_param_dict.get(param_name)
        if global_param is not None:
            return [global_param]
        else:
            dict_string = _get_path_to_execution_array(task_type)
            exec_list = self._user_param_dict[dict_string]
            if exec_list is None:
                raise Exception("Parameter not found")
            try:
                result = [execution_dict[param_name] for execution_dict in exec_list]
            except KeyError:
                raise Exception("Parameter not found")
            else:
                if result is None or len(result) == 0:
                    raise Exception("Parameter not found")
                return result

    def check_if_global_param(self, param_name: str) -> bool:
        global_param = self._user_param_dict.get(param_name)
        if global_param is not None:
            return True
        return False

    def get_param_dict(self) -> dict:
        return self._user_param_dict

from cpdbench.task.Task import TaskType


def _get_path_to_execution_array(task_type: TaskType) -> str:
    """Returns the path in the user config dict to the needed execution variables depending on the task type
    :param task_type: the task type for which the path is needed
    :return: the path in the user config
    """
    if task_type == TaskType.DATASET_FETCH:
        return "dataset-executions"
    elif task_type == TaskType.ALGORITHM_EXECUTION:
        return "algorithm-executions"
    else:
        return "metric-executions"


class UserConfig:
    """This class represents the part of the global config file which contains all user variables.
    There are two types of user parameters/variables in this testbench:
    - global variables: variables which can be used in any task, and can only be defined once
    - execution variables: specific variables for each task type, for which multiple instances/different values given
        as list can exist. In this case, any task using these are executed multiple times depending on the amount of
        given instances. A use case for this is executing the same algorithm but with different parameters.
    """

    def __init__(self, user_params=None):
        """Constructor for the UserConfig class
        :param user_params: the user params as dict extracted from the config file
        """
        if user_params is None:
            user_params = {}
        self._user_param_dict = user_params

    def get_number_of_executions(self, tasks_type: TaskType) -> int:
        """Returns the needed number of executions of each task for the given type depending on the amount of
        parameter sets
        :param tasks_type: the task type for which the number should be returned
        :return: the number of executions
        """
        if self._user_param_dict == {}:
            return 1
        execution_yaml = self._user_param_dict.get(_get_path_to_execution_array(tasks_type))
        if execution_yaml is None:
            return 1
        return len(execution_yaml)

    def get_user_param(self, param_name: str, task_type: TaskType) -> list:
        """Returns the values of the given user parameter name.
        Returns a list because for execution variables multiple instances (for multiple runs) can be defined.
        Throws an exception if the parameter is not defined.
        :param param_name: the name of the user parameter
        :param task_type: the task type if the parameter is an execution variable.
        If it is a global variable, this parameter is not used.
        :return: a list of all possible values for the requested parameter
        """
        global_param = self._user_param_dict.get(param_name)
        if global_param is not None:
            return [global_param]
        else:
            dict_string = _get_path_to_execution_array(task_type)
            try:
                exec_list = self._user_param_dict[dict_string]
            except KeyError:
                raise Exception("Parameter not found")
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
        """Checks if the given parameter is a global one or an execution parameter.
        :param param_name: the name of the to be checked parameter
        :return: True if the parameter is a global one. False otherwise.
        """
        is_global_param = None
        global_param = self._user_param_dict.get(param_name)
        if global_param is not None:
            is_global_param = True
        for i in ["dataset-executions", "algorithm-executions", "metric-executions"]:
            part_dict = self._user_param_dict.get(i)
            if part_dict is None or part_dict[0] is None:
                continue
            user_param = part_dict[0].get(param_name)
            if user_param is not None:
                if is_global_param is True:
                    raise Exception("Parameter both global and execution")
                else:
                    return False
        if is_global_param is None:
            raise Exception("Parameter not found: " + param_name)
        else:
            return is_global_param

    def get_param_dict(self) -> dict:
        """Returns all user params as dict for logging purposes.
        :return: the user param dict"""
        return self._user_param_dict

    def validate_user_config(self) -> None:
        """Validates the user config for common errors.
        This method returns nothing if the validation is successful, and throws errors
        if something is wrong with the config, as the bench cannot continue with consistency
        errors in the config.
        """
        # execution params are declared correctly
        for i in ["dataset-executions", "algorithm-executions", "metric-executions"]:
            exec_dict = self._user_param_dict.get(i)
            if exec_dict is None:
                continue
            if type(exec_dict) is not list:
                raise Exception("execution params not declared correctly")
            for j in exec_dict:
                if type(j) is not dict:
                    raise Exception("execution params not declared correctly")

        # execution param is given for all configurations
        for i in ["dataset-executions", "algorithm-executions", "metric-executions"]:
            part_dict = self._user_param_dict.get(i)
            if part_dict is None:
                continue
            exec_params = [param for param in part_dict[0]]
            for j in range(1, len(part_dict)):
                for par in exec_params:
                    if part_dict[j].get(par) is None:
                        raise Exception("Parameter not found in all configurations: " + par)

        params = self._get_all_params()
        for param in params:
            # parameters are defined as both global and execution
            is_global_param = None
            global_param = self._user_param_dict.get(param)
            if global_param is not None:
                is_global_param = True
            for i in ["dataset-executions", "algorithm-executions", "metric-executions"]:
                part_dict = self._user_param_dict.get(i)
                if part_dict is None:
                    continue
                user_param = part_dict[0].get(param)
                if user_param is not None:
                    if is_global_param is True:
                        raise Exception(f"Parameter {param} both global and execution")

    def _get_all_params(self) -> set:
        params = [param for param in self._user_param_dict
                  if param not in ["dataset-executions", "algorithm-executions", "metric-executions"]]
        for i in ["dataset-executions", "algorithm-executions", "metric-executions"]:
            exec_dict = self._user_param_dict.get(i)
            if exec_dict is None:
                continue
            user_params = [param for param in exec_dict[0]]
            params = params + user_params
        return set(params)

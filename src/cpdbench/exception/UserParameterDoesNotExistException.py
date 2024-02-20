class UserParameterDoesNotExistException(Exception):
    """Exception type when a needed user parameter in a dataset, algorithm or metric does not exist in the config
    file."""
    msg_text = "The user parameter [{0}] is needed for running [{1}], but does not exist in the given config file."

    def __init__(self, param_name, function_name):
        super().__init__(self.msg_text.format(param_name, function_name))

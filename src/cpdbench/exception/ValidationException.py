class ValidationException(Exception):
    """General exception type when some validation went wrong."""
    pass


class InputValidationException(ValidationException):
    """More specific validation exception when something about the input parameters is wrong."""
    pass


class AlgorithmValidationException(ValidationException):
    """Validation exception when runtime validation of an algorithm fails."""
    pass


class MetricValidationException(ValidationException):
    """Validation exception when runtime validation of a metric fails."""
    pass


class DatasetValidationException(ValidationException):
    """Validation exception when runtime validation of a dataset fails."""
    pass


class UserConfigValidationException(ValidationException):
    """Validation exception when user config part is inconsistent"""

    def __init__(self, problem):
        super().__init__(f"User config is invalid: {problem}")

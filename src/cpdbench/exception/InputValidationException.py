from cpdbench.exception.ValidationException import ValidationException


class InputValidationException(ValidationException):
    """More specific validation exception when something about the input parameters is wrong."""
    pass

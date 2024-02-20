import inspect
from typing import Callable

"""Utils.py module
This module contains various utility functions which are needed by multiple objects in the testbench
"""


def get_name_of_function(function_ref: Callable) -> str:
    """Returns the name of the given function reference/object by using the inspect module
    :param function_ref: the function reference
    :return: the name of the function
    """
    name_gen = (attr[1] for attr in inspect.getmembers(function_ref) if attr[0] == "__name__")
    return next(name_gen)

import inspect


def get_name_of_function(function_ref) -> str:
    name_gen = (attr[1] for attr in inspect.getmembers(function_ref) if attr[0] == "__name__")
    return next(name_gen)

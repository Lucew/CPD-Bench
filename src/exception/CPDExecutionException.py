class CPDExecutionException(Exception):
    """General Exception type when something goes wrong in dataset fetching, algorithm execution or metric
    calculation."""
    def __init__(self, message):
        super().__init__(message)


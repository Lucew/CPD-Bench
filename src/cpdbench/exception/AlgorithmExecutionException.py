from cpdbench.exception.CPDExecutionException import CPDExecutionException


class AlgorithmExecutionException(CPDExecutionException):
    """Exception type when the execution of an algorithm on a dataset has failed"""

    standard_msg = 'Error while executing the algorithm {0} on dataset {1}'

    def __init__(self, algorithm_function, dataset_function):
        super().__init__(self.standard_msg.format(algorithm_function, dataset_function))

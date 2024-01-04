from cpdbench.exception.CPDExecutionException import CPDExecutionException


class MetricExecutionException(CPDExecutionException):
    """Exception type when the execution of a metric on an algorithm result has failed"""

    standard_msg = 'Error while executing the metric {0} on algorithm {1} (dataset {2})'

    def __init__(self, metric_function, algorithm_function, dataset_function):
        super().__init__(self.standard_msg.format(metric_function, algorithm_function, dataset_function))

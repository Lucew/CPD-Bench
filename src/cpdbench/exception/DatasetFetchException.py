from cpdbench.exception.CPDExecutionException import CPDExecutionException


class DatasetFetchException(CPDExecutionException):
    """Exception type when something goes wrong while loading a dataset"""

    def __init__(self, message):
        super().__init__(message)


class CPDDatasetCreationException(DatasetFetchException):
    """Exception type when the initialization and creation of the CPDDataset object has failed"""
    standard_msg_create_dataset = "Error while creating the CPDDataset object with the {0} function"

    def __init__(self, dataset_function):
        # function_name = get_name_of_function(dataset_function)
        super().__init__(self.standard_msg_create_dataset.format(dataset_function))


class FeatureLoadingException(DatasetFetchException):
    """Exception type when the loading of a feature of a CPDDataset has failed"""
    standard_msg_load_feature = "Error while loading feature {0} of the CPDDataset from function {1}"

    def __init__(self, dataset_function, feature):
        # function_name = get_name_of_function(dataset_function)
        super().__init__(self.standard_msg_load_feature.format(feature, dataset_function))


class SignalLoadingException(DatasetFetchException):
    """Exception type when the loading of a signal of a CPDDataset has failed"""
    standard_msg_load_signal = "Error while loading the signal of the CPDDataset from function {0}"

    def __init__(self, dataset_function):
        super().__init__(self.standard_msg_load_signal.format(dataset_function))

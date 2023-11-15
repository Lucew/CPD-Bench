from exception.CPDExecutionException import CPDExecutionException
from utils.Utils import get_name_of_function

standard_msg_create_dataset = "Error while creating the CPDDataset object with the {0} function"

standard_msg_load_feature = "Error while loading feature {0} of the CPDDataset from function {1}"


class DatasetFetchException(CPDExecutionException):
    """Exception type when something goes wrong while loading a dataset"""

    def __init__(self, message):
        super().__init__(message)


class CPDDatasetCreationException(DatasetFetchException):
    """Exception type when the initialization and creation of the CPDDataset object has failed"""

    # TODO: Objekt mitgeben?
    def __init__(self, dataset_function):
        #function_name = get_name_of_function(dataset_function)
        super().__init__(standard_msg_create_dataset.format(dataset_function))


class FeatureLoadingException(DatasetFetchException):
    """Exception type when the loading of a feature of a CPDDataset has failed"""

    # TODO: Objekt mitgeben?
    def __init__(self, dataset_function, feature):
        #function_name = get_name_of_function(dataset_function)
        super().__init__(standard_msg_load_feature.format(feature, dataset_function))

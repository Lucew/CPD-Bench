from cpdbench.examples.ExampleDatasets import get_extreme_large_dataset_from_file
from cpdbench.examples.ExampleAlgorithms import numpy_array_accesses
from cpdbench.examples.ExampleMetrics import metric_accuracy_in_allowed_windows
from cpdbench.interface.CPDBench import CPDBench
import pathlib

cpdb = CPDBench()


@cpdb.dataset
def get_large_dataset():
    return get_extreme_large_dataset_from_file()


@cpdb.algorithm
def execute_algorithm(dataset, *, array_indexes):
    return numpy_array_accesses(dataset, array_indexes)


@cpdb.metric
def compute_metric(indexes, confidences, ground_truths):
    return metric_accuracy_in_allowed_windows(indexes, confidences, ground_truths, window_size=20)


if __name__ == '__main__':
    path = pathlib.Path(__file__).parent.resolve()
    path = path.joinpath("configs", "VeryLargeDatasetConfig.yml")
    cpdb.start(config_file=str(path))

from cpdbench.examples import ExampleAlgorithms
from cpdbench.examples.ExampleDatasets import get_extreme_large_dataset_from_file
from cpdbench.examples.ExampleMetrics import metric_accuracy_in_allowed_windows
from cpdbench.CPDBench import CPDBench
import pathlib

cpdb = CPDBench()


@cpdb.dataset
def get_large_dataset():
    return get_extreme_large_dataset_from_file(1000)


@cpdb.algorithm
def execute_algorithm(dataset):
    dataset = dataset.reshape((1, dataset.size))
    res = ExampleAlgorithms.algorithm_execute_single_esst(dataset)
    assert dataset.ndim == 3
    return res


@cpdb.metric
def compute_metric(indexes, confidences, ground_truths):
    return metric_accuracy_in_allowed_windows(indexes, confidences, ground_truths, window_size=20)


if __name__ == '__main__':
    path = pathlib.Path(__file__).parent.resolve()
    path = path.joinpath("configs", "VeryLargeDatasetConfig.yml")
    #cpdb.start(config_file=str(path))
    cpdb.validate(config_file=str(path))

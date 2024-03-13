from cpdbench.CPDBench import CPDBench
import cpdbench.examples.ExampleDatasets as example_datasets
import cpdbench.examples.ExampleAlgorithms as example_algorithms
import cpdbench.examples.ExampleMetrics as example_metrics

cpdb = CPDBench()


@cpdb.dataset
def get_apple_dataset():
    return example_datasets.dataset_get_apple_dataset()


@cpdb.dataset
def get_bitcoin_dataset():
    return example_datasets.dataset_get_bitcoin_dataset()


@cpdb.algorithm
def execute_esst_test(signal, *, window_length):
    return example_algorithms.algorithm_execute_single_esst(signal, window_length)


@cpdb.metric
def calc_accuracy(indexes, scores, ground_truth, *, window_size):
    return example_metrics.metric_accuracy_in_allowed_windows(indexes, scores, ground_truth, window_size=window_size)


if __name__ == '__main__':
    cpdb.start("configs/parametersConfig.yml")

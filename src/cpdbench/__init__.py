"""
# The Changepoint-Detection Workbench (CPD-Bench)

This library is a performance and test benchmark for changepoint detection algorithms,
especially created for the [changepoynt project](https://github.com/Lucew/changepoynt).

## Important links
- [Main project page on GitHub](https://github.com/Lucew/CPD-Bench)
- [Changepoynt project](https://github.com/Lucew/changepoynt)
- [Documentation](https://lucew.github.io/CPD-Bench/cpdbench.html)


## Installation
Simply install the cpd-bench via pip and include it into your library:
`pip install cpdbench`

## Usage
A very basic configuration created with included example functions looks like this:

```
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
def execute_esst_test(signal):
    return example_algorithms.algorithm_execute_single_esst(signal)


@cpdb.metric
def calc_accuracy(indexes, scores, ground_truth):
    return example_metrics.metric_accuracy_in_allowed_windows(indexes, scores, ground_truth, window_size=25)


if __name__ == '__main__':
    cpdb.start()
```

For more examples please refer to the "examples" package.

"""
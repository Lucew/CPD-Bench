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
### Basic usage
1. Import cpdbench.CPDBench and create a CPDBench object cpdb
2. Use the decorators "dataset", "algorithm", and "metric" of this cpdb object to annotate your respective
changepoint dataset function, your changepoint algorithms and validation metrics.
The functions have to look like this:
- dataset: def dataset_funtion() -> dataset: cpdbench.dataset.CPDDataset
- algorithm: def algorithm_function(signal: ndarray) -> changepoints: list[int], confidences: list[float]
- metric: def metric_funtion(changepoints: list[int], confidences: list[float], ground_truths: list[int]) -> result: float
3. Use cpdb.start() to start the workbench

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

### Configuration
You can configure multiple settings using a config.yml file.
For this create a config.yml file with the syntax/commands given in cpdbench.examples.configs.parametersConfig.yml
and enter the file path when running the bench: cpdb.start(config_file)

### Use of parameters
Use parameters in your own functions as global placeholders (global parameters) or to run the function multiple
times with different configurations (runtime parameters).
To use parameters declare them in your function heads as keyword-only parameters, for example:
`def algorithm_function(signal, *, example_param)`
Then enter the values in your config file:
- global param: user -> "param name: value"
- runtime param: user -> dataset-executions/algorithm-executions/metric-executions -> list of "param name: value" for the
amount of executions/run configurations.
Example:
```
user:
  global_param1: 242
  global_param2: 353
  algorithm_executions:
    - runtime_param1: 2424
      runtime_param2: 3
    - runtime_param1: 345
      runtime_param2: 3
```

For more examples please refer to the "examples" package.
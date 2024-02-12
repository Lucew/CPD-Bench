from cpdbench.interface.CPDBench import CPDBench
import cpdbench.utils.Functions as example_functions

cpdb = CPDBench()


@cpdb.dataset
def get_apple_dataset(*, bound):
    return example_functions.dataset_get_apple_dataset()


@cpdb.dataset
def get_bitcoin_dataset():
    return example_functions.dataset_get_bitcoin_dataset()


# @cpdb.algorithm
# def execute_esst(signal):
#     return example_functions.algorithm_execute_single_esst(signal)


@cpdb.algorithm
def execute_esst_test(signal, *, abc, bound):
    print(abc)
    print(bound)
    return example_functions.algorithm_execute_single_esst(signal)


@cpdb.metric
def calc_accuracy(indexes, scores, ground_truth):
    return example_functions.metric_accuracy_in_allowed_windows(indexes, scores, ground_truth)


if __name__ == '__main__':
    cpdb.start()

import time
import numpy as np
from changepoynt.algorithms.sst import SST

from cpdbench.dataset.CPDNdarrayDataset import CPDNdarrayDataset
from cpdbench.examples import ExampleMetrics
from cpdbench.CPDBench import CPDBench

# Instructions for performance test:
# 1. Choose raw_data depending on the wished performance test configuration

raw_data = np.load("../data/apple.npy")
# raw_data = np.load("../data/apple_small.npy")
# raw_data = np.load("../data/apple_medium.npy")
# raw_data = np.load("../data/apple_big.npy")
# raw_data = np.load("../data/apple_very_big.npy")

# 2. Run test script: python3 overhead_performance_test.py

timeseries = raw_data[:, 0]
reshaped_ts = np.reshape(timeseries, [1, timeseries.size])

cpdb = CPDBench()


@cpdb.dataset
def get_apple():
    return CPDNdarrayDataset(reshaped_ts, [200])


@cpdb.algorithm
def calc_sst(signal):
    detector = SST(250, method='svd')
    sig = signal[0]
    res = detector.transform(sig)
    indexes = [res.argmax()]
    confidences = [1.0]
    return indexes, confidences


@cpdb.metric
def calc_metric(indexes, confidences, ground_truth):
    return ExampleMetrics.metric_accuracy_in_allowed_windows(indexes, confidences, ground_truth, window_size=25)


def manual_test():
    """Uses SST as implemented in the changepoynt library as algorithm."""
    detector = SST(250, method='svd')
    sig = reshaped_ts[0]
    res = detector.transform(sig)
    indexes = [res.argmax()]
    confidences = [1.0]
    accuracy = 0
    ground_truth = [200]
    window_size = 25
    for gt in ground_truth:
        range_of_gt = range(int(gt - (window_size / 2)), int(gt + (window_size / 2)))
        hits = [i for i in indexes if i in range_of_gt]
        if len(hits) > 0:
            accuracy += (1 / len(ground_truth))
    # print(accuracy)


if __name__ == '__main__':
    result = 0
    for i in range(5):
        runtime = time.perf_counter()
        manual_test()
        runtime_new = time.perf_counter() - runtime
        print(runtime_new)
        result += runtime_new
    print("result of manual execution:" + str(result / 5))
    result = 0
    for i in range(5):
        runtime = time.perf_counter()
        cpdb.start()
        runtime_new = time.perf_counter() - runtime
        print(runtime_new)
        result += runtime_new
    print("result of framework execution:" + str(result / 5))

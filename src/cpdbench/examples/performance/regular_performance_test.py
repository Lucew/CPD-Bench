import time
import numpy as np
from changepoynt.algorithms.sst import SST

from cpdbench.dataset.CPD2DNdarrayDataset import CPD2DNdarrayDataset
from cpdbench.examples import ExampleMetrics
from cpdbench.CPDBench import CPDBench

raw_data = np.load("/Users/dominik/Documents/Projects/CPD-Bench/data/apple_very_big.npy")
timeseries = raw_data[:, 0]
reshaped_ts = np.reshape(timeseries, [1, timeseries.size])


cpdb = CPDBench()

@cpdb.dataset
def get_small_apple():
    return CPD2DNdarrayDataset(reshaped_ts, [200])

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
        #manual_test()
        cpdb.start()
        runtime_new = time.perf_counter() - runtime
        print(runtime_new)
        result += runtime_new
    print(result / 10)
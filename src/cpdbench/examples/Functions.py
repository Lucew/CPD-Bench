"""Functions.py
Contains some example datasets, algorithms and metrics for trying out the testbench
"""
import numpy as np
from changepoynt.algorithms.sst import SST

from cpdbench.dataset.CPD2DNdarrayDataset import CPD2DNdarrayDataset


def metric_accuracy_in_allowed_windows(indexes, scores, ground_truth, *, window_size):
    """Calculate the accuracy with a small deviation window.
    The result is the percentage of ground truth values, for which the algorithm got at least one fitting index in the
    surrounding window. The scores are ignored.
    """
    accuracy = 0
    for gt in ground_truth:
        range_of_gt = range(int(gt - (window_size / 2)), int(gt + (window_size / 2)))
        hits = [i for i in indexes if i in range_of_gt]
        if len(hits) > 0:
            accuracy += (1 / len(ground_truth))
    return accuracy


def algorithm_execute_single_esst(signal):
    """Uses SST as implemented in the changepoynt library as algorithm."""
    detector = SST(90, method='rsvd')
    sig = signal[0]
    res = detector.transform(sig)
    indexes = [res.argmax()]
    confidences = [1.0]
    return indexes, confidences


def dataset_get_apple_dataset():
    raw_data = np.load("data/apple.npy")
    timeseries = raw_data[:, 0]
    reshaped_ts = np.reshape(timeseries, [1, timeseries.size])
    return CPD2DNdarrayDataset(reshaped_ts, [337])


def dataset_get_bitcoin_dataset():
    raw_data = np.load("data/bitcoin.npy")
    timeseries = raw_data[:, 0]
    reshaped_ts = np.reshape(timeseries, [1, timeseries.size])
    return CPD2DNdarrayDataset(reshaped_ts, [569])

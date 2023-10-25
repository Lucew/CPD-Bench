import matplotlib.pyplot as plt

from interface.CPD2DNdarrayDataset import CPD2DNdarrayDataset
from interface.CPDBench import CPDBench
import numpy as np
from changepoynt.algorithms.sst import SST
from changepoynt.visualization.score_plotting import plot_data_and_score

cpdb = CPDBench()


@cpdb.dataset
def get_apple_dataset():
    return CPD2DNdarrayDataset(np.load("../data/apple.npy"))


@cpdb.algorithm
def execute_esst(signal):
    detector = SST(30)
    sig = signal[:, 0]
    res = detector.transform(sig)
    indexes = [res.argmax()]
    confidences = [1.0]
    return indexes, confidences


@cpdb.metric
def calc_accuracy(indexes, scores, ground_truth):
    correct_preds = len(set(indexes) & set(ground_truth))
    return correct_preds / len(indexes)


dataset = np.load("../data/apple.npy")
one, two = execute_esst(dataset)
print("done")

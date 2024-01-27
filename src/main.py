from cpdbench.interface.CPD2DNdarrayDataset import CPD2DNdarrayDataset
from cpdbench.interface.CPDBench import CPDBench
import numpy as np
from changepoynt.algorithms.sst import SST
from changepoynt.algorithms.fluss import FLUSS
from changepoynt.algorithms.clasp import CLASP

cpdb = CPDBench()


@cpdb.dataset
def get_apple_dataset():
    raw_data = np.load("../data/apple.npy")
    timeseries = raw_data[:, 0]
    reshaped_ts = np.reshape(timeseries, [1, timeseries.size])
    # raise Exception
    return CPD2DNdarrayDataset(reshaped_ts, [337])


@cpdb.dataset
def get_bitcoin_dataset():
    raw_data = np.load("../data/bitcoin.npy")
    timeseries = raw_data[:, 0]
    reshaped_ts = np.reshape(timeseries, [1, timeseries.size])
    # raise Exception
    return CPD2DNdarrayDataset(reshaped_ts, [569])


@cpdb.algorithm
def execute_esst(signal):
    detector = SST(90, method='rsvd')
     #detector = FLUSS(100)
    # detector = CLASP()
    sig = signal[0]
    print("begin transform")
    res = detector.transform(sig)
    indexes = [res.argmax()]
    confidences = [1.0]
    # raise Exception
    return indexes, confidences

#@cpdb.algorithm
def execute_test(signal):
    pass


@cpdb.metric
def calc_accuracy(indexes, scores, ground_truth):
    correct_preds = len(set(indexes) & set(ground_truth))
    # raise Exception
    return correct_preds / len(indexes)


if __name__ == '__main__':
    # dataset = np.load("../data/apple.npy")
    # one, two = execute_esst(dataset)
    # print("done")
    cpdb.start()

# TODO: Datasets blockieren sich
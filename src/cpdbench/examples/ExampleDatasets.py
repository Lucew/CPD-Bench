import pathlib

import numpy as np

from cpdbench.dataset.CPD2DFromFileDataset import CPD2DFromFileDataset
from cpdbench.dataset.CPDNdarrayDataset import CPDNdarrayDataset


def get_extreme_large_dataset_from_file(validation_amount=-1):
    path = pathlib.Path(__file__).parent.resolve()
    path = path.joinpath("data", "very_big_numpy_file.dat")
    dataset = CPD2DFromFileDataset(str(path), "float32", [5, 245, 255, 256, 25], validation_amount)
    return dataset


def dataset_get_apple_dataset():
    raw_data = np.load("data/apple.npy")
    timeseries = raw_data[:, 0]
    reshaped_ts = np.reshape(timeseries, [1, timeseries.size])
    return CPDNdarrayDataset(reshaped_ts, [337])


def dataset_get_bitcoin_dataset():
    raw_data = np.load("data/bitcoin.npy")
    timeseries = raw_data[:, 0]
    reshaped_ts = np.reshape(timeseries, [1, timeseries.size])
    return CPDNdarrayDataset(reshaped_ts, [569])

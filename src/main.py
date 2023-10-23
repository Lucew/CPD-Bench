from interface.CPD2DNdarrayDataset import CPD2DNdarrayDataset
from interface.CPDBench import CPDBench
import numpy as np

cpdb = CPDBench()


@cpdb.dataset
def get_apple_dataset():
    return CPD2DNdarrayDataset(np.load("../data/apple.npy"))

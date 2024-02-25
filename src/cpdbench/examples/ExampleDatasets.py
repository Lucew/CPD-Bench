import pathlib

from cpdbench.dataset.CPD2DFromFileDataset import CPD2DFromFileDataset


def get_extreme_large_dataset_from_file():
    path = pathlib.Path(__file__).parent.resolve()
    path = path.joinpath("data", "very_big_numpy_file.dat")
    dataset = CPD2DFromFileDataset(str(path), "float32", [5, 245, 255, 256, 25])
    return dataset

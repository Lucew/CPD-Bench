import numpy as np

data = np.arange(2000000000)  # 8 GB big file
file_ref = np.memmap("very_big_numpy_file.dat", dtype="float32", mode="w+", shape=(2000000000,))
file_ref[:] = data[:]
file_ref.flush()

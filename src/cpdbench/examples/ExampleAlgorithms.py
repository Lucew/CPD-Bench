from changepoynt.algorithms.sst import SST


def numpy_array_accesses(dataset, array_indexes):
    indexes = []
    for i in array_indexes:
        indexes.append(dataset[i])
    confidences = [1 for _ in range(len(indexes))]
    return indexes, confidences


def algorithm_execute_single_esst(signal, window_length=90):
    """Uses SST as implemented in the changepoynt library as algorithm."""
    detector = SST(window_length, method='rsvd')
    sig = signal[0]
    res = detector.transform(sig)
    indexes = [res.argmax()]
    confidences = [1.0]
    return indexes, confidences

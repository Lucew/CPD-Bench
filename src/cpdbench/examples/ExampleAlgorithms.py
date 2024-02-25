def numpy_array_accesses(dataset, array_indexes):
    indexes = []
    for i in array_indexes:
        indexes.append(dataset[i])
    confidences = [1 for _ in range(len(indexes))]
    return indexes, confidences

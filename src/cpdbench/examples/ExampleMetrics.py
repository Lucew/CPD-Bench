
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

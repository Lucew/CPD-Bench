from exception.ResultSetInconsistentException import ResultSetInconsistentException


class CPDDatasetResult:
    def __init__(self, dataset, amount_features, algorithms, metrics):
        self._dataset = dataset.get_task_name()
        self._algorithms = [a.get_task_name() for a in algorithms]
        self._metrics = [m.get_task_name() for m in metrics]
        self._amount_features = amount_features

        self._indexes = {}
        # { "1" : { "alg1": [14, 124, 1] } }
        self._scores = {}
        self._metric_scores = {}
        # { "1" : { "alg1": { "metr1": 212 } } }
        for i in range(0, self._amount_features):
            self._indexes[str(i)] = {}
            self._scores[str(i)] = {}
            self._metric_scores[str(i)] = {}
            for a in self._algorithms:
                self._metric_scores[str(i)][a] = {}

    def add_algorithm_result(self, indexes, scores, feature, algorithm):
        if feature > self._amount_features - 1 or algorithm not in self._algorithms:
            raise ResultSetInconsistentException()
        self._indexes[feature][algorithm] = indexes
        self._scores[feature][algorithm] = scores

    def add_metric_score(self, metric_score, feature, algorithm, metric):
        if (feature > self._amount_features - 1
                or algorithm not in self._algorithms
                or metric not in self._metrics):
            raise ResultSetInconsistentException()
        self._metric_scores[feature][algorithm][metric] = metric_score

    def get_result_as_dict(self):
        return {
            self._dataset: {
                "amount_features": self._amount_features,
                "indexes": self._indexes,
                "scores": self._scores,
                "metric_scores": self._metric_scores
            }
        }

    def get_algorithms(self):
        return self._algorithms

    def get_metrics(self):
        return self._metrics

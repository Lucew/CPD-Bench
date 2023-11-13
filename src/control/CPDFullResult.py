# Structure:
# {
#   "datasets": [],
#   "algorithms": [],
#   "metrics": [],
#   "created": 242,
#   "last_updated": 252,
#   "results": {
#     "ds1": {
#       "amount_features" : 2,
#       "indexes": {
#         "f1": {
#           "alg1": []
#         }
#       },
#       "scores": {},
#       "metric_scores": {
#         "f1": {
#           "alg1": {
#             "metr1": []
#           }
#         }
#       }
#     }
#   }
# }
from control.CPDDatasetResult import CPDDatasetResult
import datetime


class CPDFullResult:

    def __init__(self):
        self._result = {}
        self._created = datetime.datetime.now()
        self._last_updated = self._created
        self._datasets = []
        self._algorithms = None
        self._metrics = None

    def add_dataset_result(self, dataset_result: CPDDatasetResult):
        for dataset_name, infos in dataset_result.get_result_as_dict().items():
            self._datasets.append(dataset_name)
            if self._algorithms is None:
                self._algorithms = dataset_result.get_algorithms()
                self._metrics = dataset_result.get_metrics()
            self._result = self._result | dataset_result.get_result_as_dict()
            self._last_updated = datetime.datetime.now()

    def get_result_as_dict(self):
        return {
            "datasets": self._datasets,
            "algorithms": self._algorithms,
            "metrics": self._metrics,
            "created": self._created,
            "last_updated": self._last_updated,
            "results": self._result
        }

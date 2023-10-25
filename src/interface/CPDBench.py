class CPDBench:

    def __init__(self):
        self._datasets = []
        self._algorithms = []
        self._metrics = []

    def start(self) -> None:
        pass

    def dataset(self, function):
        self._datasets.append(function)
        return function

    def algorithm(self, function):
        self._algorithms.append(function)
        return function

    def metric(self, function):
        self._metrics.append(function)
        return function


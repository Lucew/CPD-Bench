class CPDBench:

    def __init__(self):
        self.datasets = []
        self.algorithm = []
        self.metric = []

    def start(self) -> None:
        pass

    def dataset(self, function):
        self.datasets.append(function)
        return function

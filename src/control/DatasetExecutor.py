# TODO: Laufzeiten für alle Tasks
from concurrent.futures import ThreadPoolExecutor

from control.CPDDatasetResult import CPDDatasetResult, ErrorType
from exception.AlgorithmExecutionException import AlgorithmExecutionException
from exception.DatasetFetchException import CPDDatasetCreationException, SignalLoadingException
from exception.MetricExecutionException import MetricExecutionException


class DatasetExecutor:
    def __init__(self, dataset_task, algorithm_tasks, metric_tasks, logger):
        self._result: CPDDatasetResult = None  # Created later
        self._dataset_task = dataset_task
        self._algorithm_tasks = algorithm_tasks
        self._metric_tasks = metric_tasks
        self.logger = logger

    def execute(self):
        self._result = CPDDatasetResult(self._dataset_task, self._algorithm_tasks, self._metric_tasks)
        try:
            self._execute_dataset()
        except Exception as e:
            self.logger.exception(e)
            self._result.add_error(e, ErrorType.DATASET_ERROR)
        return self._result

    def _execute_dataset(self):
        try:
            self.logger.info(f"Start running tasks for dataset {self._dataset_task.get_task_name()}")
            self.logger.debug(f"Executing dataset task {self._dataset_task.get_task_name()}")
            dataset = self._dataset_task.execute()
            self.logger.debug(f"Finished dataset task {self._dataset_task.get_task_name()}")
        except Exception as e:
            raise CPDDatasetCreationException(self._dataset_task.get_task_name()) from e
        algorithms = []
        with ThreadPoolExecutor(max_workers=None) as executor:
            self.logger.debug(f"Getting signal")
            try:
                data, ground_truth = dataset.get_signal()
                self.logger.debug(f"Got signal")
            except Exception as e:
                raise SignalLoadingException(self._dataset_task.get_task_name()) from e
            else:
                self.logger.debug(f"Starting threads for executing algorithms")
                for algorithm in self._algorithm_tasks:
                    algorithms.append(executor.submit(self._execute_algorithm_and_metric, data,
                                                      algorithm, ground_truth))
                    self.logger.debug(f"Started thread for algorithm {algorithm.get_task_name()}")
        for i in range(0, len(algorithms)):
            try:
                algorithms[i].result()
            except Exception as e:
                self.logger.exception(e)
                self._result.add_error(e, ErrorType.ALGORITHM_ERROR, self._algorithm_tasks[i].get_task_name())
        self.logger.debug(f"All algorithm threads are finished")
        self.logger.debug(f"Finished!")

    def _execute_algorithm_and_metric(self, dataset, algorithm, ground_truth):
        logger = self.logger.getChild(algorithm.get_task_name())
        try:
            logger.debug(f"Executing algorithm task {algorithm.get_task_name()}")
            indexes, scores = algorithm.execute(dataset)
            logger.debug(f"Finished algorithm task {algorithm.get_task_name()}")
        except Exception as e:
            raise AlgorithmExecutionException(algorithm.get_task_name(),
                                              self._dataset_task.get_task_name()) from e
        self._result.add_algorithm_result(indexes, scores, algorithm.get_task_name())
        metrics = []
        logger.debug(f"Starting threads for executing metrics ")
        with ThreadPoolExecutor(max_workers=None) as executor:
            for metric in self._metric_tasks:
                metrics.append(executor.submit(self._calculate_metric, indexes, scores,
                                               metric, ground_truth, algorithm))
                logger.debug(f"Started thread for metric {metric.get_task_name()}")
        for i in range(0, len(metrics)):
            try:
                metrics[i].result()
            except Exception as e:
                logger.exception(e)
                self._result.add_error(e, ErrorType.METRIC_ERROR, algorithm.get_task_name(),
                                       self._metric_tasks[i].get_task_name())
        logger.debug(f"All metric threads are finished")
        logger.debug(f"Finished")

    def _calculate_metric(self, indexes, scores, metric_task, ground_truth, algorithm):
        logger = self.logger.getChild(algorithm.get_task_name()).getChild(metric_task.get_task_name())
        logger.debug(f"Executing metric task {metric_task.get_task_name()}")
        try:
            metric_result = metric_task.execute(indexes, scores, ground_truth)
            logger.debug(f"Finished metric task {metric_task.get_task_name()}")
        except Exception as e:
            raise MetricExecutionException(metric_task.get_task_name(), algorithm.get_task_name(),
                                           self._dataset_task.get_task_name()) from e
        self._result.add_metric_score(metric_result, algorithm.get_task_name(), metric_task.get_task_name())
        logger.debug("Finished")

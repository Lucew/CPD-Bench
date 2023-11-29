import concurrent
import multiprocessing
import traceback
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

from control.CPDDatasetResult import CPDDatasetResult
from control.CPDFullResult import CPDFullResult
from control.ExecutionController import ExecutionController
from exception.DatasetFetchException import CPDDatasetCreationException, FeatureLoadingException
from exception.ValidationException import ValidationException
from task.Task import TaskType
from task.TaskFactory import TaskFactory
from utils import Logger
from utils import Utils


# TODO: Multiprocessing Logging nach https://docs.python.org/3/howto/logging-cookbook.html#logging-to-a-single-file-from-multiple-processes

def create_ds_executor_and_run(dataset, algorithms, metrics):
    ds_executor = DatasetExecutor(dataset, algorithms, metrics)
    return ds_executor.execute()


class TestrunController(ExecutionController):

    def __init__(self):
        self._logger = Logger.get_application_logger()

    def execute_run(self, methods: dict) -> any:
        self._logger.info('Creating tasks...')
        tasks = self._create_tasks(methods)
        self._logger.info(f"{len(tasks['datasets']) + len(tasks['algorithms']) + len(tasks['metrics'])} tasks created")
        # TODO: Prüfen, ob es noch genug Tasks gibt (evtl. gar nicht nötig)
        # TODO: Macht es Sinn, Errors in die result.json reinzuschreiben?
        # print(multiprocessing.cpu_count())

        dataset_results = []
        run_result = CPDFullResult(list(map(lambda x: x.get_task_name(), tasks['datasets'])),
                                   list(map(lambda x: x.get_task_name(), tasks['algorithms'])),
                                   list(map(lambda x: x.get_task_name(), tasks['metrics'])))

        with ProcessPoolExecutor(max_workers=None) as executor:
            for dataset in tasks["datasets"]:
                dataset_results.append(executor.submit(create_ds_executor_and_run,
                                                       dataset,
                                                       tasks["algorithms"],
                                                       tasks["metrics"]))
        for ds_res in dataset_results:
            try:
                res = ds_res.result()
                # res = ds_res.exception()
            except Exception as e:
                traceback.print_exc()
                # print(e)
            else:
                run_result.add_dataset_result(res)
        return run_result

    def _create_tasks(self, methods):
        task_objects = {
            "datasets": [],
            "algorithms": [],
            "metrics": []
        }
        for dataset_function in methods["datasets"]:
            self._logger.debug(f"Creating and validating dataset task "
                               f"for {Utils.get_name_of_function(dataset_function)}")
            task_object = TaskFactory.create_task(dataset_function, TaskType.DATASET_FETCH)
            try:
                task_object.validate_task()
            except ValidationException as e:
                self._logger.exception(e)
            else:
                self._logger.debug(f'Validating {Utils.get_name_of_function(dataset_function)} has succeeded')
                task_objects["datasets"].append(task_object)

        for algorithm_function in methods["algorithms"]:
            self._logger.debug(f"Creating and validating algorithm task "
                               f"for {Utils.get_name_of_function(algorithm_function)}")
            task_object = TaskFactory.create_task(algorithm_function, TaskType.ALGORITHM_EXECUTION)
            try:
                task_object.validate_task()
            except ValidationException as e:
                self._logger.exception(e)
            else:
                self._logger.debug(f'Validating {Utils.get_name_of_function(algorithm_function)} has succeeded')
                task_objects["algorithms"].append(task_object)

        for metric_function in methods["metrics"]:
            self._logger.debug(f"Creating and validating metric task "
                               f"for {Utils.get_name_of_function(metric_function)}")
            task_object = TaskFactory.create_task(metric_function, TaskType.METRIC_EXECUTION)
            try:
                task_object.validate_task()
            except ValidationException as e:
                self._logger.exception(e)
            else:
                self._logger.debug(f'Validating {Utils.get_name_of_function(metric_function)} has succeeded')
                task_objects["metrics"].append(task_object)
        return task_objects


class DatasetExecutor:
    def __init__(self, dataset_task, algorithm_tasks, metric_tasks):
        self._result: CPDDatasetResult = None  # Created later
        self._dataset_task = dataset_task
        self._algorithm_tasks = algorithm_tasks
        self._metric_tasks = metric_tasks

    # self._logger = logger

    def execute(self):
        try:
            dataset = self._dataset_task.execute()
        except Exception as e:
            raise CPDDatasetCreationException(self._dataset_task.get_task_name()) from e
        self._result = CPDDatasetResult(self._dataset_task, dataset.get_length(), self._algorithm_tasks,
                                        self._metric_tasks)
        with ThreadPoolExecutor(max_workers=None) as executor:
            for i in range(0, dataset.get_length()):
                try:
                    part_dataset, ground_truth = dataset.get_signal(i)
                except Exception as e:
                    raise FeatureLoadingException(self._dataset_task.get_task_name(), i) from e
                for algorithm in self._algorithm_tasks:
                    executor.submit(self._execute_algorithm_and_metric, part_dataset,
                                    algorithm, ground_truth, i)
        return self._result

    def _execute_algorithm_and_metric(self, dataset, algorithm, ground_truth, feature):
        indexes, scores = algorithm.execute(dataset)
        self._result.add_algorithm_result(indexes, scores, feature, algorithm.get_task_name())
        with ThreadPoolExecutor(max_workers=None) as executor:
            for metric in self._metric_tasks:
                executor.submit(self._calculate_metric, indexes, scores,
                                metric, ground_truth, feature, algorithm)

    def _calculate_metric(self, indexes, scores, metric_task, ground_truth, feature, algorithm):
        metric_result = metric_task.execute(indexes, scores, ground_truth)
        self._result.add_metric_score(metric_result, feature, algorithm.get_task_name(), metric_task.get_task_name())

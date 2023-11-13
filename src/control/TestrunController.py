import concurrent
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

from control.CPDDatasetResult import CPDDatasetResult
from control.CPDFullResult import CPDFullResult
from control.ExecutionController import ExecutionController
from task.Task import TaskType
from task.TaskFactory import TaskFactory


def create_ds_executor_and_run(dataset, algorithms, metrics):
    ds_executor = DatasetExecutor(dataset, algorithms, metrics)
    return ds_executor.execute()


class TestrunController(ExecutionController):

    def execute_run(self, methods: dict) -> any:
        tasks = self._create_tasks(methods)
        # print(multiprocessing.cpu_count())

        dataset_results = []
        run_result = CPDFullResult()

        with ProcessPoolExecutor(max_workers=None) as executor:
            for dataset in tasks["datasets"]:
                dataset_results.append(executor.submit(create_ds_executor_and_run,
                                                       dataset,
                                                       tasks["algorithms"],
                                                       tasks["metrics"]))
        for ds_res in dataset_results:
            run_result.add_dataset_result(ds_res.result())
        return run_result

    def _create_tasks(self, methods):
        task_objects = {
            "datasets": [],
            "algorithms": [],
            "metrics": []
        }
        for dataset_function in methods["datasets"]:
            task_object = TaskFactory.create_task(dataset_function, TaskType.DATASET_FETCH)
            task_object.validate_task()
            # TODO: Proper Validation incl. exception catching
            task_objects["datasets"].append(task_object)
        for algorithm_function in methods["algorithms"]:
            task_object = TaskFactory.create_task(algorithm_function, TaskType.ALGORITHM_EXECUTION)
            task_object.validate_task()
            # TODO: Proper Validation incl. exception catching
            task_objects["algorithms"].append(task_object)
        for metric_function in methods["metrics"]:
            task_object = TaskFactory.create_task(metric_function, TaskType.METRIC_EXECUTION)
            task_object.validate_task()
            # TODO: Proper Validation incl. exception catching
            task_objects["metrics"].append(task_object)
        return task_objects


class DatasetExecutor:
    def __init__(self, dataset_task, algorithm_tasks, metric_tasks):
        self._result: CPDDatasetResult = None  # Created later
        self._dataset_task = dataset_task
        self._algorithm_tasks = algorithm_tasks
        self._metric_tasks = metric_tasks

    def execute(self):
        dataset = self._dataset_task.execute()
        self._result = CPDDatasetResult(self._dataset_task, dataset.get_length(), self._algorithm_tasks,
                                        self._metric_tasks)
        with ThreadPoolExecutor(max_workers=None) as executor:
            for i in range(0, dataset.get_length()):
                part_dataset, ground_truth = dataset.get_signal(i)
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

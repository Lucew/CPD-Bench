import concurrent
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

from control.ExecutionController import ExecutionController
from task.Task import TaskType
from task.TaskFactory import TaskFactory


class TestrunController(ExecutionController):

    def execute_run(self, methods: dict) -> None:
        # 1. Create tasks and validate them
        tasks = self._create_tasks(methods)

        with ProcessPoolExecutor(max_workers=None) as executor:
            for dataset in tasks["datasets"]:
                executor.submit(self._execute_for_dataset, dataset,
                                {k: methods[k] for k in ("algorithms", "metrics")})

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

    def _execute_for_dataset(self, dataset_task, algorithms_and_metrics):
        dataset = dataset_task.execute()
        with ThreadPoolExecutor(max_workers=None) as executor:
            for i in range(0, dataset.get_length()):
                part_dataset = dataset.get_signal(i)
                for algorithm in algorithms_and_metrics["algorithms"]:
                    executor.submit(self._execute_algorithm_and_metric, part_dataset,
                                    algorithm, algorithms_and_metrics["metrics"])

    def _execute_algorithm_and_metric(self, dataset, algorithm, metrics):
        algorithm_result = algorithm.execute(dataset)
        with ThreadPoolExecutor(max_workers=None) as executor:
            for metric in metrics:
                executor.submit(self._calculate_metric, algorithm_result,
                                metric)

    def _calculate_metric(self, algorithm_result, metric_task):
        metric_result = metric_task.execute(algorithm_result)
        print(metric_result)

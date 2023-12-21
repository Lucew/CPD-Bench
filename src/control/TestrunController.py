import logging
import logging.handlers
import multiprocessing
import threading
from concurrent.futures import ProcessPoolExecutor

from control.CPDFullResult import CPDFullResult
from control.DatasetExecutor import DatasetExecutor
from control.ExecutionController import ExecutionController
from exception.ValidationException import ValidationException
from task.Task import TaskType
from task.TaskFactory import TaskFactory
from utils import Logger
from utils import Utils


# Quelle Multiprocessing Logging: https://docs.python.org/3/howto/logging-cookbook.html#logging-to-a-single-file-from-multiple-processes
def logger_thread(queue, logger):
    while True:
        record = queue.get()
        if record is None:
            break
        logger.handle(record)


def create_ds_executor_and_run(dataset, algorithms, metrics, queue):
    logger_name = 'cpdbench.' + dataset.get_task_name()
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.handlers.QueueHandler(queue))

    ds_executor = DatasetExecutor(dataset, algorithms, metrics, logger)
    try:
        return ds_executor.execute()
    except Exception as e:
        logger.exception(e)
        raise e


class TestrunController(ExecutionController):

    def __init__(self):
        self._logger = Logger.get_application_logger()

    def execute_run(self, methods: dict) -> any:
        self._logger.info('Creating tasks...')
        tasks = self._create_tasks(methods)
        self._logger.info(f"{len(tasks['datasets']) + len(tasks['algorithms']) + len(tasks['metrics'])} tasks created")
        # TODO: Prüfen, ob es noch genug Tasks gibt (evtl. gar nicht nötig)
        # print(multiprocessing.cpu_count())

        dataset_results = []
        run_result = CPDFullResult(list(map(lambda x: x.get_task_name(), tasks['datasets'])),
                                   list(map(lambda x: x.get_task_name(), tasks['algorithms'])),
                                   list(map(lambda x: x.get_task_name(), tasks['metrics'])))
        q = multiprocessing.Manager().Queue()
        logging_thread = threading.Thread(target=logger_thread, args=(q, self._logger))
        logging_thread.start()

        with ProcessPoolExecutor(max_workers=None) as executor:
            for dataset in tasks["datasets"]:
                dataset_results.append(executor.submit(create_ds_executor_and_run,
                                                       dataset,
                                                       tasks["algorithms"],
                                                       tasks["metrics"], q))
        for ds_res in dataset_results:
            try:
                res = ds_res.result()
            except Exception:
                pass # TODO: better handling
            else:
                run_result.add_dataset_result(res)
        q.put_nowait(None)
        logging_thread.join()
        self._logger.info("Collected all datasets")
        self._logger.info("Finished testrun. Printing results")
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




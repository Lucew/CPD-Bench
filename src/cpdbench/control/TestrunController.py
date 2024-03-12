import logging
import logging.handlers
import multiprocessing
import threading
from concurrent.futures import ProcessPoolExecutor

from cpdbench.control.CPDFullResult import CPDFullResult
from cpdbench.control.CPDResult import CPDResult
from cpdbench.control.DatasetExecutor import DatasetExecutor
from cpdbench.control.ExecutionController import ExecutionController
from cpdbench.utils import Logger, BenchConfig
from tqdm import tqdm


def _logger_thread(queue, logger):
    while True:
        record = queue.get()
        if record is None:
            break
        logger.handle(record)


def _create_ds_executor_and_run(dataset, algorithms, metrics, queue):
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
    """An ExecutionController implementation for the standard run configuration.
    As described in the paper, all given datasets, algorithms and metrics are
    completely executed and all results are stored in a CPDFullResult.
    """

    def __init__(self):
        self._logger = Logger.get_application_logger()
        super().__init__(self._logger)

    def execute_run(self, methods: dict) -> CPDResult:
        self._logger.info('Creating tasks...')
        tasks = self._create_tasks(methods)
        self._logger.info(f"{len(tasks['datasets']) + len(tasks['algorithms']) + len(tasks['metrics'])} tasks created")

        dataset_results = []
        run_result = CPDFullResult(list(map(lambda x: x.get_task_name(), tasks['datasets'])),
                                   list(map(lambda x: x.get_task_name(), tasks['algorithms'])),
                                   list(map(lambda x: x.get_task_name(), tasks['metrics'])))
        q = multiprocessing.Manager().Queue()
        error_list = []
        logging_thread = threading.Thread(target=_logger_thread, args=(q, self._logger))
        logging_thread.start()

        max_workers = None if BenchConfig.multiprocessing_enabled else 1
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            for dataset in tasks["datasets"]:
                dataset_results.append(executor.submit(_create_ds_executor_and_run,
                                                       dataset,
                                                       tasks["algorithms"],
                                                       tasks["metrics"], q))
            for i in tqdm(range(len(dataset_results)), desc="Processing datasets"):
                j = 0
                while True:
                    ds_res = dataset_results[j]
                    try:
                        res = ds_res.result(2)
                    except Exception as e:
                        if e is TimeoutError:
                            error_list.append(e)
                            dataset_results.pop(j)
                            i += 1
                            break
                    else:
                        run_result.add_dataset_result(res)
                        dataset_results.pop(j)
                        i += 1
                        break
                    j += 1
                    if j == len(dataset_results):
                        j = 0

        q.put_nowait(None)
        logging_thread.join()
        for error in error_list:
            self._logger.exception(error)
        self._logger.info("Collected all datasets")
        self._logger.info("Finished testrun. Printing results")
        return run_result

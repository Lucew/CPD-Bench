from cpdbench.control.CPDResult import CPDResult
from cpdbench.control.CPDValidationResult import CPDValidationResult
from cpdbench.control.ExecutionController import ExecutionController
from cpdbench.exception.ValidationException import DatasetValidationException, AlgorithmValidationException, \
    MetricValidationException
from cpdbench.utils import Logger


class ValidationRunController(ExecutionController):
    """A run configuration for validation runs.
    These runs only execute algorithms with a (user defined) subset of the datasets,
    and do not return the complete result sets.
    """

    def __init__(self):
        self._logger = Logger.get_application_logger()
        super().__init__(self._logger)

    def execute_run(self, methods: dict) -> CPDResult:
        self._logger.info('Creating tasks...')
        tasks = self._create_tasks(methods)
        self._logger.info(f"{len(tasks['datasets']) + len(tasks['algorithms']) + len(tasks['metrics'])} tasks created")

        exception_list = []

        self._logger.info('Begin validation')
        for ds_task in tasks['datasets']:
            try:
                self._logger.debug(f"Validating {ds_task.get_task_name()}")
                dataset = ds_task.validate_input()
            except DatasetValidationException as e:
                self._logger.debug(f"Error occurred when running {ds_task.get_task_name()}")
                exception_list.append(e)
                continue
            self._logger.debug(f"Validated {ds_task.get_task_name()} without error")
            data, ground_truth = dataset.get_validation_preview()
            for algo_task in tasks['algorithms']:
                try:
                    self._logger.debug(f"Validating {algo_task.get_task_name()}")
                    indexes, scores = algo_task.validate_input(data)
                except AlgorithmValidationException as e:
                    self._logger.debug(f"Error occurred when running {algo_task.get_task_name()}")
                    exception_list.append(e)
                    continue
                self._logger.debug(f"Validated {algo_task.get_task_name()} without error")
                for metric_task in tasks['metrics']:
                    try:
                        self._logger.debug(f"Validating {metric_task.get_task_name()}")
                        metric_task.validate_input(indexes, scores, ground_truth)
                    except MetricValidationException as e:
                        self._logger.debug(f"Error occurred when running {metric_task.get_task_name()}")
                        exception_list.append(e)
                        continue
                    self._logger.debug(f"Validated {metric_task.get_task_name()} without error")
        self._logger.info('Finished validation')
        self._logger.info(f'{len(exception_list)} errors occurred')
        validation_result = CPDValidationResult(exception_list,
                                                list(map(lambda x: x.get_task_name(), tasks['datasets'])),
                                                list(map(lambda x: x.get_task_name(), tasks['algorithms'])),
                                                list(map(lambda x: x.get_task_name(), tasks['metrics'])))
        for i in range(0, len(exception_list)):
            self._logger.info(f"Error {i}")
            self._logger.exception(exception_list[i], exc_info=exception_list[i])
        return validation_result

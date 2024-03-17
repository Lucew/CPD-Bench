"""
The global configuration Singleton module.
Contains all configurable parameters for the bench and functions
to read a given config.yml file.

To be used correctly the function load_config(config_file) has to be called first.
After this the other functions can be used.
"""

import yaml
import logging

from cpdbench.exception.ConfigurationException import ConfigurationFileNotFoundException, ConfigurationException
from cpdbench.exception.ValidationException import UserConfigValidationException
from cpdbench.utils import Logger
from cpdbench.utils.UserConfig import UserConfig

_complete_config = None

# LOGGING
logging_file_name: str = 'cpdbench-log.txt'
logging_level: int = logging.INFO
logging_console_level: int = logging.ERROR

# MULTIPROCESSING
multiprocessing_enabled = True

# RESULT
result_file_name: str = 'cpdbench-result.json'

# USER PARAMETERS
_user_config = None

_config_error_list = []


def get_user_config() -> UserConfig:
    """Returns the UserConfig object if the BenchConfig was already initialized.
    :return the UserConfig object
    """
    return _user_config


def get_complete_config() -> dict:
    """Returns the complete bench configuration including the user config as python dict.
    :return the config as dict
    """
    return {
        'logging': {
            'logging_file_name': logging_file_name,
            'logging_level': logging_level,
            'logging_console_level': logging_console_level
        },
        'multiprocessing': {
            'multiprocessing_enabled': multiprocessing_enabled
        },
        'result': {
            'result_file_name': result_file_name
        },
        'user_config': _user_config.get_param_dict()
    }


def load_config(config_file='config.yml') -> bool:
    """Initializes the BenchConfig object with the given config.yml file.
    If the config_file param is None or the file does not exist, the bench will use the default parameters and this
    function returns false.
    :param config_file: The path to the config file
    :return: True if the config could be loaded correctly, false otherwise.
    """
    global _complete_config
    global _user_config
    if config_file is None:
        _user_config = UserConfig()
        _throw_config_errors()
        return False
    _complete_config = _load_config_from_file(config_file)
    if _complete_config is None:
        _user_config = UserConfig()
        _throw_config_errors()
        return False

    # logging
    _load_logging_config(_complete_config.get('logging'))

    # multiprocessing enabled
    global multiprocessing_enabled
    multiprocessing_enabled = False if str(_complete_config.get('multiprocessing')).upper() == 'FALSE' else True

    # result
    global result_file_name
    result = _complete_config.get('result')
    if result is not None:
        res_filename = result.get('filename')
        if res_filename is not None:
            result_file_name = res_filename

    # user variables
    _user_config = UserConfig(_complete_config.get('user'))
    try:
        _user_config.validate_user_config()
    except Exception as e:
        raise UserConfigValidationException(str(e))

    _throw_config_errors()

    return True


def _load_logging_config(logging_config: dict) -> None:
    if logging_config is None:
        return
    # filename
    global logging_file_name
    filename = logging_config.get('filename')
    if filename is not None:
        logging_file_name = filename

    # log-level
    global logging_level
    logging_level = _get_log_level(logging_config, 'log-level')

    # log-level console
    global logging_console_level
    logging_console_level = _get_log_level(logging_config, 'log-level-console')


def _get_log_level(config, param_name):
    if config.get(param_name) is None:
        return logging.INFO
    if config[param_name].upper() == 'DEBUG':
        return logging.DEBUG
    elif config[param_name].upper() == 'INFO':
        return logging.INFO
    elif config[param_name].upper() == 'WARNING' or config[param_name].upper() == "WARN":
        return logging.WARNING
    elif config[param_name].upper() == 'ERROR':
        return logging.ERROR
    elif config[param_name].upper() == 'CRITICAL':
        return logging.CRITICAL
    else:
        _add_config_error(ConfigurationException(param_name))
        return logging.INFO


def _load_config_from_file(config_file: str):
    try:
        with open(config_file, 'r') as config_file_stream:
            yaml_config = yaml.safe_load(config_file_stream)
    except OSError:
        _add_config_error(ConfigurationFileNotFoundException(config_file))
        return None
    else:
        return yaml_config


def _add_config_error(exc: Exception) -> None:
    _config_error_list.append(exc)


def _throw_config_errors() -> None:
    logger = Logger.get_application_logger()
    for exc in _config_error_list:
        logger.warning(exc)

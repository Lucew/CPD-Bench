import yaml
import logging

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


def get_user_config():
    return _user_config


def get_complete_config():
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
    global _complete_config
    _complete_config = _load_config_from_file(config_file)
    if _complete_config is None:
        return False

    # logging
    _load_logging_config(_complete_config['logging'])

    # multiprocessing enabled
    global multiprocessing_enabled
    multiprocessing_enabled = False if str(_complete_config['multiprocessing']).upper() == 'FALSE' else True

    # result
    global result_file_name
    result_file_name = _complete_config['result']['filename'] if _complete_config['result']['filename'] is not None \
        else 'cpdbench-result.json'

    # user variables
    global _user_config
    _user_config = UserConfig(_complete_config['user'])

    return True


def _load_logging_config(logging_config: dict) -> None:
    # filename
    global logging_file_name
    logging_file_name = logging_config['filename']

    # log-level
    global logging_level
    logging_level = _get_log_level(logging_config, 'log-level')

    # log-level console
    global logging_console_level
    logging_console_level = _get_log_level(logging_config, 'log-level-console')


def _get_log_level(config, param_name):
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
        return logging.INFO


def _load_config_from_file(config_file: str):
    try:
        with open(config_file, 'r') as config_file_stream:
            yaml_config = yaml.safe_load(config_file_stream)
    except OSError:
        return None
    else:
        return yaml_config

# TODO: Teste:
# - keine Config-Datei
# - einzelne Werte fehlen

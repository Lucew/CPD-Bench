import yaml
import logging

from cpdbench.utils.UserConfig import UserConfig

# Konfigurierbar:
# Welches Log-Level wird gedruckt?
# Multiprocessing ein/aus

# LOGGING
logging_file_name: str = 'cpdbench-log.txt'
logging_level: int = logging.INFO
logging_console_level: int = logging.ERROR

# MULTIPROCESSING
multiprocessing_enabled = True

# USER PARAMETERS
_user_config = None


def get_user_config():
    return _user_config


def load_config(config_file='config.yml') -> bool:
    yaml_config = _load_config_from_file(config_file)
    if yaml_config is None:
        return False

    _load_logging_config(yaml_config['logging'])

    # multiprocessing enabled
    global multiprocessing_enabled
    multiprocessing_enabled = False if yaml_config['multiprocessing'].upper() == 'FALSE' else True

    global _user_config
    _user_config = UserConfig(yaml_config['user'])

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

# RUNTIME VARIABLES
# Ansätze:
# 1. Pro Task: optional Config-Parameter => über definierte Schnittstelle abrufen von Param
# 2. keyword-Parameter nutzen

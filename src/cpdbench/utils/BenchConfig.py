import yaml
import logging

# TODO: Ok, hier PyYaml zu importieren? Oder eigene Lib schreiben?
# TODO: Singleton einfach als Modul umgesetzt, ok?

# Konfigurierbar:
# Welches Log-Level wird gedruckt?
# Multiprocessing ein/aus

# LOGGING
logging_file_name: str = 'cpdbench-log.txt'
logging_level: int = logging.INFO


def load_config(config_file='config.yml') -> bool:
    yaml_config = _load_config_from_file(config_file)
    if yaml_config is None:
        return False
    _load_logging_config(yaml_config['logging'])
    return True


def _load_logging_config(logging_config: dict) -> None:
    # filename
    global logging_file_name
    logging_file_name = logging_config['filename']

    # log-level
    global logging_level
    # TODO: Groß- und Kleinschreibung egal
    if logging_config['log-level'] == 'DEBUG':
        logging_level = logging.DEBUG
    elif logging_config['log-level'] == 'INFO':
        logging_level = logging.INFO
    elif logging_config['log-level'] == 'WARNING' or logging_config['log-level'] == "WARN":
        logging_level = logging.WARNING
    elif logging_config['log-level'] == 'ERROR':
        logging_level = logging.ERROR
    elif logging_config['log-level'] == 'CRITICAL':
        logging_level = logging.CRITICAL
    else:
        # TODO: Warning wenn dieser Fall eintritt
        logging_level = logging.INFO


def _load_config_from_file(config_file: str):
    try:
        with open(config_file, 'r') as config_file_stream:
            yaml_config = yaml.safe_load(config_file_stream)
    except OSError:
        return None
    else:
        return yaml_config

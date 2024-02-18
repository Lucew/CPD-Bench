# Was wird geloggt?
# DEBUG
# alle Schritte => Methoden-Signaturen, Erstellung von Tasks, Beginnen/Ende von Validierungen, Task-Erstellungen,
# INFO
# Start und Ende von Verarbeitungen => Testrun, Task-Ausführungen + Performance
# WARNING
# (evtl. unterdrückte Validation-Fehler)?
# ERROR
# Exceptions in Tasks, Validation-Fehler
# CRITICAL
# Exceptions, die die Testbench beendet haben


# Logging-Mechanismus
# - nicht auf root => https://docs.python.org/3/howto/logging.html#logging-levels
# - z.B. tcpd-bench:testrun-name:dataset-fetch
# - In File => Exceptions/Crits auf Konsole

# STDOUT + cpdbench-result.json => Result-JSON
# cpdbench-log.txt => alle Log-Messages
# STDERR => ERROR + CRITICAL

import logging
from cpdbench.utils import BenchConfig

_app_logger = None


def init_logger():
    global _app_logger
    _app_logger = logging.Logger('cpdbench')
    _app_logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    general_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(general_formatter)
    console_handler.setLevel(BenchConfig.logging_console_level)
    _app_logger.addHandler(console_handler)

   # open('cpdbench-log.txt', 'w').close()
    file_handler = logging.FileHandler(BenchConfig.logging_file_name, 'w')
    file_handler.setFormatter(general_formatter)
    file_handler.setLevel(BenchConfig.logging_level)
    _app_logger.addHandler(file_handler)
    return _app_logger


def get_application_logger() -> logging.Logger:
    if _app_logger is None:
        return init_logger()
    return _app_logger

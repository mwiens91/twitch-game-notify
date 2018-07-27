"""Stores constants for all modules."""

import logging


# Loglevel CLI options
CRITICAL = 'critical'
ERROR = 'error'
WARNING = 'warning'
INFO = 'info'
DEBUG = 'debug'

LOGLEVEL_CHOICES = [CRITICAL, ERROR, WARNING, INFO, DEBUG]
LOGLEVEL_DICT = {CRITICAL: logging.CRITICAL,
                 ERROR: logging.ERROR,
                 WARNING: logging.WARNING,
                 INFO: logging.INFO,
                 DEBUG: logging.DEBUG,}

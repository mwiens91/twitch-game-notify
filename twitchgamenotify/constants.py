"""Stores constants for all modules."""

import logging
import os


# Base of the repository/project
PROJECT_BASE_DIR = (
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Config file name
CONFIG_FILE_NAME = 'config.yaml'

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

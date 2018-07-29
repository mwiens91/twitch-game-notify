"""Stores constants for all modules."""

import logging
import os
from xdg import XDG_CONFIG_HOME


# Base of the repository/project
PROJECT_BASE_DIR = (
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Base of XDG config files
PROJECT_CONFIG_HOME = os.path.join(XDG_CONFIG_HOME, 'twitch-game-notify')

# Config file names
CONFIG_FILE_NAME = 'config.yaml'
CACHE_FILE_NAME = 'cache.json'

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

# Twitch base API URL
TWITCH_BASE_API_URL = 'https://api.twitch.tv/helix'

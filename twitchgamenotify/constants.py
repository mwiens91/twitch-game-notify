"""Stores constants for all modules."""

import logging
import os


# Base of the repository/project
PROJECT_BASE_DIR = (
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Base of XDG config files
try:
    PROJECT_CONFIG_HOME = os.path.join(
        os.environ['XDG_CONFIG_HOME'],
        'twitch-game-notify')
except KeyError:
    PROJECT_CONFIG_HOME = os.path.join(
        os.environ['HOME'],
        '.config/',
        'twitch-game-notify',)

# Config file names
CONFIG_FILE_NAME = 'config.yaml'
CACHE_FILE_NAME = 'cache.json'

# URL for example config file on Github
EXAMPLE_CONFIG_FILE_URL = 'https://raw.githubusercontent.com/mwiens91/twitch-game-notify/master/config.yaml.example'

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

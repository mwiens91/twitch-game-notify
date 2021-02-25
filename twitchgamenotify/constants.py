"""Stores constants for all modules."""

import logging
import os


# Base of the repository/project
PROJECT_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Path to example config file
EXAMPLE_CONFIG_FILE_PATH = os.path.join(
    PROJECT_BASE_DIR, "config.yaml.example"
)

# Path to the app indicator icon
APP_INDICATOR_SVG_PATH = os.path.join(
    PROJECT_BASE_DIR, "static/", "twitch.svg"
)


# Base of XDG config files
try:
    PROJECT_CONFIG_HOME = os.path.join(
        os.environ["XDG_CONFIG_HOME"], "twitch-game-notify"
    )
except KeyError:
    PROJECT_CONFIG_HOME = os.path.join(
        os.environ["HOME"], ".config/", "twitch-game-notify"
    )


# Config file names
CONFIG_FILE_NAME = "config.yaml"


# Loglevel CLI options
CRITICAL = "critical"
ERROR = "error"
WARNING = "warning"
INFO = "info"
DEBUG = "debug"

LOGLEVEL_CHOICES = [CRITICAL, ERROR, WARNING, INFO, DEBUG]
LOGLEVEL_DICT = {
    CRITICAL: logging.CRITICAL,
    ERROR: logging.ERROR,
    WARNING: logging.WARNING,
    INFO: logging.INFO,
    DEBUG: logging.DEBUG,
}


# Twitch API URLs
TWITCH_BASE_API_URL = "https://api.twitch.tv/helix"
TWITCH_STREAM_API_URL = TWITCH_BASE_API_URL + "/streams"
TWITCH_TOKEN_API_URL = "https://id.twitch.tv/oauth2/token"


# HTTP status codes
HTTP_200_OK = 200
HTTP_400_BAD_REQUEST = 400
HTTP_401_UNAUTHORIZED = 401
HTTP_502_BAD_GATEWAY = 502

"""Stores constants for all modules."""

import logging
import os


# Base of the repository/project
PROJECT_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


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
CACHE_FILE_NAME = "cache.json"
CACHE_FILE_LOCK_NAME = CACHE_FILE_NAME + ".lock"


# URL for example config file on Github
EXAMPLE_CONFIG_FILE_URL = "https://raw.githubusercontent.com/mwiens91/twitch-game-notify/master/config.yaml.example"


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
TWITCH_USER_API_URL = TWITCH_BASE_API_URL + "/users"
TWITCH_GAME_API_URL = TWITCH_BASE_API_URL + "/games"
TWITCH_TOKEN_API_URL = "https://id.twitch.tv/oauth2/token"


# HTTP status codes
HTTP_200_OK = 200
HTTP_401_UNAUTHORIZED = 401

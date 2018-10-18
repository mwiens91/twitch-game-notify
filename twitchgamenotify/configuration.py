"""Contains configuration related functions."""

import argparse
import os.path
import sys
import requests
import yaml
from twitchgamenotify.cache import unlock_cache
from twitchgamenotify.constants import (
    CONFIG_FILE_NAME,
    EXAMPLE_CONFIG_FILE_URL,
    LOGLEVEL_CHOICES,
    LOGLEVEL_DICT,
    PROJECT_BASE_DIR,
    PROJECT_CONFIG_HOME,
    WARNING,
)
from twitchgamenotify.version import NAME, VERSION, DESCRIPTION


class ConfigFileNotFound(Exception):
    """Raised when a config file can't be found."""

    pass


class PrintExampleConfigAction(argparse.Action):
    """argparse action to print example config file."""

    def __call__(self, parser, namespace, values, option_string=None):
        """Download and print example config file."""
        r = requests.get(EXAMPLE_CONFIG_FILE_URL)

        if r.status_code != 200:
            print(
                "ERROR: Failed to download example config file!",
                file=sys.stderr,
            )
            sys.exit(1)
        else:
            print(r.content.decode())
            sys.exit(0)


class RemoveCacheLockAction(argparse.Action):
    """argparse action to remove cache lock (should one exist)."""

    def __call__(self, parser, namespace, values, option_string=None):
        """Remove the cache lock."""
        try:
            unlock_cache(catch_failure=False)
        except FileNotFoundError:
            print(
                "WARNING: No existing cache lock to remove!", file=sys.stderr
            )

        # Get out
        sys.exit(0)


class TranslateLogLevelAction(argparse.Action):
    """argparse action to translate loglevel to a number."""

    def __call__(self, parser, namespace, values, option_string=None):
        """Set a logging loglevel number."""
        setattr(namespace, self.dest, LOGLEVEL_DICT[values])


def find_config_file():
    """Find and return the path of a config file.

    The config file looked for is "config.yaml" and it is looked for at
    the base of the respository first (if you're running from source),
    and then in $XDG_CONFIG_HOME/twitch-game-notify/ (XDG_CONFIG_HOME
    defaults to $HOME/.config).

    Returns:
        A string containing the absolute path to the config file.

    Raises:
        ConfigFileNotFound: A config file couldn't be found.
    """
    # Check the base of the project
    config_path = os.path.join(PROJECT_BASE_DIR, CONFIG_FILE_NAME)

    if os.path.exists(config_path):
        return config_path

    # Check XDG_CONFIG_HOME
    config_path = os.path.join(PROJECT_CONFIG_HOME, CONFIG_FILE_NAME)

    if os.path.exists(config_path):
        return config_path

    # Couldn't find anything :thinking:
    raise ConfigFileNotFound


def parse_config_file():
    """Find and parse a config file."""
    # Find the config file first
    config_path = find_config_file()

    # Now parse and return it - note that PyYAML doesn't come with any
    # schema validation, which might be desirable at some point
    with open(config_path, "r") as config_file:
        return yaml.load(config_file)


def parse_runtime_args():
    """Parse runtime args using argparse.

    Returns:
        An object of type 'argparse.Namespace' containing the runtime
        arguments as attributes. See argparse documentation for more
        details.
    """
    parser = argparse.ArgumentParser(
        prog=NAME, description="%(prog)s - " + DESCRIPTION
    )
    parser.add_argument(
        "-l",
        "--loglevel",
        default=LOGLEVEL_DICT[WARNING],
        choices=LOGLEVEL_CHOICES,
        action=TranslateLogLevelAction,
        help="how much to log",
    )
    parser.add_argument(
        "--one-shot", action="store_true", help="query once then exit"
    )
    parser.add_argument(
        "--no-app-indicator",
        action="store_true",
        help="don't launch an app indicator",
    )
    parser.add_argument(
        "--no-caching", action="store_true", help="don't cache static API data"
    )
    parser.add_argument(
        "--print-config",
        nargs=0,
        action=PrintExampleConfigAction,
        help="downloads and prints example config file",
    )
    parser.add_argument(
        "--print-to-terminal",
        action="store_true",
        help="print to terminal (doesn't connect to D-Bus)",
    )
    parser.add_argument(
        "--remove-cache-lock",
        nargs=0,
        action=RemoveCacheLockAction,
        help="removes a cache lock if one exists",
    )
    parser.add_argument(
        "--version", action="version", version="%(prog)s " + VERSION
    )

    return parser.parse_args()

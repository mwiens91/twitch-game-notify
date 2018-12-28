"""Functions for caching static API data.

For all of these functions, the cache is located at
$XDG_CONFIG_HOME/twitch-game-notify/cache.json, where XDG_CONFIG_HOME
defaults to $HOME/.config.
"""

import json
import os
from twitchgamenotify.constants import (
    CACHE_FILE_LOCK_NAME,
    CACHE_FILE_NAME,
    PROJECT_CONFIG_HOME,
)


def is_cache_locked():
    """Determines whether a cache is locked.

    Returns:
        A boolean signalling whether the cache is locked.
    """
    # Build the path to the cache lock
    cache_lock_path = os.path.join(PROJECT_CONFIG_HOME, CACHE_FILE_LOCK_NAME)

    return os.path.exists(cache_lock_path)


def lock_cache():
    """Creates a cache lock file."""
    # Build the path to the cache lock
    cache_lock_path = os.path.join(PROJECT_CONFIG_HOME, CACHE_FILE_LOCK_NAME)

    # Create an empty lock file
    open(cache_lock_path, "x")


def unlock_cache(catch_failure=True):
    """Removes a cache lock file.

    Arg:
        catch_failure: An optional boolean signalling whether to catch
            a FileNotFoundError exception occuring when the cache lock
            to remove doesn't exist.
    """
    # Build the path to the cache lock
    cache_lock_path = os.path.join(PROJECT_CONFIG_HOME, CACHE_FILE_LOCK_NAME)

    # Remove the lock
    if catch_failure:
        try:
            os.remove(cache_lock_path)
        except FileNotFoundError:
            pass
    else:
        os.remove(cache_lock_path)


def load_cache():
    """Loads a cache, or creates one if it doesn't exit.

    Returns:
        A dictionary containing static API data. For example:

        {"games": {"460630": "Tom Clancy's Rainbow Six: Siege",
                   "493057": "PLAYERUNKNOWN'S BATTLEGROUNDS"},
         "streamers": {"macie_jay": "Macie_Jay",
                       "shroud": "shroud"}}
    """
    # Build the path to the cache JSON file
    cache_path = os.path.join(PROJECT_CONFIG_HOME, CACHE_FILE_NAME)

    # If a cache doesn't exist or if it's an empty file (maybe it got
    # corrupted at some point?), return an empty dictionary as the new
    # cache
    if not os.path.exists(cache_path) or not os.stat(cache_path).st_size:
        return {"games": {}, "streamers": {}}

    # Load the cache file
    with open(cache_path, "r") as cache_file:
        return json.load(cache_file)


def save_cache(cache_dictionary):
    """Saves a cache as JSON.

    Arg:
        cache_dictionary: A dictionary containing cache information to
            be serialized to JSON.
    """
    # Get the path for the cache
    cache_path = os.path.join(PROJECT_CONFIG_HOME, CACHE_FILE_NAME)

    # Make sure the directory paths to the cache file exist
    os.makedirs(PROJECT_CONFIG_HOME, exist_ok=True)

    with open(cache_path, "w") as cache_file:
        cache_file.write(
            json.dumps(cache_dictionary, indent=2, sort_keys=True)
        )

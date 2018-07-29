"""Functions for caching static API data."""

import json
import os
from twitchgamenotify.constants import (
    CACHE_FILE_NAME,
    PROJECT_CONFIG_HOME,)


def load_cache():
    """Loads a cache, or creates one if it doesn't exit.

    The cache is located at
    $XDG_CONFIG_HOME/twitch-game-notify/cache.json (XDG_CONFIG_HOME
    defaults to $HOME/.config).

    Returns:
        A dictionary containing static API data. For example:
    """
    # Build the path to the cache JSON file
    cache_path = os.path.join(PROJECT_CONFIG_HOME, CACHE_FILE_NAME)

    # If a cache doesn't exist, return an empty dictionary as the new
    # cache
    if not os.path.exists(cache_path):
        return {'games': {}, 'streamers': {}}

    # Load the cache file
    with open(cache_path, 'r') as cache_file:
        return json.load(cache_file)

def save_cache(cache_dictionary):
    """Saves a cache as JSON.

    The cache is located at
    $XDG_CONFIG_HOME/twitch-game-notify/cache.json (XDG_CONFIG_HOME
    defaults to $HOME/.config).

    Arg:
        cache_dictionary: A dictionary containing cache information to
            be serialized to JSON.
    """
    # Get the path for the cache
    cache_path = os.path.join(PROJECT_CONFIG_HOME, CACHE_FILE_NAME)

    # Make sure the directory paths to the cache file exist
    os.makedirs(PROJECT_CONFIG_HOME, exist_ok=True)

    with open(cache_path, 'w') as cache_file:
        cache_file.write(json.dumps(cache_dictionary))

"""Contains the main function."""

import atexit
import logging
import time
import threading
import sys
import notify2
from twitchgamenotify.cache import (
    load_cache,
    save_cache,)
from twitchgamenotify.configuration import (
    ConfigFileNotFound,
    parse_config_file,
    parse_runtime_args,)
from twitchgamenotify.notifications import process_notifications
from twitchgamenotify.twitch_api import (
    TwitchApi,)
from twitchgamenotify.version import NAME


def main():
    """The main function."""
    # Get runtime arguments
    cli_args = parse_runtime_args()

    # Set up logger
    logging.basicConfig(
        format='%(levelname)s: %(message)s',
        level=cli_args.loglevel,)

    # Load cached static API data
    if not cli_args.no_caching:
        # Load the cache
        cache_dict = load_cache()

        # Create a hook to save the cache when exiting the program
        atexit.register(save_cache, cache_dict)

    # Read config file
    try:
        config_dict = parse_config_file()
    except ConfigFileNotFound:
        logging.error("Config file not found. Aborting.")
        sys.exit(1)

    # Set up the notifier
    if not cli_args.print_to_terminal:
        notify2.init(NAME)

    # Connect to the API
    twitch_api = TwitchApi(config_dict['twitch-api-client-id'])

    # Query (and possibly notify) only once or periodically
    if cli_args.one_shot:
        process_notifications(
            print_to_terminal=cli_args.print_to_terminal,
            streamers=config_dict['streamers'],
            twitch_api=twitch_api,)
    else:
        # Save what game a streamer was playing last so we don't re-notify
        streamers_last_seen_playing_dict = (
            {streamer: "" for streamer in config_dict['streamers'].keys()})

        # Loop until we hit a keyboard interrupt
        try:
            while True:
                # Set up arguments to give process_notifcations
                kwargs = dict(
                    print_to_terminal=cli_args.print_to_terminal,
                    streamers=config_dict['streamers'],
                    streamers_previous_game=(
                        streamers_last_seen_playing_dict),
                    twitch_api=twitch_api,)

                if not cli_args.no_caching:
                    kwargs['names_cache'] = cache_dict

                # Process any notifications
                threading.Thread(
                    target=process_notifications,
                    kwargs=kwargs,).start()

                # Wait before querying again
                time.sleep(config_dict['query-period'])
        except KeyboardInterrupt:
            logging.info("Exitting %s", NAME)

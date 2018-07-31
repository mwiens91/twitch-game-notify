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

    # Set up app indicator and run it in a separate thread
    if not cli_args.one_shot or cli_args.no_app_indicator:
        # Import this here to GTK-incompatible machines are still
        # supported
        from twitchgamenotify.app_indicator import AppIndicator

        indicator = AppIndicator()

        # Kill the indicator when we quit
        atexit.register(indicator.stop)

        # Start the indicator in its own thread
        threading.Thread(target=indicator.start, daemon=True).start()

    # Connect to the API
    twitch_api = TwitchApi(
        client_id=config_dict['twitch-api-client-id'],
        client_secret=config_dict['twitch-api-client-secret'],)

    # Set up arguments to give process_notifcations
    kwargs = dict(
        print_to_terminal=cli_args.print_to_terminal,
        streamers=config_dict['streamers'],
        twitch_api=twitch_api,)

    if not cli_args.no_caching:
        kwargs['names_cache'] = cache_dict

    if not cli_args.one_shot:
        # Remember what game a streamer was playing last so we don't
        # re-notify
        streamers_last_seen_playing_dict = (
            {streamer: "" for streamer in config_dict['streamers'].keys()})

        kwargs['streamers_previous_game'] = streamers_last_seen_playing_dict

    # Query (and possibly notify) only once or periodically
    if cli_args.one_shot:
        process_notifications(**kwargs)
    else:
        # Loop until we hit a keyboard interrupt
        try:
            while True:
                # Process any notifications
                threading.Thread(
                    target=process_notifications,
                    kwargs=kwargs,).start()

                # Wait before querying again
                time.sleep(config_dict['query-period'])
        except KeyboardInterrupt:
            logging.info("Exitting %s", NAME)

"""Contains the main function."""

import atexit
import logging
import time
import threading
import signal
import sys
import notify2
import requests
from twitchgamenotify.cache import (
    is_cache_locked,
    load_cache,
    lock_cache,
    unlock_cache,
    save_cache,
)
from twitchgamenotify.configuration import (
    ConfigFileNotFound,
    parse_config_file,
    parse_runtime_args,
)
from twitchgamenotify.notifications import (
    process_notifications_wrapper,
    send_connection_error_notification,
)
from twitchgamenotify.twitch_api import TwitchApi
from twitchgamenotify.version import NAME


def graceful_exit(*_, **__):
    """Exit such that atexit gets triggered."""
    logging.info("Exitting %s", NAME)
    sys.exit(0)


def main():
    """The main function."""
    # Get runtime arguments
    cli_args = parse_runtime_args()

    # Set up logger
    logging.basicConfig(
        format="%(levelname)s: %(message)s", level=cli_args.loglevel
    )

    # Make sure process kills and poweroffs cause atexit registers to
    # trigger
    signal.signal(signal.SIGTERM, graceful_exit)
    signal.signal(signal.SIGINT, graceful_exit)

    # Load cached static API data
    if not cli_args.no_caching:
        # Load the cache
        cache_dict = load_cache()

        if is_cache_locked():
            # Another process has claimed the cache
            logging.warning(
                "Cache file is locked. All static API data "
                "collected during this run will be discarded."
            )
        else:
            # Claim ownership of the cache
            lock_cache()

            # Create a hook to save and unlock the cache when exiting
            # the program
            atexit.register(unlock_cache)
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
    if (
        not cli_args.one_shot
        or not cli_args.print_to_terminal
        or cli_args.no_app_indicator
    ):
        # Import this here so GTK-incompatible machines are still
        # supported
        from twitchgamenotify.app_indicator import AppIndicator

        indicator = AppIndicator()

        # Kill the indicator when we quit
        atexit.register(indicator.stop)

        # Start the indicator in its own thread
        threading.Thread(target=indicator.start, daemon=True).start()

    # Connect to the API - keep retrying and be loud if there's a
    # connection error
    retry_attempt = 0

    while True:
        try:
            twitch_api = TwitchApi(
                client_id=config_dict["twitch-api-client-id"],
                client_secret=config_dict["twitch-api-client-secret"],
            )

            # Successful connection; reset retry attempts
            if retry_attempt:
                retry_attempt = 0

            break
        except requests.exceptions.ConnectionError:
            # Internet is probably down. Log an error and notify if we're
            # notifying
            retry_attempt += 1
            sleep_delta = 2 ** retry_attempt

            send_connection_error_notification(
                send_dbus_notification=not cli_args.print_to_terminal,
                retry_seconds=sleep_delta,
            )

            # Wait a bit before retrying
            time.sleep(sleep_delta)

    # Set up arguments to give process_notifcations
    kwargs = dict(
        print_to_terminal=cli_args.print_to_terminal,
        streamers=config_dict["streamers"],
        twitch_api=twitch_api,
    )

    if not cli_args.no_caching:
        kwargs["names_cache"] = cache_dict

    if not cli_args.one_shot:
        # Remember what game a streamer was playing last so we don't
        # re-notify
        streamers_last_seen_playing_dict = {
            streamer: "" for streamer in config_dict["streamers"].keys()
        }

        kwargs["streamers_previous_game"] = streamers_last_seen_playing_dict

    # Query (and possibly notify) only once or periodically
    if cli_args.one_shot:
        process_notifications_wrapper(**kwargs)
    else:
        # Loop until we get interrupted
        while True:
            # Process any notifications
            threading.Thread(
                target=process_notifications_wrapper,
                kwargs=kwargs,
                daemon=True,
            ).start()

            # Wait before querying again
            time.sleep(config_dict["query-period"])

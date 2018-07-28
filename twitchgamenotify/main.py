"""Contains the main function."""

import logging
import time
import threading
import sys
import notify2
from twitchgamenotify.configuration import (
    ConfigFileNotFound,
    parse_config_file,
    parse_runtime_args,)
from twitchgamenotify.twitch_api import (
    FailedHttpRequest,
    TwitchApi,)
from twitchgamenotify.version import NAME


def query_iteration(streamers, twitch_api, print_to_terminal=False):
    """Query the Twitch API once.

    Arg:
        print_to_terminal: A boolean signalling whether to print to the
            terminal instead of passing a message to D-Bus.
        streamers: A dictionary of streamers where the keys are strings
            containing the streamer's login name and the values are
            dictionaries containing the user's settings for the
            streamer.
        twitch_api: An authenticated TwitchApi object to interact with
            Twitch's API.
    """
    # TODO: test functionality - remove me!
    for streamer_login_name in streamers.keys():
        try:
            info = twitch_api.get_online_stream_info(streamer_login_name)

            msg = (streamer_login_name, info['title'],)

            if print_to_terminal:
                print("%s: %s" % msg)
            else:
                notify2.Notification(*msg).show()
        except FailedHttpRequest:
            # The sender of this exception has already logged an error.
            pass

def main():
    """The main function."""
    # Get runtime arguments
    cli_args = parse_runtime_args()

    # Set up logger
    logging.basicConfig(
        format='%(levelname)s: %(message)s',
        level=cli_args.loglevel,)

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

    # Initialize some sort of data structure to keep track of what
    # selected streamers are playing - maybe pickle this too?

    # Query (and possibly notify) periodically
    if cli_args.one_shot:
        query_iteration(
            print_to_terminal=cli_args.print_to_terminal,
            streamers=config_dict['streamers'],
            twitch_api=twitch_api,)
    else:
        try:
            while True:
                # Query
                query_iteration(
                    print_to_terminal=cli_args.print_to_terminal,
                    streamers=config_dict['streamers'],
                    twitch_api=twitch_api,)

                # Wait before querying again
                time.sleep(config_dict['query-period'])
        except KeyboardInterrupt:
            logging.info("Exitting %s", NAME)

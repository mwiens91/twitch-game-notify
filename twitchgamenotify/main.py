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
from twitchgamenotify.twitch_api import TwitchApi
from twitchgamenotify.version import NAME


def query_iteration(print_to_terminal=False):
    """Query the Twitch API once.

    Arg:
        print_to_terminal: A boolean signalling whether to print to the
            terminal instead of passing a message to D-Bus.
    """
    # TODO: debug message
    msg = ("HEY", "hola",)

    if print_to_terminal:
        print("%s: %s" % msg)
    else:
        notify2.Notification(*msg).show()

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
    # selected streamers are playing

    # Query (and possibly notify) periodically
    if cli_args.one_shot:
        query_iteration(print_to_terminal=cli_args.print_to_terminal)
    else:
        try:
            while True:
                # Query
                query_iteration(print_to_terminal=cli_args.print_to_terminal)

                # Wait before querying again
                time.sleep(config_dict['query-period'])
        except KeyboardInterrupt:
            logging.critical("Exitting %s", NAME)

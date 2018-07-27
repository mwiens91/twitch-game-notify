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
from twitchgamenotify.version import NAME


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

    # Loop every N seconds - find some way to exit gracefully
    # Inside loop call API a bunch

    # TODO: debug message
    if not cli_args.print_to_terminal:
        notify2.Notification("HEY", "HI").show()

"""Contains the main function."""

import time
import threading
import notify2
from twitchgamenotify.configuration import parse_runtime_args
from twitchgamenotify.version import NAME


def main():
    """The main function."""
    # Get runtime arguments
    cli_args = parse_runtime_args()

    # Read config file

    # Set up the notifier
    if not cli_args.print_to_terminal:
        notify2.init(NAME)

    # Loop every N seconds - find some way to exit gracefully
    # Inside loop call API a bunch

    # TODO: debug message
    if not cli_args.print_to_terminal:
        notify2.Notification("HEY", "HI").show()

"""Contains the main function."""

import time
import threading
import notify2
from twitchgamenotify.cli import parse_runtime_args
from twitchgamenotify.version import NAME


def main():
    """The main function."""
    # Set up the notifier
    notify2.init(NAME)

    # Get runtime arguments
    cli_args = parse_runtime_args()

    # Read config file

    # Loop every N seconds - find some way to exit gracefully
    # Inside loop call API a bunch

    # TODO: debug message
    notify2.Notification("HEY", "HI").show()

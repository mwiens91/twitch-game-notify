"""Contains CLI related functions."""

import argparse
from twitchgamenotify.version import NAME, VERSION, DESCRIPTION


def parse_runtime_args():
    """Parse runtime args using argparse.

    Returns:
        An object of type 'argparse.Namespace' containing the runtime
        arguments as attributes. See argparse documentation for more
        details.
    """
    parser = argparse.ArgumentParser(
        prog=NAME,
        description="%(prog)s - " + DESCRIPTION,)
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s " + VERSION)

    return parser.parse_args()

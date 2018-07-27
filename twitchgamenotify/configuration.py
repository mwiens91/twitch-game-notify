"""Contains configuration related functions."""

import argparse
from twitchgamenotify.constants import LOGLEVEL_CHOICES, LOGLEVEL_DICT, WARNING
from twitchgamenotify.version import NAME, VERSION, DESCRIPTION


class TranslateLogLevelAction(argparse.Action):
    """Sets the logging number given loglevel string."""
    def __call__(self, parser, namespace, values, option_string=None):
        """Set a logging loglevel number."""
        setattr(namespace, self.dest, LOGLEVEL_DICT[values])


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
        '-l', '--loglevel',
        default=LOGLEVEL_DICT[WARNING],
        choices=LOGLEVEL_CHOICES,
        action=TranslateLogLevelAction,
        help="how much to log",)
    parser.add_argument(
        '--print-to-terminal',
        action='store_true',
        help="print to terminal (doesn't connect to D-Bus)")
    parser.add_argument(
        '--version',
        action='version',
        version="%(prog)s " + VERSION)

    return parser.parse_args()

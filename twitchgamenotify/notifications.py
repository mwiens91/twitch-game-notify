"""Functions for processing and displaying notifications."""

import datetime
import notify2
from twitchgamenotify.twitch_api import FailedHttpRequest


# ANSI escape for bold
ANSI_BOLD = '\033[1m'
ANSI_END = '\033[0m'


def print_notification_to_terminal(streamer_name, stream_title, game_name):
    """Print a notification to the terminal.

    Args:
        streamer_name: A string containing the name of the streamer.
        stream_title: A string containing the title of the stream.
        game_name: A string containing the name of the game.
    """
    print(ANSI_BOLD + streamer_name + ANSI_END, end='')
    print(" @ " + datetime.datetime.now().isoformat())
    print("Title: %s" % stream_title)
    print("Playing: %s" % game_name)


def send_notification_to_dbus(streamer_name, stream_title, game_name):
    """Send a notification to D-Bus.

    Args:
        streamer_name: A string containing the name of the streamer.
        stream_title: A string containing the title of the stream.
        game_name: A string containing the name of the game.
    """
    notify2.Notification(
        streamer_name,
        "%s\nPlaying: %s" % (stream_title, game_name)).show()


def process_notifications(streamers, twitch_api, print_to_terminal=False):
    """Query the Twitch API for all streamers and display notications.

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
    # Look up info about each streamer's stream
    for streamer_login_name in streamers.keys():
        try:
            # Get info about stream
            info = twitch_api.get_online_stream_info(streamer_login_name)
        except FailedHttpRequest:
            # The sender of this exception has already logged an error.
            # On to the next streamer
            continue

        # If the stream isn't live, move on
        if not info['live']:
            continue

        # Gather info
        streamer_display_name = (
            twitch_api.get_streamer_display_name(streamer_login_name))
        stream_title = info['title']
        game_title = twitch_api.get_game_title(info['game_id'])

        # Send the notification
        if print_to_terminal:
            print_notification_to_terminal(
                streamer_display_name,
                stream_title,
                game_title,)
        else:
            send_notification_to_dbus(
                streamer_display_name,
                stream_title,
                game_title,)

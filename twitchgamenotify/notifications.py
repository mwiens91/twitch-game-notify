"""Functions for processing and displaying notifications."""

import datetime
import logging
import time
import notify2
import requests
from twitchgamenotify.constants import HTTP_502_BAD_GATEWAY
from twitchgamenotify.twitch_api import FailedHttpRequest
from twitchgamenotify.version import NAME


# ANSI escape sequence for bold text
ANSI_BOLD = "\033[1m"
ANSI_END = "\033[0m"


def print_notification_to_terminal(streamer_name, stream_title, game_name):
    """Print a game notification to the terminal.

    Args:
        streamer_name: A string containing the name of the streamer.
        stream_title: A string containing the title of the stream.
        game_name: A string containing the name of the game.
    """
    print(ANSI_BOLD + streamer_name + ANSI_END, end="")
    print(" @ " + datetime.datetime.now().isoformat())
    print("Streaming %s" % game_name)
    print("Title: %s" % stream_title)


def send_notification_to_dbus(streamer_name, stream_title, game_name):
    """Send a game notification to D-Bus.

    Args:
        streamer_name: A string containing the name of the streamer.
        stream_title: A string containing the title of the stream.
        game_name: A string containing the name of the game.
    """
    notify2.Notification(
        streamer_name + " @ " + time.strftime("%H:%M"),
        "Streaming %s\nTitle: %s" % (game_name, stream_title),
    ).show()


def send_error_notification(error_message, send_dbus_notification):
    """Logs and notifies an error message.

    Args:
        error_message: A string containing the error message
        send_dbus_notification: A boolean specifying whether to send a
            notification to D-Bus.
    """
    # Log the error
    logging.error(error_message)

    # Send a notification about the error, if instructed to
    if send_dbus_notification:
        notify2.Notification(
            NAME + " @ " + time.strftime("%H:%M"), error_message
        ).show()


def send_connection_error_notification(send_dbus_notification, retry_seconds):
    """Logs and notifies about a connection failure.

    Args:
        send_dbus_notification: A boolean specifying whether to send a
            notification to D-Bus.
        retry_seconds: A string containing the number of seconds before
            the next connection attempt.
    """
    # The message to show
    error_message = (
        "Unable to connect to Twitch. Retrying in %ss" % retry_seconds
    )

    # Show the message
    send_error_notification(error_message, send_dbus_notification)


def send_authentication_error_notification(send_dbus_notification):
    """Logs and notifies about an authentication failure.

    Arg:
        send_dbus_notification: A boolean specifying whether to send a
            notification to D-Bus.
    """
    # The message to show
    error_message = (
        "Invalid authentication credentials for Twitch API. Exiting."
    )

    # Show the message
    send_error_notification(error_message, send_dbus_notification)


def handle_failed_http_request(e, ignore_502s, print_to_terminal):
    """Handle a failed HTTP request occuring when querying the Twitch API.

    Args:
        e: An exception of type FailedHttpRequest.
        ignore_502s: A boolean signaling whether to ignore 502 errors when
            querying the Twitch API.
        print_to_terminal: A boolean signalling whether to
            print to the terminal instead of passing a message to D-Bus.
    """
    if (
        not ignore_502s
        or ignore_502s
        and e.status_code != HTTP_502_BAD_GATEWAY
    ):
        send_error_notification(e.message, not print_to_terminal)


def process_notifications_for_streamer(
    streamer_login_name,
    games,
    twitch_api,
    ignore_502s,
    streamers_previous_game,
    print_to_terminal,
):
    """Query the Twitch API for a spcific streamer and display notifications.

    Args:
        ignore_502s: A boolean signaling whether to ignore 502 errors when
            querying the Twitch API.
        games: A dictionary containing information about what games to
            allow (or disallow) for the streamer. See the configuration
            file for how these look.
        print_to_terminal: A boolean signalling whether to
            print to the terminal instead of passing a message to D-Bus.
        streamer_login_name: A string containing the login name of the
            streamer to process notifications for.
        streamers_previous_game: A dictionary containing
            information about what game a streamer was last seen
            playing.  The keys are strings containing the streamers
            login name, and the keys are strings containing the game ID
            of what they were last seen playing (or an empty string if
            the streamer hasn't yet been seen live). Can be None.
        twitch_api: An authenticated TwitchApi object to interact with
            Twitch's API.
    """
    try:
        # Get info about stream
        info = twitch_api.get_online_stream_info(streamer_login_name)
    except FailedHttpRequest as e:
        handle_failed_http_request(e, ignore_502s, print_to_terminal)

        return

    # If the streamer isn't live, record that they aren't playing
    # anything and move onto the next streamer
    if not info["live"]:
        # Mark them as last seen playing nothing
        if (
            streamers_previous_game
            and streamers_previous_game[streamer_login_name]
        ):
            streamers_previous_game[streamer_login_name] = ""

        return

    # Check if this is a game to notify about
    game_id = info["game_id"]
    game_name = info["game_name"]

    # If the streamer was last seen playing this game, move on. If
    # they are playing something new, record it.
    if streamers_previous_game:
        if streamers_previous_game[streamer_login_name] == game_id:
            # The streamer is playing the same game as before
            return

        # Streamer is playing something new. Update the previously
        # seen game.
        streamers_previous_game[streamer_login_name] = game_id

    # Check the include (and possibly exclude) list
    if "*" in games["include"]:
        # All games are included. Check if we need to exclude any
        # games.
        if "exclude" in games and (
            game_id in games["exclude"] or game_name in games["exclude"]
        ):
            return
    elif game_id not in games["include"] or game_name not in games["include"]:
        # Game not in the include list
        return

    # Send a notification
    if print_to_terminal:
        print_notification_to_terminal(
            info["user_display_name"], info["title"], info["game_name"]
        )
    else:
        send_notification_to_dbus(
            info["user_display_name"], info["title"], info["game_name"]
        )


def process_notifications(
    streamers,
    twitch_api,
    ignore_502s,
    streamers_previous_game=None,
    print_to_terminal=False,
):
    """Query the Twitch API for all streamers and display notifications.

    The whole function is a big loop going over all the streamers present
    in the config file.

    Args:
        ignore_502s: A boolean signaling whether to ignore 502 errors when
            querying the Twitch API.
        print_to_terminal: An optional boolean signalling whether to
            print to the terminal instead of passing a message to D-Bus.
            Defaults to False.
        streamers: A dictionary of streamers where the keys are strings
            containing the streamer's login name and the values are
            dictionaries containing the user's settings for the
            streamer. For example:

            {'shroud: {'include': ['Valorant']},
             'hasanabi': {'include': ['*'], 'exclude': ['Just Chatting']},
             'tyler1': {'include': ['*'], 'exclude': ['33214']}}
        streamers_previous_game: An optional dictionary containing
            information about what game a streamer was last seen
            playing.  The keys are strings containing the streamers
            login name, and the keys are strings containing the game ID
            of what they were last seen playing (or an empty string if
            the streamer hasn't yet been seen live). This defaults to
            None, which is used when this function is only being called
            once.
        twitch_api: An authenticated TwitchApi object to interact with
            Twitch's API.
    """
    # Look up info about each streamer's stream
    for streamer_login_name, games_dict in streamers.items():
        process_notifications_for_streamer(
            streamer_login_name,
            games_dict,
            twitch_api,
            ignore_502s,
            streamers_previous_game,
            print_to_terminal,
        )


def process_notifications_wrapper(*args, **kwargs):
    """A wrapper for process_notifications to catch connection errors.

    This makes the code a bit cleaner than inserting lots of try/except
    blocks into the process_notifications function.
    """
    # Determine whether to print to the terminal
    display_dbus_notification = not kwargs["print_to_terminal"]

    # Try calling process_notifications
    retry_attempt = 0

    try:
        process_notifications(*args, **kwargs)

        if retry_attempt:
            retry_attempt = 0
    except requests.exceptions.ConnectionError:
        # Bad connection - stop this iteration and wait
        retry_attempt += 1
        sleep_delta = 2 ** retry_attempt

        send_connection_error_notification(
            send_dbus_notification=display_dbus_notification,
            retry_seconds=sleep_delta,
        )

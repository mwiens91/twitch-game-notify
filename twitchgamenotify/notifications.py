"""Functions for processing and displaying notifications."""

import datetime
import logging
import time
import notify2
import requests
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
    print("Title: %s" % stream_title)
    print("Playing: %s" % game_name)


def send_notification_to_dbus(streamer_name, stream_title, game_name):
    """Send a game notification to D-Bus.

    Args:
        streamer_name: A string containing the name of the streamer.
        stream_title: A string containing the title of the stream.
        game_name: A string containing the name of the game.
    """
    notify2.Notification(
        streamer_name + " @ " + time.strftime("%H:%M"),
        "Title: %s\nPlaying: %s" % (stream_title, game_name),
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


def process_notifications(
    streamers,
    twitch_api,
    names_cache=None,
    streamers_previous_game=None,
    print_to_terminal=False,
):
    """Query the Twitch API for all streamers and display notications.

    Args:
        names_cache: An optional dictionary containing cached names for
            games and streamers. For example:

            {"games": {"460630": "Tom Clancy's Rainbow Six: Siege"},
             "streamers": {"macie_jay": "Macie_Jay"}}

            Defaults to None.
        print_to_terminal: An optional boolean signalling whether to
            print to the terminal instead of passing a message to D-Bus.
            Defaults to False.
        streamers: A dictionary of streamers where the keys are strings
            containing the streamer's login name and the values are
            dictionaries containing the user's settings for the
            streamer. For example:

            {'macie_jay': {'include': '460630'},
             'moonmoon_ow': {'include': '*', 'exclude': '33214'}}

        streamers_previous_game: An optional dictionary containing
            information about what game a streamer was last seen
            playing.  The keys are strings containing the streamers
            login name, and the keys are strings containing the game ID
            of what they were last seen playing (or an empty string if
            the streamer hasn't yet been seen live). This defaults to
            None, which is useful if this function is only being called
            once.
        twitch_api: An authenticated TwitchApi object to interact with
            Twitch's API.
    """
    # Look up info about each streamer's stream
    for streamer_login_name, games in streamers.items():
        try:
            # Get info about stream
            info = twitch_api.get_online_stream_info(streamer_login_name)
        except FailedHttpRequest as e:
            # Bad HTTP request! Log the error and move onto the next
            # streamer!
            send_error_notification(e.message, not print_to_terminal)

            continue

        # If the streamer isn't live, record that they aren't playing
        # anything and move onto the next streamer
        if not info["live"]:
            # Mark them as last seen playing nothing
            if (
                streamers_previous_game
                and streamers_previous_game[streamer_login_name]
            ):
                streamers_previous_game[streamer_login_name] = ""

            continue

        # Check if this is a game to notify about
        game_id = info["game_id"]

        # If the streamer was last seen playing this game, move on. If
        # they are playing something new, record it.
        if streamers_previous_game:
            if streamers_previous_game[streamer_login_name] == game_id:
                # The streamer is playing the same game as before
                continue

            # Streamer is playing something new. Update the previously
            # seen game.
            streamers_previous_game[streamer_login_name] = game_id

        # Check the include (and possibly exclude) list
        if "*" in games["include"]:
            # All games are included. Check if we need to exclude any
            # games.
            if "exclude" in games and game_id in games["exclude"]:
                continue

        elif game_id not in games["include"]:
            # Game not in the include list
            continue

        # Gather info about the stream. Lookup info in the cache first
        # if it's available.
        if names_cache is not None:
            # Try getting the display name from the cache
            try:
                streamer_display_name = names_cache["streamers"][
                    streamer_login_name
                ]
            except KeyError:
                # Fetch it
                try:
                    streamer_display_name = twitch_api.get_streamer_display_name(
                        streamer_login_name
                    )
                except FailedHttpRequest as e:
                    # Bad HTTP request! Log the error and move onto the next
                    # streamer!
                    send_error_notification(e.message, not print_to_terminal)

                    continue

                # Store it
                names_cache["streamers"][
                    streamer_login_name
                ] = streamer_display_name

            # Try getting the game title from the cache
            try:
                game_title = names_cache["games"][game_id]
            except KeyError:
                # Fetch it
                try:
                    game_title = twitch_api.get_game_title(game_id)
                except FailedHttpRequest as e:
                    # Bad HTTP request! Log the error and move onto the next
                    # streamer!
                    send_error_notification(e.message, not print_to_terminal)

                    continue

                # Store it
                names_cache["games"][game_id] = game_title
        else:
            # Not using cache. Fetch everything.
            try:
                streamer_display_name = twitch_api.get_streamer_display_name(
                    streamer_login_name
                )
                game_title = twitch_api.get_game_title(game_id)
            except FailedHttpRequest as e:
                # Bad HTTP request! Log the error and move onto the next
                # streamer!
                send_error_notification(e.message, not print_to_terminal)

                continue

        # Title is never cached
        stream_title = info["title"]

        # Send a notification
        if print_to_terminal:
            print_notification_to_terminal(
                streamer_display_name, stream_title, game_title
            )
        else:
            send_notification_to_dbus(
                streamer_display_name, stream_title, game_title
            )


def send_connection_error_notification(send_dbus_notification, retry_seconds):
    """Logs and notifies about a connection failure.

    Arg:
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


def process_notifications_wrapper(*args, **kwargs):
    """A wrapper for process_notifications to catch connection errors.

    This makes the code a bit cleaner than inserting lots of try/except
    blocks into the process_notifications function.
    """
    # Determine whether to print to the terminal
    try:
        display_dbus_notification = not kwargs["print_to_terminal"]
    except KeyError:
        # In accordance with print_to_terminal defaulting to False
        display_dbus_notification = True

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

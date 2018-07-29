"""Functions for processing and displaying notifications."""

import datetime
import time
import notify2
from twitchgamenotify.twitch_api import FailedHttpRequest


# ANSI escape sequence for bold text
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
        streamer_name + " @ " + time.strftime('%H:%M'),
        "Title: %s\nPlaying: %s" % (stream_title, game_name)
        ).show()


def process_notifications(
        streamers,
        twitch_api,
        names_cache=None,
        streamers_previous_game=None,
        print_to_terminal=False):
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
        except FailedHttpRequest:
            # Bad HTTP request! The sender of this exception has already
            # logged an error, so we don't need to do that here. Move on
            # to the next streamer.
            continue

        # If the streamer isn't live, record that they aren't playing
        # anything and move onto the next streamer
        if not info['live']:
            # Mark them as last seen playing nothing
            if (streamers_previous_game
                    and streamers_previous_game[streamer_login_name]):
                streamers_previous_game[streamer_login_name] = ""

            continue

        # Check if this is a game to notify about
        game_id = info['game_id']

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
        if "*" in games['include']:
            # All games are included. Check if we need to exclude any
            # games.
            if 'exclude' in games and game_id in games['exclude']:
                continue

        elif game_id not in games['include']:
            # Game not in the include list
            continue

        # Gather info about the stream. Lookup info in the cache first
        # if it's available.
        if names_cache is not None:
            try:
                streamer_display_name = (
                    names_cache['streamers'][streamer_login_name])
            except KeyError:
                streamer_display_name = (
                    twitch_api.get_streamer_display_name(streamer_login_name))
                names_cache['streamers'][streamer_login_name] = (
                    streamer_display_name)

            try:
                game_title = names_cache['games'][game_id]
            except KeyError:
                game_title = twitch_api.get_game_title(game_id)
                names_cache['games'][game_id] = game_title
        else:
            streamer_display_name = (
                twitch_api.get_streamer_display_name(streamer_login_name))
            game_title = twitch_api.get_game_title(game_id)

        # Title is never cached
        stream_title = info['title']

        # Send a notification
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

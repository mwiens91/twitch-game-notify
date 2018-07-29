"""Provides a class to interact with a subset of the Twitch API.

Specifically, the "new Twitch API", which they haven't put a version on
yet. Right now this uses the Client-ID header, which is fine for a
relatively small number of requests. JWT support can be developed at
some point to allow for a higher volume of requests.
"""

import logging
import requests
from twitchgamenotify.constants import TWITCH_BASE_API_URL


class FailedHttpRequest(Exception):
    """An exception raised when an HTTP request failed."""
    pass


class TwitchApi:
    """Interacts with the Twitch API."""
    def __init__(self, client_id):
        """Set up authorization."""
        self.client_id = client_id
        self.session = requests.Session()
        self.session.headers.update({'Client-ID': self.client_id})

    @staticmethod
    def check_http_status_code(status_code, http_request_url):
        """Checks that an HTTP status code is okay.

        If it's not okay, it'll issue an error message to the logger
        specifying why and also raise a FailedHttpRequest exception.

        Args:
            status_code: An integer specifying the status code of a
                completed HTTP request.
            http_request_url: A string containing the URL that was used
                to make the completed HTTP request.
        Raises:
            FailedHttpRequest: The status code indicates the HTTP
                request was not successful.
        """
        try:
            # Make the the HTTP request was okay
            assert status_code == 200
        except AssertionError:
            # Uh oh
            logging.error(
                "The HTTP request to %s failed with status code %s",
                http_request_url,
                status_code,)

            raise FailedHttpRequest

    def get_online_stream_info(self, streamer_login_name):
        """Requests info about an online stream.

        Arg:
            streamer_login_name: A string specifying the streamer's user
                login name. E.g., moonmoon_ow.

        Returns:
            A dictionary of information about the queried stream
            including whether it's live, its title, and the current
            game's game ID. For example:

            {'live': True,
             'title': "Macie Jay Charm PogChamp",
             'game_id': '460630'}

        Raises:
            FailedHttpRequest: The status code indicates the HTTP
                request was not successful.
        """
        # Make a request to the Twitch API
        r = self.session.get(
            TWITCH_BASE_API_URL
            + '/streams?user_login='
            + streamer_login_name)

        # Verify that the HTTP method was okay
        self.check_http_status_code(r.status_code, r.url)

        # Build up the info of this stream
        r_data = r.json()['data']

        if not r_data:
            # Stream is offline
            stream_info = dict(
                live=False,
                title="",
                game_id="",)
        else:
            stream_info = dict(
                live=True,
                title=r_data[0]['title'],
                game_id=r_data[0]['game_id'],)

        return stream_info

    def get_streamer_display_name(self, streamer_login_name):
        """Get a streamer's display name given their login name.

        Arg:
            streamer_login_name: A string specifying the streamer's user
                login name. E.g., moonmoon_ow.

        Returns:
            A string containing the streamer's display name.

        Raises:
            FailedHttpRequest: The status code indicates the HTTP
                request was not successful.
        """
        # Make a request to the Twitch API
        r = self.session.get(
            TWITCH_BASE_API_URL
            + '/users?login='
            + streamer_login_name)

        # Verify that the HTTP method was okay
        self.check_http_status_code(r.status_code, r.url)

        # Return the display name
        return r.json()['data'][0]['display_name']

    def get_game_title(self, game_id):
        """Get a game's title given its ID.

        Arg:
            game_id: A string containing a Twitch game ID.

        Returns:
            A string containing the game's title.

        Raises:
            FailedHttpRequest: The status code indicates the HTTP
                request was not successful.
        """
        # Make a request to the Twitch API
        r = self.session.get(
            TWITCH_BASE_API_URL
            + '/games?id='
            + game_id)

        # Verify that the HTTP method was okay
        self.check_http_status_code(r.status_code, r.url)

        # Return the game title
        return r.json()['data'][0]['name']

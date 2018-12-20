"""Provides a class to interact with a subset of the Twitch API.

Specifically, the "new Twitch API", which they haven't put a version
number on yet.
"""

import requests
from twitchgamenotify.constants import (
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED,
    TWITCH_GAME_API_URL,
    TWITCH_STREAM_API_URL,
    TWITCH_TOKEN_API_URL,
    TWITCH_USER_API_URL,
)


class FailedHttpRequest(Exception):
    """An exception raised when an HTTP request failed."""

    def __init__(self, message, http_status_code):
        """Record what the HTTP status code for the bad request was."""
        # Call the parent class __init__
        super().__init__(message)

        # Record the status code and message
        self.status_code = http_status_code
        self.message = message


class TwitchApi:
    """Interacts with the Twitch API."""

    def __init__(self, client_id, client_secret):
        """Set up authorization."""
        # Load in authentication details
        self.client_id = client_id
        self.client_secret = client_secret

        # Start a requests session
        self.session = requests.Session()

        # Get and set an access token
        self.obtain_access_token()

    def obtain_access_token(self):
        """Obtains and sets a fresh access token."""
        # Get the access token
        response = requests.post(
            TWITCH_TOKEN_API_URL
            + "?client_id="
            + self.client_id
            + "&client_secret="
            + self.client_secret
            + "&grant_type=client_credentials"
        )

        try:
            # Make the the HTTP request was okay
            assert response.status_code == HTTP_200_OK
        except AssertionError:
            # The HTTP request wasn't okay
            message = (
                "An access token fetch failed with status code %s"
                % response.status_code
            )

            raise FailedHttpRequest(
                message=message, http_status_code=response.status_code
            )

        # Set the access token
        access_token = response.json()["access_token"]
        self.session.headers.update(
            {"Authorization": "Bearer " + access_token}
        )

    def make_http_request(self, http_request_url):
        """Makes an HTTP request.

        This assumes that all incoming HTTP requests are GETs, which
        will be true for everything passed to this function within the
        scope of this program.

        If an access token is expired, another one is obtained.

        Args:
            http_request_url: A string containing the URL to make an
                HTTP request to.

        Returns:
            A requests.models.Response object containing the response to
            the successful HTTP request.

        Raises:
            FailedHttpRequest: The status code indicated the HTTP
                request was not successful.
        """
        # Make the request
        response = self.session.get(http_request_url)

        # If our access token has expired, get another one and retry the
        # request
        if response.status_code == HTTP_401_UNAUTHORIZED:
            # Get a new access token
            self.obtain_access_token()

            # Repeat the request
            response = self.session.get(http_request_url)

        try:
            # Make the the HTTP request was okay
            assert response.status_code == HTTP_200_OK
        except AssertionError:
            # The HTTP request wasn't okay
            message = "An HTTP request to %s failed with status code %s" % (
                http_request_url,
                response.status_code,
            )

            raise FailedHttpRequest(
                message=message, http_status_code=response.status_code
            )

        return response

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
        """
        # Make a request to the Twitch API
        response = self.make_http_request(
            TWITCH_STREAM_API_URL + "?user_login=" + streamer_login_name
        )

        # Build up the info of this stream
        response_data = response.json()["data"]

        if not response_data:
            # Stream is offline
            stream_info = dict(live=False, title="", game_id="")
        else:
            stream_info = dict(
                live=True,
                title=response_data[0]["title"],
                game_id=response_data[0]["game_id"],
            )

        return stream_info

    def get_streamer_display_name(self, streamer_login_name):
        """Get a streamer's display name given their login name.

        Arg:
            streamer_login_name: A string specifying the streamer's user
                login name. E.g., moonmoon_ow.

        Returns:
            A string containing the streamer's display name.
        """
        # Make a request to the Twitch API
        response = self.make_http_request(
            TWITCH_USER_API_URL + "?login=" + streamer_login_name
        )

        # Return the display name
        return response.json()["data"][0]["display_name"]

    def get_game_title(self, game_id):
        """Get a game's title given its ID.

        Arg:
            game_id: A string containing a Twitch game ID.

        Returns:
            A string containing the game's title.
        """
        # Special case: no game set (Twitch gives this a game ID of 0)
        if game_id == "0":
            return ""

        # Make a request to the Twitch API
        response = self.make_http_request(
            TWITCH_GAME_API_URL + "?id=" + game_id
        )

        # Return the game title
        return response.json()["data"][0]["name"]

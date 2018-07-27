"""Provides a class to interact with a subset of the Twitch API.

Specifically, the "new Twitch API", which they haven't put a version on
yet. Right now this uses the Client-ID header, which is fine for a
relatively small number of requests. JWT support can be developed at
some point to allow for a higher volume of requests.
"""

class TwitchApi:
    """Interacts with the Twitch API."""
    def __init__(self, client_id):
        # Set up authorization
        self.client_id = client_id

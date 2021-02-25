[![Build status](https://ci.appveyor.com/api/projects/status/1qrsle0yooilklav?svg=true)](https://ci.appveyor.com/project/mwiens91/twitch-game-notify)
[![codecov](https://codecov.io/gh/mwiens91/twitch-game-notify/branch/master/graph/badge.svg)](https://codecov.io/gh/mwiens91/twitch-game-notify)
[![PyPI](https://img.shields.io/pypi/v/twitch-game-notify.svg)](https://pypi.org/project/twitch-game-notify/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/twitch-game-notify.svg)](https://pypi.org/project/twitch-game-notify/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# twitch-game-notify

This is a Twitch notifier which notifies you when your favourite
steamers stream your favourite things. Any flavour of unix that
supports GTK3 should work with this.

With normal settings, this will send notifications to your existing
notification handler when a streamer is playing a game you've specified.
There's also a tray icon so you can easily quit the application.


## Installation

There are a few dependencies needed for this. I'll write
commands to install the dependencies for Ubuntu; however,
these packages are common, so translating this to whatever
package manager you use should be fairly easy.

To get the dependencies needed for D-Bus notifications and for
displaying an icon in the system tray, run

```
sudo apt install libdbus-1-dev libdbus-glib-1-dev \
                 libcairo2-dev libgirepository1.0-dev
```

If you want to install twitch-game-notify globally on your machine (you
could also run this from the from source code directly from
[run_twitchgamenotify.py](run_twitchgamenotify.py)), install it using
pip with or without root as in

```
sudo pip3 install twitch-game-notify
```

Running the above command with root isn't strictly necessary, but it'll
put `twitch-game-notify` in your `$PATH`, which is nice.

## Configuration

Configuration files something look like the following:

```yaml
# Twitch API authorization - see https://dev.twitch.tv/docs/api/
twitch-api-client-id: "p0gch4mp101fy451do9uod1s1x9i4a"
twitch-api-client-secret: "itqb0thqi5cek18ae6ekm7pbqvh63k"

# Streamers: a list of streamer login names, and for each, which
# games/game IDs to notify about
streamers:
  "shroud":
    include:
      - "Valorant" # notify me only when shroud plays Rainbow Six: Siege
  "hasanabi":
    include:
      - "*"        # notify me when Hasan plays any game
    exclude:
      - "Just Chatting"    # except for when he's Just Chatting
  "loltyler1":
    include:
      - "*"        # notify me when Tyler1 plays any game
    exclude:
      - "21779"    # except for League of Legends

```

Here you need to put in your authentication credentials, and specify
what streamers you care about and what things they stream that you care
about (or don't care about). Note that you can specify games using
either their name as they appear on Twitch or by their internal game
IDs—either is fine.

### Setting up a configuration file

twitch-game-notify looks for a configuration file at two paths:

1. `$PROJECT_ROOT/config.yaml`
2. `$XDG_CONFIG_HOME/twitch-game-notify/config.yaml`

where `$PROJECT_ROOT` is the base of the twitch-game-notify project
(which you generally only want to use if you're running from source),
and `$XDG_CONFIG_HOME` defaults to `$HOME/.config`, if you don't have it
defined.

To get started, either copy the example configuration file
[config.yaml.example](config.yaml.example) to one of the above locations
(making sure to rename it to `config.yaml`) or run

```
twitch-game-notify --print-config
```

which prints the example config file
to the terminal, which you can redirect to a file.

### Getting a Twitch API client ID and client secret

To get a Twitch client ID and client secret, you need to either create
or link an existing Twitch account with [Twitch's dev
portal](https://dev.twitch.tv/). Up to date instructions for obtaining a
client ID and client secret can be found at
[dev.twitch.tv/docs/authentication](https://dev.twitch.tv/docs/authentication/).

## Usage

Run twitch-game-notify with

```
twitch-game-notify
```

or directly with [run_twitchgamenotify.py](run_twitchgamenotify.py):

```
./run_twitchgamenotify.py
```

For a list of everything you can do with twitch-game-notify, run

```
twitch-game-notify --help
```

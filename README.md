[![Build status](https://ci.appveyor.com/api/projects/status/1qrsle0yooilklav?svg=true)](https://ci.appveyor.com/project/mwiens91/twitch-game-notify)
[![codecov](https://codecov.io/gh/mwiens91/twitch-game-notify/branch/master/graph/badge.svg)](https://codecov.io/gh/mwiens91/twitch-game-notify)
[![PyPI](https://img.shields.io/pypi/v/twitch-game-notify.svg)](https://pypi.org/project/twitch-game-notify/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/twitch-game-notify.svg)](https://pypi.org/project/twitch-game-notify/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

# twitch-game-notify

This is a Twitch notifier which notifies you when your favourite
steamers play your favourite games. Officially, Ubuntu >= 16.04 is
supported, but other Linux distros and possibly even Mac OSs may also
work (contact me if you have it running on another distro or OS—I'm
curious).

With normal settings, this will send notifications to your existing
notification handler when a streamer is playing a game you've specified:

[![notification](https://i.imgur.com/4MM61Pk.png)](https://www.twitch.tv/shroud)

You'll also get a tray icon so you can easily quit the application:

![tray-icon](https://i.imgur.com/uDdtJDa.png)

## Installation

We'll need to install a few dependencies first. I'll assume you're on
Ubuntu.

To get the dependencies needed for D-Bus notifications and for
displaying an icon in the system tray, run

```
sudo apt install libdbus-1-dev libdbus-glib-1-dev \
                 libcairo2-dev libgirepository1.0-dev
```

If you want to install twitch-game-notify globally on your machine (cf.
running from source directly from
[run_twitchgamenotify.py](run_twitchgamenotify.py)), install it using
pip with

```
sudo pip3 install twitch-game-notify
```

Running the above command with root isn't strictly necessary, but it'll
put the `twitch-game-notify` binary on your `$PATH`, which is nice.

## Configuration

Configuration files look like the following:

```yaml
query-period: 5
twitch-api-client-id: "p0gch4mp101fy451do9uod1s1x9i4a"
twitch-api-client-secret: "itqb0thqi5cek18ae6ekm7pbqvh63k"
streamers:
  "macie_jay":     # Macie_Jay
    include:
      - "460630"   # notify my when Macie plays Rainbow Six: Siege
  "moonmoon_ow":   # MOONMOON_OW
    include:
      - "*"        # notify me when Moon plays any game
    exclude:
      - "33214"    # except for Fortnite
```

There's a `query-period`, which specifies how often the main loop
happens for querying the streamers you've specified (in seconds).
There's a `twitch-api-client-id` and `twitch-api-client-secret`, which
we'll get to in a second. Then there's a list of streamers, which for
each you specify what games you want to be notified about.

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
twitch-game-notify --print-config > $DEST/config.yaml
```

which downloads the example configuration file from GitHub and prints it
to the terminal, which you can then redirect to a file.

### Getting a Twitch API client ID and client secret

To get a Twitch client ID and client secret, you need to either create
or link an existing Twitch account with [Twitch's dev
portal](https://dev.twitch.tv/). Up to date instructions for obtaining a
client ID and client secret can be found at
[dev.twitch.tv/docs/authentication](https://dev.twitch.tv/docs/authentication/).

### Constructing the streamers list

The streamers list has a bunch of streamer login names. For example,
[MOONMOON_OW](https://www.twitch.tv/moonmoon_ow)'s login name is
moonmoon_ow, which can be easily found from his stream's URL:

```
https://www.twitch.tv/moonmoon_ow
```

For each streamer you can include games you want to be notified about.
For example,

```yaml
streamers:
  "macie_jay":     # Macie_Jay
    include:
      - "460630"   # notify my when Macie plays Rainbow Six: Siege
```

where 460630 is the game ID for Tom Clancy's Rainbow Six: Siege.

If you want to be notified when a streamer plays any game you can use
`"*"`. For example,

```yaml
streamers:
  "moonmoon_ow":   # MOONMOON_OW
    include:
      - "*"        # notify me when Moon plays any game
```

If you want to be notified about every game *except* specific games, you
can also specify an `exclude` section along with `"*"`. For example,

```yaml
streamers:
  "moonmoon_ow":   # MOONMOON_OW
    include:
      - "*"        # notify me when Moon plays any game
    exclude:
      - "33214"    # except for Fortnite
```

where 33214 is the game ID for Fortnite.

You can find out what the game ID for a given game is by querying the
Twitch API directly (see [their
reference](https://dev.twitch.tv/docs/api/reference/#get-games) for
how). For convenience, a list of popular games' IDs are listed in the
example configuration file [config.yaml.example](config.yaml.example):

```yaml
# 7 Days to Die: 271304
# A Dance of Fire and Ice: 511183
# Ace Combat 7: 492605
# Age of Empires II: 13389
# Age of Wonders: Planetfall: 506105
# AI: The Somnium Files: 508537
# Albion Online: 417528
# Always On: 499973
# Anno 1800: 498638
# Apex Legends: 511224
# Arena of Valor: 498302
# ARK: 489635
# Art: 509660
# Artifact: 16937
# ASMR: 509659
# ...
```

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

## Rate limits

The Twitch API allows for 120 API queries per minute. When you first
start up twitch-game-notify, you're going to be using up to 3 API
queries per streamer you've specified. When you've been running
twitch-game-notify for awhile, most of the static API data will be
cached and you're going be using ~1 API query per streamer.

As a rough estimate, if you have `N` streamers on your list, you're
going to want to have a `query-period` of a little above `N / 2`
seconds.

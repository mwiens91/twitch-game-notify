#!/usr/bin/env python3

from setuptools import setup
from twitchgamenotify.version import NAME, DESCRIPTION, VERSION


# Parse readme to include in PyPI page
with open("README.md") as f:
    long_description = f.read()


def capitalize(s):
    """Capitalize the first letter of a string.

    Unlike the capitalize string method, this leaves the other
    characters untouched.
    """
    return s[:1].upper() + s[1:]


setup(
    name=NAME,
    version=VERSION,
    description=capitalize(DESCRIPTION),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mwiens91/twitch-game-notify",
    author="Matt Wiens",
    author_email="mwiens91@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: Unix",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
    ],
    packages=["twitchgamenotify", "static"],
    package_data={"static": ["twitch.svg"]},
    entry_points={
        "console_scripts": ["twitch-game-notify = twitchgamenotify.main:main"]
    },
    python_requires=">=3.5",
    install_requires=[
        "dbus-python",
        "notify2",
        "PyGObject",
        "PyYAML",
        "requests",
    ],
)

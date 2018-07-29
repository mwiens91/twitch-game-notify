#!/usr/bin/env python3

from setuptools import setup
from twitchgamenotify.version import NAME, DESCRIPTION, VERSION


# Parse readme to include in PyPI page
with open('README.md') as f:
    long_description = f.read()

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION.capitalize(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/mwiens91/twitch-game-notify',
    author='Matt Wiens',
    author_email='mwiens91@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3 :: Only',
    ],
    packages=['twitchgamenotify', 'static'],
    package_data={'static': ['twitch.svg']},
    entry_points={
        'console_scripts': ['twitch-game-notify = twitchgamenotify.main:main'],
    },
    install_requires=[
        'dbus-python',
        'notify2',
        'PyGObject',
        'PyYAML',
        'requests',
    ],
)

from setuptools import setup
from twitchgamenotify.version import NAME, DESCRIPTION, VERSION

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
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
    packages=['twitchgamenotify'],
    entry_points={
        'console_scripts': ['twitch-game-notify = twitchgamenotify.main:main'],
    },
    install_requires=[
        'dbus-python',
        'notify2',
        'PyYAML',
        'requests',
        'xdg',
    ],
)

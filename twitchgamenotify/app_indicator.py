"""Contains an application indicator.

Thanks to Timur Rubeko with his wonderful guide here:
https://candidtim.github.io/appindicator/2014/09/13/ubuntu-appindicator-step-by-step.html.
"""

import logging
import os
import gi
from twitchgamenotify.constants import APP_INDICATOR_SVG_PATH
from twitchgamenotify.version import NAME

# Make sure our GTK stuff is good before loading the app indicator
try:
    gi.require_version('Gtk', '3.0')
    gi.require_version('AppIndicator3', '0.1')
except ValueError as e:
    logging.error(e)
    os._exit(1)

from gi.repository import Gtk, AppIndicator3


class AppIndicator():
    """Shows a simple app indicator for the program."""
    def __init__(self):
        """Setup the app indicator."""
        # Setup
        self.indicator = AppIndicator3.Indicator.new(
            NAME,
            APP_INDICATOR_SVG_PATH,
            AppIndicator3.IndicatorCategory.SYSTEM_SERVICES)
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)

        # Build the menu
        menu = Gtk.Menu()
        item_quit = Gtk.MenuItem('Quit')

        # Wrap the kill_main function
        quit_wrapper = lambda source: kill_main(0)

        item_quit.connect('activate', quit_wrapper)
        menu.append(item_quit)
        menu.show_all()

        self.indicator.set_menu(menu)

    @staticmethod
    def start():
        """Starts the Gtk main loop (and hence the indicator)."""
        Gtk.main()

    @staticmethod
    def stop():
        """Stops the Gtk main loop (and hence the indicator)."""
        Gtk.main_quit()

def kill_main(exit_code):
    """Kills the main loop gracefully from within a thread.
    See
    https://stackoverflow.com/questions/1489669/how-to-exit-the-entire-application-from-a-python-thread.
    """
    os._exit(exit_code)

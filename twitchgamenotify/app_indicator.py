"""Contains an application indicator.

I've only tested this on Ubuntu + i3. This should work wherever GTK
works, though.
"""

import _thread  # pylint: disable=wrong-import-order
import logging
import gi
from twitchgamenotify.constants import APP_INDICATOR_SVG_PATH
from twitchgamenotify.version import NAME, VERSION

# Make sure our GTK stuff is good before loading the app indicator
try:
    gi.require_version("Gtk", "3.0")
except ValueError as e:
    logging.error(e)
    _thread.interrupt_main()

# fmt: off
from gi.repository import Gtk # pylint: disable=wrong-import-order,wrong-import-position
# fmt: on


class AppIndicator:
    """Shows a simple app indicator for the program."""

    def __init__(self):
        """Setup the app indicator."""
        # Build the menu
        self.menu = Gtk.Menu()
        item_quit = Gtk.MenuItem("Quit")

        # Wrap the kill_main function
        quit_wrapper = lambda source: _thread.interrupt_main()

        item_quit.connect("activate", quit_wrapper)
        self.menu.append(item_quit)
        self.menu.show_all()

        self.indicator = Gtk.StatusIcon(
            title=NAME, tooltip_text=NAME + " " + VERSION
        )
        self.indicator.set_from_file(APP_INDICATOR_SVG_PATH)
        self.indicator.connect("popup-menu", self.on_popup_menu)

    def on_popup_menu(self, icon, button, time):
        """Calls the menu popup."""
        self.menu.popup(
            None, None, Gtk.StatusIcon.position_menu, icon, button, time
        )

    @staticmethod
    def start():
        """Starts the Gtk main loop (and hence the indicator)."""
        Gtk.main()

    @staticmethod
    def stop():
        """Stops the Gtk main loop (and hence the indicator)."""
        Gtk.main_quit()

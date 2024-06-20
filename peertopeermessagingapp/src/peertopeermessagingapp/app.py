"""
A messaging app utilizing peer to peer technology, aimed at usage in high schools.
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


class PeertoPeerMessagingApp(toga.App):
    def startup(self):
        """
        Constructs and shows the Toga application.
        Args:
            None
        Returns: None
        """
        main_box = toga.Box()  # holds all GUI the content in the app

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

def main():
    return PeertoPeerMessagingApp()

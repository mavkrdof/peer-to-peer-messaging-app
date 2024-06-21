"""
A messaging app utilizing peer to peer technology,
aimed at usage in high schools.
"""

import toga
from peertopeermessagingapp.graphical_user_interface import GUI_manager


class PeertoPeerMessagingApp(toga.App):
    def startup(self):
        """
        Constructs and shows the Toga application.
        Args:
            None
        Returns: None
        """
        GUI_manager = GUI_manager(app=self)
        GUI_manager.init_main_GUI()

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = GUI_manager.main_box
        self.main_window.show()

    def exit(self) -> None:
        pass


def main():
    return PeertoPeerMessagingApp()

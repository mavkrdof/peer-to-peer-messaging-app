"""
A messaging app utilizing peer to peer technology,
aimed at usage in high schools.
"""

import toga
from peertopeermessagingapp.graphical_user_interface import GUI_manager


class PeertoPeerMessagingApp(toga.App):
    def startup(self) -> None:
        """
        Constructs and shows the Toga application.
        Args:
            None
        Returns: None
        """
        GUI = GUI_manager(app=self)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = GUI.main_box
        GUI.start()
        self.main_window.show()

    def exit(self) -> None:
        pass


def main() -> PeertoPeerMessagingApp:
    return PeertoPeerMessagingApp()

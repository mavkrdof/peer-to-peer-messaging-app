"""
A messaging app utilizing peer to peer technology,
aimed at usage in high schools.
"""

import logging
import toga
import toga.style
import toga.style.pack
from peertopeermessagingapp.graphical_user_interface import GUI_manager
from peertopeermessagingapp.backend import Backend_manager


class PeertoPeerMessagingApp(toga.App):
    def startup(self) -> None:
        """
        Constructs and shows the Toga application.
        Args:
            None
        Returns: None
        """
        # initialise Backend
        # logging.basicConfig(filename='runtime_logs.log', encoding='utf-8', level=logging.DEBUG, filemode='w')
        logging.basicConfig(level=logging.INFO)
        self.backend = Backend_manager(app=self)
        # initialise GUI
        GUI = GUI_manager(app=self)
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = GUI.main_box
        GUI.start()
        self.main_window.show()

    def exit(self) -> None:
        super().exit()


def main() -> PeertoPeerMessagingApp:
    """
    main func that starts the app

    Returns:
        PeertoPeerMessagingApp: the toga application
    """
    return PeertoPeerMessagingApp()

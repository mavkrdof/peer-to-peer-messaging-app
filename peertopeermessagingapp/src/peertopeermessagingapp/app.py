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
from peertopeermessagingapp.network_manager import Network_manager


class PeertoPeerMessagingApp(toga.App):
    def startup(self) -> None:
        """
        Constructs and shows the Toga application.
        Args:
            None
        Returns: None
        """
        # initialise Backend
        logging.basicConfig(level=logging.DEBUG)
        self.backend = Backend_manager(app=self)
        # init network
        self.network_manager = Network_manager(app=self)
        # init logging
        logging.basicConfig(filename=self.backend.log_filepath, encoding='utf-8', level=logging.DEBUG, filemode='w')
        # initialise GUI
        self.GUI = GUI_manager(app=self)
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.GUI.main_box
        self.GUI.start()
        self.main_window.show()

    def exit(self) -> None:
        """
        exit exits the application
        """
        try:
            self.backend.user_data.save_to_file()  # when data is saved using this func it is mangled
        finally:
            super().exit()


def main() -> PeertoPeerMessagingApp:
    """
    main func that starts the app

    Returns:
        PeertoPeerMessagingApp: the toga application
    """
    return PeertoPeerMessagingApp()

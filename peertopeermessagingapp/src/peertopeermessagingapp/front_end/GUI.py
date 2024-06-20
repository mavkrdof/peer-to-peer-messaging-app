"""
this module holds the functions for the GUI
"""
import toga


class GUI:
    """
    manages the graphical user interface
    vars:
    home_box: toga.Box
        the homescreen Box
    chat_list_GUI: toga.ScrollContainer
        the scroll container for chats
    main_box: toga.Box
        the main box
    methods:
        __init__: none
            the initializer function
        home_screen: none
            displays the home screen
        init_home_screen: none
            initializes the home screen
        main_GUI_init: none
            initializes the main box
    """

    def __init__(self) -> None:
        self.home_box = None
        self.chat_list_GUI = None

    def main_GUI_init(self):
        main_box = toga.Box()
        top_bar = toga.Box()

    def init_home_screen(self, chats=None):
        """
        initializer the home screen
        """
        self.home_box = toga.Box()
        self.chat_list_GUI = toga.ScrollContainer(
            id=None,
            style=None,
            horizontal=True,
            vertical=True,
            on_scroll=None,
            content=None
            )
        chat_list = {}
        for chat in chats:
            chat_list[chat.uniqueID] = (
                toga.Button(
                    icon=chat.icon_path,
                    text=chat.text,
                    on_press=chat.open  # when button pressed calls the open function for that chat
                )
            )
    
    def display_home_screen(self):
        """
        displays the home screen
        """

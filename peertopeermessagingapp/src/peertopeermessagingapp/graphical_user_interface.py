"""
this module holds the functions for the GUI
"""
from tkinter import N
import toga


class GUI_manager:
    """
    manages the graphical user interface
    vars:
    home_box: toga.Box
        the home screen Box
    chat_list_GUI: toga.ScrollContainer
        the scroll container for chats
    main_box: toga.Box
        the main box
    nav_bar_box: toga.Box
        the navigation bar container
    chat_box toga.box
        the chat screen container
    settings_box: toga.Box
        the settings screen container
    methods:
        __init__: none
            the initializer function
        home_screen: none
            displays the home screen
        init_nav_bar: none
            initializes the nav bar
        init_home_screen: none
            initializes the home screen
        init_chat_screen: none
            initializes the home screen
        init_settings_screen: none
            initializes the home screen
        main_GUI_init: none
            initializes the main box
    """

    def __init__(self, app) -> None:
        """
        init main GUI manager class
        """
        self.app = app
        # static
        self.current_screen = None
        self.main_box = None
        self.current_screen = 'Login'
        self.return_to = {
            'Login': app.exit,
            'Home': self.logout,
            'Chat': self.display_home_screen,
            'Settings-chat': self.display_chat_screen,
            'Settings-home': self.display_home_screen
        }
        # init screens
        self.login_screen = login_screen(
            main_box=self.main_box,
            GUI_manager=self
            )
        self.home_screen = home_screen(
            main_box=self._main_box,
            GUI_manager=self
            )
        # TODO: finish screen init
        # self.chat_screen =
        # self.create_account_screen = 
        # self.settings_screen = 

        




class screen():
    """
    a template class for all screens
    """

    def __init__(self, main_box, GUI_manager) -> None:
        """
        initializes the screen
        args:
             none
         returns:
             none
        """
        self.main_box: toga.Box = main_box
        self.GUI_manager: GUI_manager = GUI_manager
        # static
        self.name = None
        self.__box = None

    def display(self) -> None:
        """
         displays the screen
         args:
             none
         returns:
             none
        """
        for content in self.main_box.children:
            if content.name == 'nav_bar':
                pass
            else:
                self.main_box.remove(content)

        self.main_box.add(self.__box)


class home_screen(screen):
    """
    the screen that displays all chats
    """

    def __init__(self, main_box, GUI_manager) -> None:
        """
        initializes the home screen
        args:
            main_box (toga.Box): the main box of the app
        """
        super().__init__(main_box=main_box)
        self.chat_scroll_segment_count = 0
        self.chat_load_per_segment_limit = 5
        self.max_chat_list_segments = 5

        self.name = 'home_screen'
        self.__box = toga.Box()
        self.chat_list_scroll = toga.ScrollContainer(
            vertical=True,
            horizontal=False
        )
        # Add content to home screen box
        self.__box.add(self.chat_list_GUI)

    def populate_chat_list(self, chat_list: list) -> None:
        """
        populates the chat list with chats
        args:
            chat_list (list): a list of chats to be displayed
        returns:
            none
        """
        if self.chat_scroll_segment_count >= self.max_chat_list_segments:
            pass  # TODO: implement  max segments

        segment = self.create_chat_list_segment(
                chats=chat_list,
                chat_load_per_segment_limit=10
                )
        if segment:
            self.chat_scroll_segment_count += 1
            self.chat_list_scroll.add(segment)
        else:
            return None

    def create_chat_list_segment(self, chats, start_index) -> toga.Box:
        """
        creates a segment for the chat list
        args:
            chats (Chat): the chats to be displayed
         returns:
             box (toga.Box): a box containing all elements of this segment
         """
        # value checking
        final_index = start_index + self.chat_load_per_segment_limit
        if start_index or final_index > len(chats):
            return None
        # create segment
        segment = toga.Box()
        # fill segment
        for chat in chats[start_index: final_index]:
            chat_button = toga.Button(
                text=chat.name,
                on_press=self.display_chat_screen(chat)
            )  # TODO: maybe make into toga.box to make more good looking
            # add content to chat box
            segment.add(chat_button)
        return segment


class login_screen(screen):
    """
    the login screen
    """

    def __init__(self, main_box, GUI_manager) -> None:
        super().__init__(main_box=main_box, GUI_manager=GUI_manager)

        self.__username_field = toga.TextInput()
        self.__username_label = toga.Label()
        self.__password_field = toga.PasswordInput()
        self.__login_button = toga.Button(
            text='LOGIN',
            on_press=self.validate_login
        )
        self.__create_account_button = toga.Button(
            text='CREATE ACCOUNT',
            on_press=self.GUI_manager.Display_create_account
        )
        # add content to __box
        self.__box.add(self.__username_field)
        self.__box.add(self.__username_label)
        self.__box.add(self.__password_field)
        self.__box.add(self.__password_field)
        self.__box.add(self.__login_button)
        self.__box.add(self.__create_account_button)

    def validate_login(self) -> None:
        pass
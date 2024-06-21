"""
this module holds the functions for the GUI
"""
import toga


class GUI:
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
        init class
        """
        self.app = app
        # static
        self.current_screen = None
        self.main_box = None
        self.nav_bar_box = None
        self.chat_box = None
        self.settings_box = None
        self.chat_list_GUI = None
        self.current_screen = 'Login'
        self.return_to = {
            'Login': app.exit,
            'Home': self.logout,
            'Chat': self.display_home_screen,
            'Settings-chat': self.display_chat_screen,
            'Settings-home': self.display_home_screen
        }
    
    def display_home_screen(self) -> None:
        pass

    def display_chat_screen(self) -> None:
        pass

    def logout(self) -> None:
        pass

    def init_main_GUI(self) -> None:
        """
        initializes the main box
         args:
             none
         returns:
             none
        """
        self.main_box = toga.Box()
        self.init_nav_bar()
        self.main_box.add(self.nav_bar_box)

    def init_nav_bar(self) -> None:
        """
        initializes the nav bar
        args:
            none
        returns:
            none
        """
        self.nav_bar_box = toga.Box()
        self.back_button = toga.Button(
            text='Back',
            on_press=self.return_to[self.current_screen]
            )
        self.settings_button = toga.Button(
            text='Settings',
            on_press=self.init_settings_screen
            )
        self.nav_title = toga.Label(
            text=self.current_screen
        )

        # Add buttons to nav bar
        self.nav_bar_box.add(self.back_button)
        self.nav_bar_box.add(self.settings_button)
        self.nav_bar_box.add(self.nav_title)

    def init_home_screen(self) -> None:
        """
         initializes the home screen
         args:
             none
         returns:
             none
        """
        self.home_box = toga.Box()
        self.chat_list_GUI = toga.ScrollContainer(
            vertical=True,
            horizontal=False
        )

        # Add content to home screen box
        self.home_box.add(self.chat_list_GUI)

    def init_settings_screen(self) -> None:
        """
         initializes the settings screen
         args:
             none
         returns:
             none
        """
        self.settings_box = toga.Box()


class screen():
    """
    a template class for all screens
    """

    def __init__(self, main_box) -> None:
        """
        initializes the screen
        args:
             none
         returns:
             none
        """
        self.main_box: toga.Box = main_box
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

    def __init__(self, main_box) -> None:
        """
        initializes the home screen
        args:
            main_box (toga.Box): the main box of the app
        """
        super().__init__(main_box=main_box)
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
        self.chat_list_scroll.add(self.create_chat_list_segment(chats=chat_list, chat_load_per_segment_limit=10))

    def create_chat_list_segment(self, chats, chat_load_per_segment_limit) -> toga.Box:
        """
        creates a segment for the chat list
        args:
            chats (Chat): the chats to be displayed
         returns:
             box (toga.Box): a box containing all elements of this segment
         """
        segment = toga.Box()
        for chat in chats:
            chat_button = toga.Button(
                text=chat.name,
                on_press=self.display_chat_screen(chat)
            )  # TODO: maybe make into toga.box to make more complex / good looking
            # add content to chat box
            segment.add(chat_button)
        return segment

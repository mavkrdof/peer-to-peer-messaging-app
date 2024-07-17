"""
this module holds the GUI manager
"""
import logging
import toga
import toga.style
import toga.style.pack
import toga.constants
from peertopeermessagingapp.screens import home_screen, login_screen, create_account_screen, nav_bar, chat_screen, settings_screen, create_chat_screen


class GUI_manager:
    """
    manages the graphical user interface
    vars:
        current_screen: str
            the name of the current screen being displayed
            possible values: 'home', 'login', 'create_account',
            'nav_bar', 'chat_screen', 'create_chat'
        home_screen: peertopeermessagingapp.screens.home_screen
            the screen that displays all chats
        login_screen: peertopeermessagingapp.screens.login_screen
            the login screen
        create_account_screen: peertopeermessagingapp.screens.create_account_screen
            the create account screen
        nav_bar: peertopeermessagingapp.screens.nav_bar
            the navigation bar
        chat_screen: peertopeermessagingapp.screens.chat_screen
            the chat screen
        settings_screen: peertopeermessagingapp.screens.settings_screen
            the settings screen
        app: app.PeertoPeerMessagingApp
            the toga application instance
        main_box: toga.Box
            the main box of the app
        theme: dict[toga.constants]
            the overall theme for the app
    methods:
        __init__: none
            the initializer function
        start: none
            displays the initial screen of the gui
        back: none
            goes back to the previous screen
        change_screen: none
            changes the current screen being displayed
    """

    def __init__(self, app) -> None:
        """
        __init__ initilizes the GUI manager

        Args:
            app (peertopeermessagingapp.app.PeertoPeerMessagingApp): the toga application
        """
        self.app = app
        # static
        self.theme = {
            'font_color': toga.constants.BLACK,
            'background': toga.constants.GRAY,
            'middleground': toga.constants.SILVER,
            'foreground': toga.constants.LIGHTGREY,
        }
        self.current_screen = None
        self.main_box = toga.Box(
            style=toga.style.Pack(
                direction="column",
                background_color=self.theme['background']
                )
            )
        self.current_screen = ''
        # init screens
        self.login_screen = login_screen(
            GUI_manager=self
            )
        self.home_screen = home_screen(
            GUI_manager=self
            )
        self.chat_screen = chat_screen(
            GUI_manager=self
        )
        self.create_account_screen = create_account_screen(
            GUI_manager=self
        )
        self.settings_screen = settings_screen(
            GUI_manager=self
        )
        self.nav_bar = nav_bar(
            GUI_manager=self
        )
        self.create_chat_screen = create_chat_screen(
            GUI_manager=self
        )
        # init GUI
        self.login_screen.init_GUI()
        self.home_screen.init_GUI()
        self.chat_screen.init_GUI()
        self.create_account_screen.init_GUI()
        self.settings_screen.init_GUI()
        self.nav_bar.init_GUI()
        self.create_chat_screen.init_GUI()

    def start(self) -> None:
        """
        start starts the GUI
        """
        self.main_box.clear()
        self.nav_bar.display()
        self.change_screen(new_screen='login')

    def back(self, *args, **kwargs) -> None:
        """
        back retruns to the previous screen
        """
        match self.current_screen:
            case 'login':
                self.app.exit()
            case 'home':
                self.change_screen(new_screen='login')
            case 'create_account':
                self.change_screen(new_screen='login')
            case 'chat':
                self.change_screen(new_screen='home')
            case 'create_chat':
                self.change_screen(new_screen='home')
            case _:
                self.app.exit()

    def change_screen(self, new_screen, *args, **kwargs) -> None:
        """
        change_screen changes the screen being displayed

        Args:
            new_screen (str | toga.button): the nameo of the new screen or the button that was pressed
            if button, id must be in screen_dict
        """
        screen_dict = {
            'login': self.login_screen,
            'create_account': self.create_account_screen,
            'home': self.home_screen,
            'chat': self.chat_screen,
            'settings_screen': self.settings_screen,
            'cancel_create_chat': self.home_screen,
            'add_chat': self.create_chat_screen,
        }
        if isinstance(new_screen, str):
            new_screen_name = new_screen
        else:
            if isinstance(new_screen, toga.Button):
                if new_screen.id in screen_dict:
                    new_screen = new_screen.id
                else:
                    logging.error(
                        f'Error: {new_screen} is not a valid screen'
                    )
            else:
                logging.error(
                    f"Error: expected type 'str or toga.Button', got {type(new_screen)}"
                )

        # remove content from screen
        for content in self.main_box.children:
            if content.id == 'nav_bar':
                pass
            else:
                self.main_box.remove(content)
        # add content to screen
        screen_dict[new_screen_name].display()
        self.current_screen = new_screen_name.replace('_', ' ').capitalize()
        self.nav_bar.update()

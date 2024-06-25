"""
this module holds the GUI manager
"""
import toga
import toga.style
import toga.style.pack
from peertopeermessagingapp.screens import home_screen, login_screen, create_account_screen, nav_bar, chat_screen, settings_screen


class GUI_manager:
    """
    manages the graphical user interface
    vars:
        current_screen: str
            the name of the current screen being displayed
            possible values: 'home', 'login', 'create_account',
            'nav_bar', 'chat_screen'
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
        init main GUI manager class
        """
        self.app = app
        # static
        self.current_screen = None
        self.main_box = toga.Box(
            style=toga.style.Pack(
                direction="column"
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
        # init GUI
        self.login_screen.init_GUI()
        self.home_screen.init_GUI()
        self.chat_screen.init_GUI()
        self.create_account_screen.init_GUI()
        self.settings_screen.init_GUI()
        self.nav_bar.init_GUI()

    def start(self) -> None:
        self.main_box.clear()
        self.nav_bar.display()
        self.change_screen(new_screen='login')

    def back(self, *args, **kwargs) -> None:
        match self.current_screen:
            case 'login':
                self.app.exit()
            case 'home':
                self.change_screen(new_screen='login')
            case 'create_account':
                self.change_screen(new_screen='login')
            case 'chat':
                self.change_screen(new_screen='home')
            case _:
                self.app.exit()

    def change_screen(self, new_screen, *args, **kwargs) -> None:
        screen_dict = {
            'login': self.login_screen,
            'create_account': self.create_account_screen,
            'home': self.home_screen,
            'chat': self.chat_screen,
            'settings_screen': self.settings_screen,
        } # TODO Make work with multiple buttons per action could just add more segments
        if isinstance(new_screen, str):
            pass
        else:
            new_screen = new_screen.id
        for content in self.main_box.children:
            if content.id == 'nav_bar':
                pass
            else:
                self.main_box.remove(content)
        screen_dict[new_screen].display()
        self.current_screen = new_screen  # TODO: make look pretty when displayed - use dict to change from machine name to display name?
        self.nav_bar.update()

"""
this module holds the functions for the GUI
"""
from struct import pack
import toga
import toga.style


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
        self.main_box = toga.Box()
        self.current_screen = ''
        # init screens
        self.login_screen = login_screen(
            GUI_manager=self
            )
        self.home_screen = home_screen(
            GUI_manager=self
            )
        # TODO: finish screen init
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
        self.nav_bar.display()
        self.change_screen(new_screen=self.login_screen)

    def back(self, *args, **kwargs) -> None:
        pass

    def change_screen(self, new_screen) -> None:
        for content in self.main_box.children:
            if content.id == 'nav_bar':
                pass
            else:
                self.main_box.remove(content)
        new_screen.display()
        self.current_screen = new_screen.name  # TODO: make look pretty when displayed - use dict to change from machine name to display name?
        self.nav_bar.update()


class screen():
    """
    a template class for all screens
    """

    def __init__(self, GUI_manager, name) -> None:
        """
        initializes the screen
        args:
             none
         returns:
             none
        """
        self.GUI_manager = GUI_manager
        # static
        self.name = name
        self.box = toga.Box(id=self.name)

    def init_GUI(self) -> None:
        pass

    def update(self) -> None:
        pass

    def display(self) -> None:
        """
         displays the screen
         args:
             none
         returns:
             none
        """
        self.GUI_manager.main_box.add(self.box)



class home_screen(screen):
    """
    the screen that displays all chats
    """

    def __init__(self, GUI_manager) -> None:
        """
        initializes the home screen
        args:
            main_box (toga.Box): the main box of the app
        """
        super().__init__(GUI_manager=GUI_manager, name='home_screen')
        self.chat_scroll_segment_count = 0
        self.chat_load_per_segment_limit = 5
        self.max_chat_list_segments = 5

    def init_GUI(self) -> None:
        self.chat_list_scroll = toga.ScrollContainer(
            vertical=True,
            horizontal=False
        )
        # Add content to home screen box
        self.box.add(self.chat_list_scroll)

    def populate_chat_list(self, chat_list: list) -> None:
        """
        populates the chat list with chats
        args:
            chat_list (list): a list of chats to be displayed
        returns:
            none
        """
        if self.chat_scroll_segment_count >= self.max_chat_list_segments:
            pass  # TODO: implement max segments

        segment = self.create_chat_list_segment(
                start_index=self.chat_scroll_segment_count * self.chat_load_per_segment_limit,
                chats=chat_list,
                )
        if segment is None:
            return None
        else:
            self.chat_scroll_segment_count += 1
            self.chat_list_scroll.add(segment)

    def create_chat_list_segment(self, chats, start_index) -> toga.Box | None:
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
        else:
            # create segment
            segment = toga.Box()
            # fill segment
            # for chat in chats[start_index: final_index]:
            #     chat_button = toga.Button(
            #         text=chat.name,
            #         on_press=self.GUI_manager.chat_screen.display(chat)
            #     )  # TODO: maybe make into toga.box to make more good looking
            # add content to chat box
            # segment.add(chat_button)
            return segment


class nav_bar(screen):
    """
    the navigation bar
    """

    def __init__(self, GUI_manager) -> None:
        super().__init__(GUI_manager=GUI_manager, name='nav_bar')
        self.back_button_text = {
            'home': 'Logout',
            'create_account': 'Back',
            'chat': 'Home',
            'create_chat': 'Back to create chat',
            'login': 'Quit'
            # TODO: add more screens
        }

    def init_GUI(self) -> None:
        # create navigation bar
        # add buttons for each screen
        if self.GUI_manager.current_screen in self.back_button_text:
            back_text = self.back_button_text[self.GUI_manager.current_screen]
        else:
            back_text = ''
        self.back_button = toga.Button(
            text=back_text,
            on_press=self.GUI_manager.back
        )

        self.title = toga.Label(
            text=self.GUI_manager.current_screen
        )
        # add to box
        self.box.add(self.back_button)
        self.box.add(self.title)
    
    def update(self) -> None:
        self.title.text = self.GUI_manager.current_screen
        if self.GUI_manager.current_screen in self.back_button_text:
            back_text = self.back_button_text[self.GUI_manager.current_screen]
        else:
            back_text = ''
        self.back_button.text = back_text


class login_screen(screen):
    """
    the login screen
    """

    def __init__(self, GUI_manager) -> None:
        super().__init__(GUI_manager=GUI_manager, name='login')

    def init_GUI(self) -> None:
        self.__username_field = toga.TextInput()
        self.__username_label = toga.Label(
            text='USERNAME'
        )
        self.__password_field = toga.PasswordInput()
        self.__password_label = toga.Label(
            text='PASSWORD'
        )
        self.__login_button = toga.Button(
            text='LOGIN',
            on_press=self.validate_login
        )
        self.__create_account_button = toga.Button(
            text='CREATE ACCOUNT',
            on_press=self.GUI_manager.create_account_screen.display
        )
        # add content to box
        self.box.add(self.__username_field)
        self.box.add(self.__username_label)
        self.box.add(self.__password_field)
        self.box.add(self.__password_label)
        self.box.add(self.__login_button)
        self.box.add(self.__create_account_button)

    def validate_login(self) -> None:
        pass


class settings_screen(screen):
    """
    the settings screen
    """

    def __init__(self, GUI_manager) -> None:
        super().__init__(GUI_manager=GUI_manager, name='settings')

    def init_GUI(self) -> None:
        super().init_GUI()


class create_account_screen(screen):
    """
    the create account screen
    """

    def __init__(self, GUI_manager) -> None:
        super().__init__(GUI_manager=GUI_manager, name='create_account')

    def init_GUI(self) -> None:
        self.__username_field = toga.TextInput(
            placeholder='Enter username'
            )
        self.__username_label = toga.Label(
            text='Username:'
            )
        self.__password_field = toga.PasswordInput(
            placeholder='Enter password'
            )
        self.__password_label = toga.Label(
            text='Password:'
            )
        self.__confirm_password_field = toga.PasswordInput(
            placeholder='Confirm password'
            )
        self.__confirm_password_label = toga.Label(
            text='Confirm Password:'
             )
        self.__create_account_button = toga.Button(
            text='Create Account',
            on_press=self.GUI_manager.back
            )
        self.__cancel_button = toga.Button(
            text='Cancel',
            on_press=self.GUI_manager.back
            )
        self.box.add(self.__username_label)
        self.box.add(self.__username_field)
        self.box.add(self.__password_label)
        self.box.add(self.__password_field)
        self.box.add(self.__confirm_password_label)
        self.box.add(self.__confirm_password_field)
        self.box.add(self.__create_account_button)
        self.box.add(self.__cancel_button)


class chat_screen(screen):
    """
    the chat screen
    """

    def __init__(self, GUI_manager) -> None:
        super().__init__(GUI_manager=GUI_manager, name='chats')

    def init_GUI(self) -> None:
        super().init_GUI()

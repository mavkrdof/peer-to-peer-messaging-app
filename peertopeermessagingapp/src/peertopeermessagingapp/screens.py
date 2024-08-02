"""
this module holds all the different screens the GUI can display
"""
import logging
import toga
import toga.constants
import toga.style


class screen():
    """
    a template class for all screens
    vars:
    GUI_manager: GUI_manager
        the GUI manager instance
    name: str
        the name of the screen
    box: toga.Box
        the main box of the screen
    methods:
        __init__: none
            the initializer function
        init_GUI: none
            initializes the GUI elements of the screen
        update: none
            updates any dynamic elements on the screen (e.g. chat messages)
        display: none
            displays the screen
    """

    def __init__(self, GUI_manager, name) -> None:
        """
        initializes the screen
        args:
             GUI_manager: GUI_manager
                 the GUI manager instance
             name: str
                 the name of the screen
         returns:
             none
        """
        self.GUI_manager = GUI_manager
        # static
        self.name = name
        self.box = toga.Box(
            id=self.name,
            )
        self.logger = logging.getLogger(name=f'{__name__}:{self.name}')

    def init_GUI(self) -> None:
        """
        initializes the GUI elements of the screen
        args:
            none
        returns:
            none
        """
        pass

    def set_style(self):
        """
        set_style sets the style for all GUI elements
        """
        self.box.style.update(
            direction='column',
            background_color=self.GUI_manager.theme['background']
        )
        pass

    def add_to_box(self):
        """
        add_to_box adds GUI elements to the main box
        """
        pass

    def update(self) -> None:
        """
        updates dynamic elements on the screen
        args:
            none
        returns:
            none
        """
        self.set_style()
        self.box.refresh()

    def display(self) -> None:
        """
        displays the screen
        args:
            none
        returns:
            none
        """
        self.GUI_manager.main_box.add(self.box)
        self.update()

    def clear_gui(self) -> None:
        """
        clear_gui clears the GUI elements
        """
        self.box.clear()
        self.logger.info(msg='GUI cleared')


class home_screen(screen):
    """
    the screen that displays all chats
    vars:
        GUI_manager: GUI_manager
            the GUI manager instance
        name: str
            the name of the screen
        box: toga.Box
            the main box of the screen
    methods:
        __init__: none
            the initializer function
        init_GUI: none
            initializes the GUI elements of the screen
        update: none
            updates any dynamic elements on the screen (e.g. chat messages)
        display: none
            displays the screen
        populate_chat_list: none
            populates the list of chats on the screen
        create_chat_list_segment: none
                creates a segment for the chat list
    """

    def __init__(self, GUI_manager) -> None:
        """
        initializes the home screen
        args:
            GUI_manager: GUI_manager
                the GUI manager instance
        returns:
            none
        """
        super().__init__(GUI_manager=GUI_manager, name='home_screen')
        self.chat_buttons = []

    def init_GUI(self) -> None:
        """
        init_GUI initialises the GUI elements of the screen
        """
        self.create_title_box()
        self.populate_chat_list()
        # chat select
        self.chat_box = toga.Box()
        self.chat_list_scroll = toga.ScrollContainer(
            vertical=True,
            horizontal=False,
            content=self.chat_box
        )
        self.set_style()
        self.add_to_box()

    def set_style(self) -> None:
        self.chat_box.style.update(
            flex=1,
            direction='column',
            background_color=self.GUI_manager.theme['background']
        )
        self.chat_list_scroll.style.update(
            flex=1,
            direction='column',
            background_color=self.GUI_manager.theme['background']
        )
        self.title_box.style.update(
            flex=1,
            direction='row',
            background_color=self.GUI_manager.theme['middleground']
        )
        self.add_chat_button.style.update(
            flex=0.5,
            padding_right=10,
            color=self.GUI_manager.theme['font_color'],
            background_color=self.GUI_manager.theme['foreground']
        )
        for button in self.chat_buttons:
            button.style.update(
                flex=0.5,
                padding_right=10,
                color=self.GUI_manager.theme['font_color'],
                background_color=self.GUI_manager.theme['foreground']
            )
        super().set_style()

    def add_to_box(self) -> None:
        # add to title box
        self.title_box.add(self.add_chat_button)
        self.box.add(self.title_box)
        # add to main box
        self.box.add(self.chat_list_scroll)

    def create_title_box(self) -> None:
        """
        create_title_box creates the title box
        """
        self.title_box = toga.Box()
        self.add_chat_button = toga.Button(
            id="add_chat",
            text='Add Chat',
            on_press=self.GUI_manager.change_screen,
        )

    def populate_chat_list(self) -> None:
        """
        populates the chat list with chats
        args:
            chat_list (list): a list of chats to be displayed
        returns:
            none
        """
        chat_list: dict = self.GUI_manager.app.backend.user_data.get_chat_list()
        for key, chat in chat_list.items():
            chat_button = toga.Button(
                id=f'chat:{key}',
                text=f'{chat.icon}       {chat.name}',
                on_press=self.display_chat
            )
            self.chat_buttons.append(chat_button)
            self.chat_box.add(chat_button)

    def display_chat(self, button) -> None:
        self.GUI_manager.change_screen('chat')
        current_chat = button.id[5:]
        self.GUI_manager.current_chat = current_chat

    def update(self) -> None:
        self.chat_box.clear()
        self.populate_chat_list()
        super().update()


class nav_bar(screen):
    """
    the navigation bar
    vars:
        GUI_manager: GUI_manager
            the GUI manager instance
        name: str
            the name of the screen
        box: toga.Box
            the main box of the screen
    methods:
        __init__: none
            the initializer function
        init_GUI: none
            initializes the GUI elements of the screen
        update: none
            updates any dynamic elements on the screen (e.g. chat messages)
        display: none
            displays the screen
    """

    def __init__(self, GUI_manager) -> None:
        """
        initializes the navigation bar
        args:
            GUI_manager: GUI_manager
                the GUI manager instance
        returns:
            none
        """
        super().__init__(GUI_manager=GUI_manager, name='nav_bar')
        self.back_button_text = {
            'home': 'Logout',
            'create_account': 'Back',
            'chat': 'Home',
            'create_chat': 'Back to create chat',
            'login': 'Quit',
            'settings': 'Back'
        }

    def init_GUI(self) -> None:
        """
        init_GUI initialises the GUI elements of the screen
        """
        self.create_back_button()
        self.create_title()
        self.settings()
        self.add_to_box()
        self.set_style()

    def set_style(self):
        self.settings_button.style.update(
            padding=10,
            flex=0.2,
            color=self.GUI_manager.theme['font_color'],
            background_color=self.GUI_manager.theme['middleground']
        )
        self.title.style.update(
            padding=10,
            flex=0.6,
            text_align='center',
            font_size=15,
            color=self.GUI_manager.theme['font_color'],
            background_color=self.GUI_manager.theme['middleground']
        )
        self.back_button.style.update(
            padding=10,
            flex=0.2,
            color=self.GUI_manager.theme['font_color'],
            background_color=self.GUI_manager.theme['middleground']
        )
        self.box.style.update(
            direction='row',
            background_color=self.GUI_manager.theme['middleground']
        )

    def add_to_box(self) -> None:
        """
        add_to_box adds content to the screens main box
        """
        self.box.add(self.back_button)
        self.box.add(self.title)
        self.box.add(self.settings_button)

    def settings(self) -> None:
        """
        settings creates the settings button
        """
        self.settings_button = toga.Button(
            id='settings_screen',
            text='Settings',
            on_press=self.GUI_manager.change_screen,
        )

    def create_title(self) -> None:
        """
        create_title creates the title of the screen displayed
        """
        self.title = toga.Label(
            text=self.GUI_manager.current_screen,
        )

    def create_back_button(self) -> None:
        """
        create_back_button creates a back button
        """
        back_text = self.back_button_text[self.GUI_manager.current_screen.name]
        self.back_button = toga.Button(
            text=back_text,
            on_press=self.GUI_manager.back,
        )

    def update(self) -> None:
        """
        update the nav bar to reflect the current screen
        """
        self.title.text = self.GUI_manager.current_screen.name.replace('_', ' ').capitalize()
        if self.GUI_manager.current_screen.name in self.back_button_text:
            back_text = self.back_button_text[self.GUI_manager.current_screen.name]
        else:
            back_text = ''
        self.back_button.text = back_text
        super().update()


class login_screen(screen):
    """
    the login screen
    vars:
        GUI_manager: GUI_manager
            the GUI manager instance
        name: str
            the name of the screen
        box: toga.Box
            the main box of the screen
    methods:
        __init__: none
            the initializer function
        init_GUI: none
            initializes the GUI elements of the screen
        update: none
            updates any dynamic elements on the screen (e.g. chat messages)
        display: none
            displays the screen
        validate_login: none
            validates the login credentials
    """

    def __init__(self, GUI_manager) -> None:
        """
        __init__ initialises the login screen

        Args:
            GUI_manager (peertopeermessagingapp.screens.GUI_manager): the gui manager
        """
        super().__init__(GUI_manager=GUI_manager, name='login')

    def init_GUI(self) -> None:
        """
        init_GUI initializes the GUI elements of the screen
        """
        self.content_padding()
        self.login_error_field()
        self.username_entry_field()
        self.password_entry_field()
        self.buttons()
        # style and add to box
        self.set_style()
        self.add_content_to_box()

    def add_content_to_box(self) -> None:
        """
        add_content_to_box adds content to the login screens main box
        """
        self.__button_box.add(self.__login_button)
        self.__button_box.add(self.__create_account_button)
        # add content to content_box
        self.content_box.add(self.__username_box)
        self.content_box.add(self.__password_box)
        self.content_box.add(self.__login_error_label)
        self.content_box.add(self.__button_box)
        # add content and pad boxes
        self.box.add(self.left_pad_box)
        self.box.add(self.content_box)
        self.box.add(self.right_pad_box)

    def set_style(self):
        self.box.style.update(
            direction='row',
            background_color=self.GUI_manager.theme['background']
        )
        self.__button_box.style.update(
            direction='row',
            padding=10,
            flex=1,
            background_color=self.GUI_manager.theme['middleground']
        )
        self.__login_button.style.update(
            flex=0.5,
            padding_right=10,
            color=self.GUI_manager.theme['font_color'],
            background_color=self.GUI_manager.theme['foreground']
        )
        self.__create_account_button.style.update(
            flex=0.5,
            padding_right=10,
            color=self.GUI_manager.theme['font_color'],
            background_color=self.GUI_manager.theme['foreground']
        )
        self.__password_box.style.update(
            direction='row',
            padding=10,
            flex=1,
            background_color=self.GUI_manager.theme['middleground']
        )
        self.__password_field.style.update(
            flex=0.75,
            color=self.GUI_manager.theme['font_color'],
            background_color=self.GUI_manager.theme['foreground']
        )
        self.__password_label.style.update(
            flex=0.25,
            padding_right=10,
            text_align='center',
            font_size=20,
            font_weight='bold',
            font_family='monospace',
            color=self.GUI_manager.theme['font_color'],
            background_color=self.GUI_manager.theme['middleground']
        )
        self.__username_box.style.update(
            direction='row',
            padding=10,
            flex=1,
            alignment='center',
            background_color=self.GUI_manager.theme['middleground'],
        )
        self.__username_label.style.update(
            flex=0.25,
            padding_right=10,
            text_align='center',
            font_size=20,
            font_weight='bold',
            font_family='monospace',
            color=self.GUI_manager.theme['font_color'],
            background_color=self.GUI_manager.theme['middleground']
        )
        self.left_pad_box.style.update(
            flex=self.pad_width_percent,
            background_color=self.GUI_manager.theme['background']
        )
        self.right_pad_box.style.update(
            flex=self.pad_width_percent,
            background_color=self.GUI_manager.theme['background']
        )
        self.content_box.style.update(
            flex=self.content_width_percent,
            direction='column',
            background_color=self.GUI_manager.theme['middleground']
        )
        self.__login_error_label.style.update(
            flex=1,
            padding_right=10,
            text_align='center',
            font_size=10,
            font_weight='bold',
            font_family='monospace',
            color=self.GUI_manager.theme['font_color'],
            background_color=self.GUI_manager.theme['middleground']
        )

    def buttons(self) -> None:
        """
        buttons creates the login and create account buttons
        """
        self.__button_box = toga.Box()
        self.__login_button = toga.Button(
            text='LOGIN',
            on_press=self.validate_login,
        )
        self.__create_account_button = toga.Button(
            id='create_account',
            text='CREATE ACCOUNT',
            on_press=self.GUI_manager.change_screen,
        )
        super().set_style()

    def password_entry_field(self) -> None:
        """
        password_entry_field creates the password entry field
        """
        self.__password_box = toga.Box()
        self.__password_field = toga.PasswordInput()
        self.__password_label = toga.Label(
            text='Password',
        )
        self.__password_box.add(self.__password_label)
        self.__password_box.add(self.__password_field)

    def username_entry_field(self) -> None:
        """
        username_entry_field creates the username entry field
        """
        self.__username_box = toga.Box()
        self.__username_field = toga.TextInput(
            style=toga.style.Pack(
                flex=0.75,
                background_color=self.GUI_manager.theme['foreground']
            ),
            on_confirm=self.validate_login
        )
        self.__username_label = toga.Label(
            text='Username',
        )
        self.__username_box.add(self.__username_label)
        self.__username_box.add(self.__username_field)

    def login_error_field(self):
        self.__login_error_label = toga.Label(
            id='login_error_label',
            text=''
        )

    def content_padding(self) -> None:
        self.content_width_percent = 0.33
        self.pad_width_percent = (1-self.content_width_percent)/2
        self.left_pad_box = toga.Box()
        self.right_pad_box = toga.Box()
        self.content_box = toga.Box()

    def validate_login(self, *args, **kwargs) -> None:
        """
        validate_login validates the login credentials
        """
        username = self.__username_field.value
        password = self.__password_field.value
        valid = self.GUI_manager.app.backend.validate_login(username, password)
        match valid:
            case 1:
                self.__login_error_label.text = 'Successful login'
                self.GUI_manager.change_screen('home')
            case 2:
                self.__login_error_label.text = 'Invalid Password Formatting \nmust be integer-integer'
            case 3:
                self.__login_error_label.text = 'No stored account matches \nusername and password use create account instead'
            case _:
                self.__login_error_label.text = 'Unexpected value Returned'
                self.logger.error(
                    f'Expected valid with values \n1, 2 or 3. instead got {valid}'
                    )

    def display(self) -> None:
        """
        display displays the screen and logs the user out
        """
        super().display()
        # TODO: logout


class settings_screen(screen):
    """
    the settings screen
    vars:
        GUI_manager: GUI_manager
            the GUI manager instance
        name: str
            the name of the screen
        box: toga.Box
            the main box of the screen
    methods:
        __init__: none
            the initializer function
        init_GUI: none
            initializes the GUI elements of the screen
        update: none
            updates any dynamic elements on the screen (e.g. chat messages)
        display: none
            displays the screen
    """

    def __init__(self, GUI_manager) -> None:
        """
        __init__ initialises the settings screen

        Args:
            GUI_manager (peertopeermessagingapp.screens.GUI_manager): the gui manager
        """
        super().__init__(GUI_manager=GUI_manager, name='settings')
        self.valid_colors = [color for color in dir(toga.constants) if color.isalpha()]

    def set_style(self):  # TODO FIX
        self.__theme_customise_box.style.update(
            direction='column',
            padding=10,
            flex=1,
            background_color=self.GUI_manager.theme['middleground']
            )
        self.box.style.update(
            direction='column',
            background_color=self.GUI_manager.theme['background']
            )
        self.__background_color_select_box.style.update(
            direction='row',
            padding=10,
            flex=1,
            background_color=self.GUI_manager.theme['middleground']
            )
        self.__background_color_select_label.style.update(
                flex=0.25,
                padding_right=10,
                text_align='center',
                font_size=20,
                font_weight='bold',
                font_family='monospace',
                color=self.GUI_manager.theme['font_color'],
                background_color=self.GUI_manager.theme['middleground']
            )
        self.__background_color_select.style.update(
                flex=0.75,
                color=self.GUI_manager.theme['font_color'],
                background_color=self.GUI_manager.theme['foreground']
            ),  # type: ignore
        self.__middleground_color_select_box.style.update(
                direction='row',
                padding=10,
                flex=1,
                background_color=self.GUI_manager.theme['middleground']
            )
        self.__middleground_color_select_label.style.update(
                flex=0.25,
                padding_right=10,
                text_align='center',
                font_size=20,
                font_weight='bold',
                font_family='monospace',
                color=self.GUI_manager.theme['font_color'],
                background_color=self.GUI_manager.theme['middleground']
            )
        self.__foreground_color_select.style.update(
                flex=0.75,
                color=self.GUI_manager.theme['font_color'],
                background_color=self.GUI_manager.theme['foreground']
            ),  # type: ignore
        self.__middleground_color_select_label.style.update(
                flex=0.25,
                padding_right=10,
                text_align='center',
                font_size=20,
                font_weight='bold',
                font_family='monospace',
                color=self.GUI_manager.theme['font_color'],
                background_color=self.GUI_manager.theme['middleground']
            )
        self.__foreground_color_select.style.update(
                flex=0.75,
                color=self.GUI_manager.theme['font_color'],
                background_color=self.GUI_manager.theme['foreground']
            ),  # type: ignore
        self.__font_color_select_label.style.update(
                flex=0.25,
                padding_right=10,
                text_align='center',
                font_size=20,
                font_weight='bold',
                font_family='monospace',
                color=self.GUI_manager.theme['font_color'],
                background_color=self.GUI_manager.theme['middleground']
            )
        self.__font_color_select.style.update(
                flex=0.75,
                color=self.GUI_manager.theme['font_color'],
                background_color=self.GUI_manager.theme['foreground']
            ),  # type: ignore

    def add_to_box(self):
        # add to __foreground_color_select_box
        self.__foreground_color_select_box.add(self.__foreground_color_select_label)
        self.__foreground_color_select_box.add(self.__foreground_color_select)
        # add to __font_color_select_box
        self.__font_color_select_box.add(self.__font_color_select_label)
        self.__font_color_select_box.add(self.__font_color_select)
        # add to __middleground_color_select_box
        self.__middleground_color_select_box.add(self.__middleground_color_select_label)
        self.__middleground_color_select_box.add(self.__middleground_color_select)
        # add to __background_color_select_box
        self.__background_color_select_box.add(self.__background_color_select_label)
        self.__background_color_select_box.add(self.__background_color_select)
        # add to __theme_customise_box
        self.__theme_customise_box.add(self.__middleground_color_select_box)
        self.__theme_customise_box.add(self.__background_color_select_box)
        self.__theme_customise_box.add(self.__foreground_color_select_box)
        self.__theme_customise_box.add(self.__font_color_select_box)
        # add to main box
        self.box.add(self.__theme_customise_box)

    def init_GUI(self) -> None:
        """
        init_GUI initialises the GUI elements of the screen
        """
        # theme select
        self.__theme_customise_box = toga.Box()
        self.background_color_select()
        self.middleground_color_select()
        self.foreground_color_select()
        self.font_color_color_select()

        self.add_to_box()
        self.set_style()

    def background_color_select(self):
        self.__background_color_select_box = toga.Box()
        self.__background_color_select_label = toga.Label(
            text='Background Color',
        )
        self.__background_color_select = toga.Selection(
            id='background',
            on_change=self.change_theme,
            items=self.valid_colors,
        )

    def middleground_color_select(self) -> None:
        self.__middleground_color_select_box = toga.Box()
        self.__middleground_color_select_label = toga.Label(
            text='Middleground Color',
        )
        self.__middleground_color_select = toga.Selection(
            id='middleground',
            on_change=self.change_theme,
            items=self.valid_colors,
        )

    def foreground_color_select(self) -> None:
        self.__foreground_color_select_box = toga.Box()
        self.__foreground_color_select_label = toga.Label(
            text='Foreground Color',
        )
        self.__foreground_color_select = toga.Selection(
            id='foreground',
            on_change=self.change_theme,
            items=self.valid_colors,
        )

    def font_color_color_select(self) -> None:
        self.__font_color_select_box = toga.Box()
        self.__font_color_select_label = toga.Label(
            text='Font Color',
        )
        self.__font_color_select = toga.Selection(
            id='font_color',
            on_change=self.change_theme,
            items=self.valid_colors,
        )

    def change_theme(self, button: toga.Selection) -> None:
        self.GUI_manager.theme[button.id] = button.value.lower()  # type: ignore
        self.GUI_manager.update_screens()


class create_account_screen(screen):
    """
    the create account screen
    vars:
        GUI_manager: GUI_manager
            the GUI manager instance
        name: str
            the name of the screen
        box: toga.Box
            the main box of the screen
    methods:
        __init__: none
            the initializer function
        init_GUI: none
            initializes the GUI elements of the screen
        update: none
            updates any dynamic elements on the screen (e.g. chat messages)
        display: none
            displays the screen
    """

    def __init__(self, GUI_manager) -> None:
        """
        __init__ initilises the create account screen

        Args:
            GUI_manager (peertopeermessagingapp.screens.GUI_manager): the gui manager
        """
        super().__init__(GUI_manager=GUI_manager, name='create_account')

    def init_GUI(self) -> None:
        """
        init_GUI initialises the GUI elements of the screen
        """
        self.box.style = toga.style.Pack(
                direction='row'
                )
        self.already_have_account_field()
        self.password_output_field()
        self.content_padding()
        self.username_entry_field()
        self.password_entry_field()
        self.buttons()
        self.add_content_to_box()

    def add_content_to_box(self) -> None:
        """
        Adds content to the box by adding various elements to different sub-boxes.
        """
        # output field
        self.__output_box.add(self.__output_label)
        self.__output_box.add(self.__output_field)
        # button box
        self.__button_box.add(self.__cancel_button)
        self.__button_box.add(self.__create_account_button)
        # already have account
        self.__already_have_account_box.add(self.__already_have_account_label)
        self.__already_have_account_box.add(self.__already_have_account_checkbox)
        # password entry field
        self.__password_box.add(self.__password_label)
        self.__password_box.add(self.__password_field)
        # add content to content_box
        self.__content_box.add(self.__username_box)
        self.__content_box.add(self.__already_have_account_box)
        self.__content_box.add(self.__password_box)
        self.__content_box.add(self.__button_box)
        self.__content_box.add(self.__output_box)
        # add content and pad boxes
        self.box.add(self.__left_pad_box)
        self.box.add(self.__content_box)
        self.box.add(self.__right_pad_box)

    def set_style(self):
        self.box.style.update(
            direction='row',
            background_color=self.GUI_manager.theme['background']
        )
        self.__button_box.style.update(
            direction='row',
            padding=10,
            flex=1,
            background_color=self.GUI_manager.theme['middleground']
        )
        self.__cancel_button.style.update(
            flex=0.5,
            padding_right=10,
            color=self.GUI_manager.theme['font_color'],
            background_color=self.GUI_manager.theme['foreground']
        )
        self.__create_account_button.style.update(
            flex=0.5,
            padding_right=10,
            color=self.GUI_manager.theme['font_color'],
            background_color=self.GUI_manager.theme['foreground']
        )
        self.__password_box.style.update(
            direction='row',
            padding=10,
            flex=1,
            background_color=self.GUI_manager.theme['middleground']
        )
        self.__password_label.style.update(
            flex=0.75,
            color=self.GUI_manager.theme['font_color'],
            background_color=self.GUI_manager.theme['foreground']
        )
        self.__password_label.style.update(
            flex=0.25,
            padding_right=10,
            text_align='center',
            font_size=20,
            font_weight='bold',
            font_family='monospace',
            color=self.GUI_manager.theme['font_color'],
            background_color=self.GUI_manager.theme['middleground']
        )
        self.__username_box.style.update(
            direction='row',
            padding=10,
            flex=1,
            alignment='center',
            background_color=self.GUI_manager.theme['middleground'],
        )
        self.__username_field.style.update(
            flex=0.75,
            background_color=self.GUI_manager.theme['foreground']
        )
        self.__username_label.style.update(
            flex=0.25,
            padding_right=10,
            text_align='center',
            font_size=20,
            font_weight='bold',
            font_family='monospace',
            color=self.GUI_manager.theme['font_color'],
            background_color=self.GUI_manager.theme['middleground']
        )
        self.__left_pad_box.style.update(
            flex=self.pad_width_percent,
            background_color=self.GUI_manager.theme['background']
        )
        self.__right_pad_box.style.update(
            flex=self.pad_width_percent,
            background_color=self.GUI_manager.theme['background']
        )
        self.__content_box.style.update(
            flex=self.content_width_percent,
            direction='column',
            background_color=self.GUI_manager.theme['middleground']
        )
        self.__already_have_account_box.style.update(
            direction='row',
            background_color=self.GUI_manager.theme['middleground']
        )
        self.__already_have_account_label.style.update(
            flex=0.25,
            padding_right=10,
            text_align='center',
            font_size=20,
            font_weight='bold',
            font_family='monospace',
            color=self.GUI_manager.theme['font_color'],
            background_color=self.GUI_manager.theme['middleground']
        )
        self.__already_have_account_checkbox.style.update(
            flex=0.75,
            background_color=self.GUI_manager.theme['foreground']
        )
        self.__output_box.style.update(
            direction='row',
            padding=10,
            flex=1,
            alignment='center',
            background_color=self.GUI_manager.theme['middleground'],
        )
        self.__output_label.style.update(
            flex=0.25,
            padding_right=10,
            text_align='center',
            font_size=20,
            font_weight='bold',
            font_family='monospace',
            color=self.GUI_manager.theme['font_color'],
            background_color=self.GUI_manager.theme['middleground']
        )
        self.__username_box.style.update(
            direction='row',
            padding=10,
            flex=1,
            alignment='center',
            background_color=self.GUI_manager.theme['middleground'],
        )
        self.__username_field.style.update(
            flex=0.75,
            background_color=self.GUI_manager.theme['foreground']
        )
        self.__output_field.style.update(
            flex=0.25,
            padding_right=10,
            text_align='center',
            font_size=20,
            font_weight='bold',
            font_family='monospace',
            color=self.GUI_manager.theme['font_color'],
            background_color=self.GUI_manager.theme['middleground']
        )

    def buttons(self) -> None:
        """
        buttons adds buttons to the button box
        """
        self.__button_box = toga.Box()
        self.__cancel_button = toga.Button(
            id='login',
            text='Cancel',
            on_press=self.GUI_manager.change_screen,
        )
        self.__create_account_button = toga.Button(
            text='Create Account',
            on_press=self.create_account,
        )

    def already_have_account_field(self) -> None:
        self.__already_have_account_box = toga.Box()
        self.__already_have_account_checkbox = toga.Selection(
            items=[False, True],
            on_change=self.already_have_account
        )
        self.__already_have_account_label = toga.Label(
            text='Already have account'
        )

    def already_have_account(self, checkBox: toga.Selection) -> None:
        if checkBox.value:
            self.__password_label.text = 'Current Password'
        else:
            self.__password_label.text = 'Password Seed'

    def password_entry_field(self) -> None:
        """
        password_entry_field creates the password entry field
        """
        self.__password_box = toga.Box()
        self.__password_field = toga.PasswordInput()
        self.__password_label = toga.Label(
            text='Password Seed',
        )

    def username_entry_field(self) -> None:
        """
        Creates the username entry field with a box containing a text input field and a label.
        Sets the style of the box, text input, and label based on the GUI theme.
        """
        self.__username_box = toga.Box()
        self.__username_field = toga.TextInput(
            on_confirm=self.create_account
        )
        self.__username_label = toga.Label(
            text='Username',
        )
        self.__username_box.add(self.__username_label)
        self.__username_box.add(self.__username_field)

    def password_output_field(self) -> None:
        """
        password_entry_field creates the password entry field
        """
        self.__output_box = toga.Box()
        self.__output_field = toga.Label(
            text=''
        )
        self.__output_label = toga.Label(
            text='Your Password is:',
        )

    def content_padding(self) -> None:
        """
        content_padding generates the content padding for the box
        """
        self.content_width_percent = 0.33
        self.pad_width_percent = (1-self.content_width_percent)/2
        self.__left_pad_box = toga.Box()
        self.__right_pad_box = toga.Box()
        self.__content_box = toga.Box()

    def create_account(self, *args, **kwargs) -> None:
        """
        create_account activates all relevant backend functions to create an account
        """
        logging.debug('create account button pressed')
        if self.__already_have_account_checkbox.value:
            create_old_account_success = self.GUI_manager.app.backend.create_old_account()
            if create_old_account_success:
                self.logger.info('Account successfully Added')
            else:
                self.logger.error('Add account Failure')
        else:
            logging.debug('creating new account')
            self.__output_field.text = 'Generating...'
            try:
                password = int(self.__password_field.value)
                create_new_account_success = self.GUI_manager.app.backend.create_new_account(
                    password_seed=password,
                    username=self.__username_field.value
                )  # TODO make async
            except ValueError:
                create_new_account_success = None
            if create_new_account_success is None:
                self.logger.error('Create account Failure')
            else:
                self.logger.info('Account successfully created')
                self.__output_field.text = f'{create_new_account_success[0]}-{create_new_account_success[1]}'


class chat_screen(screen):  # TODO add message display
    """
    the chat screen
    vars:
        GUI_manager: GUI_manager
            the GUI manager instance
        name: str
            the name of the screen
        box: toga.Box
            the main box of the screen
    methods:
        __init__: none
            the initializer function
        init_GUI: none
            initializes the GUI elements of the screen
        update: none
            updates any dynamic elements on the screen (e.g. chat messages)
        display: none
            displays the screen
    """

    def __init__(self, GUI_manager) -> None:
        """
        __init__ initialises the chat screen

        Args:
            GUI_manager (peertopeermessagingapp.screens.GUI_manager): the GUI manager
        """
        super().__init__(GUI_manager=GUI_manager, name='chats')

    def init_GUI(self) -> None:
        """
        init_GUI initialises the GUI elements of the screen
        """
        super().init_GUI()
        self.create_message_bar()
        self.create_message_scroll()
        self.add_to_box()

    def add_to_box(self) -> None:
        # message bar
        self.__message_bar_box.add(self.__message_entry)
        self.__message_bar_box.add(self.__send_button)
        # box
        self.box.add(self.__message_bar_box)
        self.box.add(self.__message_scroll_box)

    def set_style(self):
        self.__message_bar_box.style.update(
            direction='row',
            background_color=self.GUI_manager.theme['middleground']
        )
        self.__message_entry.style.update(
            flex=1,
            background_color=self.GUI_manager.theme['foreground'],
            color=self.GUI_manager.theme['font_color']
        )
        self.__send_button.style.update(
            background_color=self.GUI_manager.theme['foreground'],
            color=self.GUI_manager.theme['font_color']
        )
        self.__message_scroll_box.style.update(
            direction='row',
            background_color=self.GUI_manager.theme['background']
        )

    def create_message_bar(self) -> None:
        self.__message_bar_box = toga.Box(
            id='message_bar_box',
        )
        self.__message_entry = toga.TextInput(
            id='message_entry',
        )
        self.__send_button = toga.Button(
            id='send_button',
            text='Send',
            on_press=self.send_message,
        )

    def create_message_scroll(self) -> None:
        self.__message_scroll_box = toga.Box(
            id='message_scroll_box',
        )

    def send_message(self, *args, **kwargs) -> None:
        """
        send_message activates relevant backend functions to send a message
        """
        message = self.__message_entry.value
        chat = self.GUI_manager.current_chat
        self.GUI_manager.app.backend.send_message(message, chat)


class create_chat_screen(screen):
    """
    the create account screen
    vars:
        GUI_manager: GUI_manager
            the GUI manager instance
        name: str
            the name of the screen
        box: toga.Box
            the main box of the screen
    methods:
        __init__: none
            the initializer function
        init_GUI: none
            initializes the GUI elements of the screen
        update: none
            updates any dynamic elements on the screen (e.g. chat messages)
        display: none
            displays the screen
    """

    def __init__(self, GUI_manager) -> None:
        """
        __init__ initilises the create account screen

        Args:
            GUI_manager (peertopeermessagingapp.screens.GUI_manager): the GUI manager
        """
        super().__init__(GUI_manager=GUI_manager, name='create_chat')

    def init_GUI(self) -> None:
        """
        init_GUI initilizes the GUI elements of the screen
        """
        self.content_padding()
        self.name_entry_field()
        self.icon_entry_field()
        self.buttons()
        self.add_content_to_box()

    def add_content_to_box(self) -> None:
        """
        add_content_to_box adds the content of the screen to the box and sub boxes
        """
        # name
        self.__name_box.add(self.__name_label)
        self.__name_box.add(self.__name_field)
        # icon entry
        self.__icon_box.add(self.__icon_label)
        self.__icon_box.add(self.__icon_field)
        # buttons
        self.__button_box.add(self.__cancel_button)
        self.__button_box.add(self.__create_chat_button)
        # add content to content_box
        self.content_box.add(self.__name_box)
        self.content_box.add(self.__icon_box)
        self.content_box.add(self.__button_box)
        # add content and pad boxes
        self.box.add(self.left_pad_box)
        self.box.add(self.content_box)
        self.box.add(self.right_pad_box)

    def set_style(self) -> None:
        self.box.style.update(
            direction='row',
            background_color=self.GUI_manager.theme['background']
        )
        self.__button_box.style.update(
            direction='row',
            padding=10,
            flex=1,
            background_color=self.GUI_manager.theme['middleground']
        )
        self.__cancel_button.style.update(
            flex=0.5,
            padding_right=10,
            color=self.GUI_manager.theme['font_color'],
            background_color=self.GUI_manager.theme['foreground']
        )
        self.__create_chat_button.style.update(
            flex=0.5,
            padding_right=10,
            color=self.GUI_manager.theme['font_color'],
            background_color=self.GUI_manager.theme['foreground']
        )
        self.__icon_box.style.update(
            direction='row',
            padding=10,
            flex=1,
            background_color=self.GUI_manager.theme['middleground']
        )
        self.__icon_field.style.update(
            flex=0.75,
            color=self.GUI_manager.theme['font_color'],
            background_color=self.GUI_manager.theme['foreground']
        )
        self.__icon_label.style.update(
            flex=0.25,
            padding_right=10,
            text_align='center',
            font_size=20,
            font_weight='bold',
            font_family='monospace',
            color=self.GUI_manager.theme['font_color'],
            background_color=self.GUI_manager.theme['middleground']
        )
        self.__name_box.style.update(
            direction='row',
            padding=10,
            flex=1,
            alignment='center',
            background_color=self.GUI_manager.theme['middleground'],
        )
        self.__name_field.style.update(
            flex=0.75,
            background_color=self.GUI_manager.theme['foreground']
        )
        self.__name_label.style.update(
            flex=0.25,
            padding_right=10,
            text_align='center',
            font_size=20,
            font_weight='bold',
            font_family='monospace',
            color=self.GUI_manager.theme['font_color'],
            background_color=self.GUI_manager.theme['middleground']
        )
        self.left_pad_box.style.update(
            flex=self.pad_width_percent,
            background_color=self.GUI_manager.theme['background']
        )
        self.right_pad_box.style.update(
            flex=self.pad_width_percent,
            background_color=self.GUI_manager.theme['background']
        )
        self.content_box.style.update(
            flex=self.content_width_percent,
            direction='column',
            background_color=self.GUI_manager.theme['middleground']
        )

    def buttons(self) -> None:
        """
        buttons creates the buttons for the create chat screen
        """
        self.__button_box = toga.Box()
        self.__cancel_button = toga.Button(
            id='cancel_create_chat',
            text='HOME',
            on_press=self.GUI_manager.change_screen,
        )
        self.__create_chat_button = toga.Button(
            text='CREATE CHAT',
            on_press=self.create_chat,
        )

    def icon_entry_field(self) -> None:
        """
        icon_entry_field creates the icon entry field and its container
        """
        self.__icon_box = toga.Box()
        self.__icon_field = toga.TextInput()
        self.__icon_label = toga.Label(
            text='Icon',
        )

    def name_entry_field(self) -> None:
        """
        Generates a name entry field in the GUI with a label and input box for the user to enter the chats name.
        """
        self.__name_box = toga.Box()
        self.__name_field = toga.TextInput(
            on_confirm=self.create_chat
        )
        self.__name_label = toga.Label(
            text='Name',
        )

    def content_padding(self) -> None:
        """
        Generate a padding around the content box.
        """
        self.content_width_percent = 0.33
        self.pad_width_percent = (1-self.content_width_percent)/2
        self.left_pad_box = toga.Box()
        self.right_pad_box = toga.Box()
        self.content_box = toga.Box()

    def create_chat(self, *args, **kwargs) -> None:
        """
        Create a chat with the given name and icon.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        name = self.__name_field.value
        icon = self.__icon_field.value
        self.GUI_manager.app.backend.user_data.add_chat(name, icon)

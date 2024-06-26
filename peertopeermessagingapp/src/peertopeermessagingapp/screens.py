"""
this module holds all the different screens the GUI can display
"""
import toga
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
            style=toga.style.Pack(
                direction='column',
                background_color=self.GUI_manager.theme['background']
                )
            )

    def init_GUI(self) -> None:
        """
        initializes the GUI elements of the screen
        args:
            none
        returns:
            none
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
        self.chat_scroll_segment_count = 0
        self.chat_load_per_segment_limit = 5
        self.max_chat_list_segments = 5

    def init_GUI(self) -> None:
        self.chat_list_scroll = toga.ScrollContainer(
            vertical=True,
            horizontal=False,
            style=toga.style.Pack(
                flex=1,
                direction='column',
                background_color=self.GUI_manager.theme['background']
            )
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
            chats: [Chat]
                the chats to be displayed
            start_index: int
                the index of the first chat to be displayed
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
            for chat in chats[start_index: final_index]:
                chat_button = toga.Button(
                    id=chat.id,
                    text=chat.name,
                    on_press=self.GUI_manager.chat_screen.display,
                    style=toga.style.Pack(
                        flex=1,
                        direction='row',
                        padding_left=10,
                        background_color=self.GUI_manager.theme['middleground'],
                        color=self.GUI_manager.theme['font_color']
                    )
                )  # TODO: maybe make into toga.box to make more good looking
            # add content to chat box
            segment.add(chat_button)
            return segment


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
            'login': 'Quit'
            # TODO: add more screens
        }

    def init_GUI(self) -> None:
        """
        initializes the navigation bar
        args:
            none
        returns:
            none
        """
        self.box.style = toga.style.Pack(
            direction='row',
            background_color=self.GUI_manager.theme['middleground']
        )
        self.create_back_button()
        self.create_title()
        self.settings()
        self.add_content()

    def add_content(self) -> None:
        self.box.add(self.back_button)
        self.box.add(self.title)
        self.box.add(self.settings_button)

    def settings(self) -> None:
        self.settings_button = toga.Button(
            id='settings_screen',
            text='Settings',
            on_press=self.GUI_manager.change_screen,
            style=toga.style.Pack(
                padding=10,
                flex=0.2,
                color=self.GUI_manager.theme['font_color'],
                background_color=self.GUI_manager.theme['middleground']
            )
        )

    def create_title(self) -> None:
        self.title = toga.Label(
            text=self.GUI_manager.current_screen,
            style=toga.style.Pack(
                padding=10,
                flex=0.6,
                text_align='center',
                font_size=15,
                color=self.GUI_manager.theme['font_color'],
                background_color=self.GUI_manager.theme['middleground']
            )
        )

    def create_back_button(self) -> None:
        if self.GUI_manager.current_screen in self.back_button_text:
            back_text = self.back_button_text[self.GUI_manager.current_screen]
        else:
            back_text = ''
        self.back_button = toga.Button(
            text=back_text,
            on_press=self.GUI_manager.back,
            style=toga.style.Pack(
                padding=10,
                flex=0.2,
                color=self.GUI_manager.theme['font_color'],
                background_color=self.GUI_manager.theme['middleground']
            )
        )

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
        super().__init__(GUI_manager=GUI_manager, name='login')

    def init_GUI(self) -> None:
        self.box.style = toga.style.Pack(
                direction='row'
                )
        self.content_padding()
        self.username_entry_field()
        self.password_entry_field()
        self.buttons()
        self.add_content_to_box()

    def add_content_to_box(self) -> None:
        self.__button_box.add(self.__login_button)
        self.__button_box.add(self.__create_account_button)
        # add content to content_box
        self.content_box.add(self.__username_box)
        self.content_box.add(self.__password_box)
        self.content_box.add(self.__button_box)
        # add content and pad boxes
        self.box.add(self.left_pad_box)
        self.box.add(self.content_box)
        self.box.add(self.right_pad_box)

    def buttons(self) -> None:
        self.__button_box = toga.Box(
            style=toga.style.Pack(
                direction='row',
                padding=10,
                flex=1,
                background_color=self.GUI_manager.theme['middleground']
            )
        )
        self.__login_button = toga.Button(
            text='LOGIN',
            on_press=self.validate_login,
            style=toga.style.Pack(
                flex=0.5,
                padding_right=10,
                color=self.GUI_manager.theme['font_color'],
                background_color=self.GUI_manager.theme['foreground']
            ),
        )
        self.__create_account_button = toga.Button(
            id='create_account',
            text='CREATE ACCOUNT',
            on_press=self.GUI_manager.change_screen,
            style=toga.style.Pack(
                flex=0.5,
                padding_right=10,
                color=self.GUI_manager.theme['font_color'],
                background_color=self.GUI_manager.theme['foreground']
            ),
        )

    def password_entry_field(self) -> None:
        self.__password_box = toga.Box(
            style=toga.style.Pack(
                direction='row',
                padding=10,
                flex=1,
                background_color=self.GUI_manager.theme['middleground']
            )
        )
        self.__password_field = toga.PasswordInput(
            style=toga.style.Pack(
                flex=0.75,
                color=self.GUI_manager.theme['font_color'],
                background_color=self.GUI_manager.theme['foreground']
            ),
        )
        self.__password_label = toga.Label(
            text='Password',
            style=toga.style.Pack(
                flex=0.25,
                padding_right=10,
                text_align='center',
                font_size=20,
                font_weight='bold',
                font_family='monospace',
                color=self.GUI_manager.theme['font_color'],
                background_color=self.GUI_manager.theme['middleground']
            )
        )
        self.__password_box.add(self.__password_label)
        self.__password_box.add(self.__password_field)

    def username_entry_field(self) -> None:
        self.__username_box = toga.Box(
            style=toga.style.Pack(
                direction='row',
                padding=10,
                flex=1,
                alignment='center',
                background_color=self.GUI_manager.theme['middleground'],
            )
        )
        self.__username_field = toga.TextInput(
            style=toga.style.Pack(
                flex=0.75,
                background_color=self.GUI_manager.theme['foreground']
            ),
            on_confirm=self.validate_login
        )
        self.__username_label = toga.Label(
            text='Username',
            style=toga.style.Pack(
                flex=0.25,
                padding_right=10,
                text_align='center',
                font_size=20,
                font_weight='bold',
                font_family='monospace',
                color=self.GUI_manager.theme['font_color'],
                background_color=self.GUI_manager.theme['middleground']
            )
        )
        self.__username_box.add(self.__username_label)
        self.__username_box.add(self.__username_field)

    def content_padding(self) -> None:
        content_width_percent = 0.33
        pad_width_percent = (1-content_width_percent)/2
        self.left_pad_box = toga.Box(
            style=toga.style.Pack(
                flex=pad_width_percent,
                background_color=self.GUI_manager.theme['background']
            )
        )
        self.right_pad_box = toga.Box(
            style=toga.style.Pack(
                flex=pad_width_percent,
                background_color=self.GUI_manager.theme['background']
            )
        )
        self.content_box = toga.Box(
            style=toga.style.Pack(
                flex=content_width_percent,
                direction='column',
                background_color=self.GUI_manager.theme['middleground']
            )
        )

    def validate_login(self, *args, **kwargs) -> None:
        valid = True  # TODO: connect to back end
        if valid:
            self.GUI_manager.change_screen('home')

    def display(self) -> None:
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
        super().__init__(GUI_manager=GUI_manager, name='settings')

    def init_GUI(self) -> None:
        super().init_GUI()


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
        super().__init__(GUI_manager=GUI_manager, name='create_account')

    def init_GUI(self) -> None:
        self.box.style = toga.style.Pack(
                direction='row'
                )
        self.content_padding()
        self.username_entry_field()
        self.password_entry_field()
        self.buttons()
        self.add_content_to_box()

    def add_content_to_box(self) -> None:
        self.__button_box.add(self.__cancel_button)
        self.__button_box.add(self.__create_account_button)
        # add content to content_box
        self.content_box.add(self.__username_box)
        self.content_box.add(self.__password_box)
        self.content_box.add(self.__button_box)
        # add content and pad boxes
        self.box.add(self.left_pad_box)
        self.box.add(self.content_box)
        self.box.add(self.right_pad_box)

    def buttons(self) -> None:
        self.__button_box = toga.Box(
            style=toga.style.Pack(
                direction='row',
                padding=10,
                flex=1,
                background_color=self.GUI_manager.theme['middleground']
            )
        )
        self.__cancel_button = toga.Button(
            id='login',
            text='LOGIN',
            on_press=self.GUI_manager.change_screen,
            style=toga.style.Pack(
                flex=0.5,
                padding_right=10,
                color=self.GUI_manager.theme['font_color'],
                background_color=self.GUI_manager.theme['foreground']
            ),
        )
        self.__create_account_button = toga.Button(
            text='CREATE ACCOUNT',
            on_press=self.create_account,
            style=toga.style.Pack(
                flex=0.5,
                padding_right=10,
                color=self.GUI_manager.theme['font_color'],
                background_color=self.GUI_manager.theme['foreground']
            ),
        )

    def password_entry_field(self) -> None:
        self.__password_box = toga.Box(
            style=toga.style.Pack(
                direction='row',
                padding=10,
                flex=1,
                background_color=self.GUI_manager.theme['middleground']
            )
        )
        self.__password_field = toga.PasswordInput(
            style=toga.style.Pack(
                flex=0.75,
                color=self.GUI_manager.theme['font_color'],
                background_color=self.GUI_manager.theme['foreground']
            ),
        )
        self.__password_label = toga.Label(
            text='Password',
            style=toga.style.Pack(
                flex=0.25,
                padding_right=10,
                text_align='center',
                font_size=20,
                font_weight='bold',
                font_family='monospace',
                color=self.GUI_manager.theme['font_color'],
                background_color=self.GUI_manager.theme['middleground']
            )
        )
        self.__password_box.add(self.__password_label)
        self.__password_box.add(self.__password_field)

    def username_entry_field(self) -> None:
        self.__username_box = toga.Box(
            style=toga.style.Pack(
                direction='row',
                padding=10,
                flex=1,
                alignment='center',
                background_color=self.GUI_manager.theme['middleground'],
            )
        )
        self.__username_field = toga.TextInput(
            style=toga.style.Pack(
                flex=0.75,
                background_color=self.GUI_manager.theme['foreground']
            ),
            on_confirm=self.create_account
        )
        self.__username_label = toga.Label(
            text='Username',
            style=toga.style.Pack(
                flex=0.25,
                padding_right=10,
                text_align='center',
                font_size=20,
                font_weight='bold',
                font_family='monospace',
                color=self.GUI_manager.theme['font_color'],
                background_color=self.GUI_manager.theme['middleground']
            )
        )
        self.__username_box.add(self.__username_label)
        self.__username_box.add(self.__username_field)

    def content_padding(self) -> None:
        content_width_percent = 0.33
        pad_width_percent = (1-content_width_percent)/2
        self.left_pad_box = toga.Box(
            style=toga.style.Pack(
                flex=pad_width_percent,
                background_color=self.GUI_manager.theme['background']
            )
        )
        self.right_pad_box = toga.Box(
            style=toga.style.Pack(
                flex=pad_width_percent,
                background_color=self.GUI_manager.theme['background']
            )
        )
        self.content_box = toga.Box(
            style=toga.style.Pack(
                flex=content_width_percent,
                direction='column',
                background_color=self.GUI_manager.theme['middleground']
            )
        )

    def create_account(self, *args, **kwargs) -> None:
        pass


class chat_screen(screen):
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
        super().__init__(GUI_manager=GUI_manager, name='chats')

    def init_GUI(self) -> None:
        super().init_GUI()

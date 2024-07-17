import time


class Chat:
    """
    Methods:
        create_chat: name, icon
            creates the chat
        add_user: user_id
            adds a user to the chat
        delete_chat: none
            deletes the chat
    Vars:
        members: list[]
            the members in the chat
        name: str
            the name of the chat
        identifier: str
            the id of the chat
    """

    def __init__(self) -> None:
        """
        __init__ initialises the chat data object
        """
        self.members = None
        self.name = None
        self.identifier = None
        self.icon_max_len = 4
        self.users: list = []

    def create_chat(self, name: str, icon: str) -> None:
        """
        create_chat creates a new chat

        Args:
            name (str): the name of the chat
            icon (str): an icon to display for the chat
        """
        if isinstance(name, str):
            self.name = name
            if isinstance(icon, str):
                if len(icon) <= self.icon_max_len:
                    self.icon = icon
                    # set id
                    self.identifier = f'{name}{time.time}'

    def add_user(self, user_id: str) -> None:
        """
        add_user adds a user to the chat

        Args:
            user_id (str): the id of the user to add
        """
        self.users.append(user_id)

    def delete_chat(self) -> None:
        """
        delete_chat deletes the chat
        """
        pass

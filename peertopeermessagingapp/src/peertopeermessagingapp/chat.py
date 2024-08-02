import logging
import time
from peertopeermessagingapp.message import message


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
        self.name = None  # TODO initialise here
        self.identifier = None
        self.icon_max_len = 4
        self.users: list = []
        self.logger = logging.getLogger(name='{__name__}:{name}')
        self.__messages: list[message] = []

    def convert_message_to_json_compatible(self) -> list[dict]:
        json_compatible = []
        for msg in self.__messages:
            json_compatible.append(msg.convert_to_dict())
        return json_compatible

    def convert_to_dict(self) -> dict:
        json_compatible_message_list: list[dict] = self.convert_message_to_json_compatible()
        chat_dict = {
            'members': self.members,
            'name': self.name,
            'icon_max_len': self.icon_max_len,
            'users': self.users,
            'message': json_compatible_message_list
        }
        return chat_dict

    def send_message(self, message: message) -> None:
        self.__messages.append(message)

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

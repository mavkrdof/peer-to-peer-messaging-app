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
        get_messages: none
            gets the messages
        convert_to_dict: none
            converts the chat to a dict
        convert_message_to_json_compatible: none
            converts the messages to json compatible 
    attributes:
        members: list[]
            the members in the chat
        name: str
            the name of the chat
        identifier: str
            the id of the chat
        icon_max_len: int
            the max length of the icon
        users: list[]
            the users in the chat
        logger: logging object
            the error and info logger for the chat class
        __messages: list[message]
            the messages in the chat
    """

    def __init__(self, app) -> None:
        """
        __init__ initialises the chat data object
        attributes:
            members: list[]
                the members in the chat
            name: str
                the name of the chat
            identifier: str
                the id of the chat
            icon_max_len: int
                the max length of the icon
            users: list[]
                the users in the chat
            logger: logging object
                the error and info logger for the chat class
            __messages: list[message]
                the messages in the chat
        """
        self.app = app
        self.members = None
        self.name = 'chat'  # TODO initialise here
        self.identifier = None
        self.icon_max_len = 4
        self.users: list = []
        self.logger = logging.getLogger(name='{__name__}:{name}')
        self.__messages: list[message] = []

    def get_messages(self) -> list[message]:
        """
        get_messages gets the messages in the chat

        Returns:
            list[message]: a list of the messages in the chat
        """
        return self.__messages

    def convert_message_to_json_compatible(self) -> list[dict]:
        """
        convert_message_to_json_compatible converts the messages to be json compatible

        Returns:
            list[dict]: a list of the json compatible messages in the chat
        """
        json_compatible = []
        for msg in self.__messages:
            json_compatible.append(msg.convert_to_dict())
        return json_compatible

    def convert_to_dict(self) -> dict:
        """
        convert_to_dict converts the chat to a dict

        Returns:
            dict: a dictionary storing the data of the chat
        """
        json_compatible_message_list: list[dict] = self.convert_message_to_json_compatible()
        chat_dict = {
            'members': self.members,
            'name': self.name,
            'icon_max_len': self.icon_max_len,
            'users': self.users,
            'message': json_compatible_message_list
        }
        return chat_dict

    def send_message(self, message: message) -> None:  # TODO trigger syncing of message data not just storing message
        """
        send_message sends a message to the chat

        Args:
            message (message): the message to send
        """
        self.logger.info('Sending message...')
        self.logger.debug('Storing message...')
        self.__messages.append(message)
        self.logger.debug('Successfully stored message')
        self.logger.info('Sending message...')
        # self.logger.info('Successfully sent message')

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
        self.app.network_manager.add_address(name=user_id, ip='', port=0)

    def delete_chat(self) -> None:  # TODO
        """
        delete_chat deletes the chat
        """
        pass

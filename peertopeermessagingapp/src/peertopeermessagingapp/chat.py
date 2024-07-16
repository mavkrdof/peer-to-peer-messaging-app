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
        self.members = None
        self.name = None
        self.identifier = None
        self.icon_max_len = 4

    def create_chat(self, name: str, icon):
        """
        creates the chat
        args:
            name: str
                the name of the chat
            icon: str
                the icon of the chat
        """
        if isinstance(name, str):
            self.name = name
            if isinstance(icon, str):
                if len(icon) <= self.icon_max_len:
                    self.icon = icon
                    # set id
                    self.identifier = time.time

    def add_user(user_id):
        pass

    def delete_chat():
        pass
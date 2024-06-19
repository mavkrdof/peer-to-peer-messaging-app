import toga


class chat:
    """
    is an outline of a chat function
    vars:
    icon_path: str
        the path to the chat icon
    name: str
        the display name of the chat
    uniqueID: str
        a unique identifier for the chat
    messages: list[message]
        a list of message sent in chat
    methods:
        __init__: none
            the init func
        open: none
            opens a gui for the chat
    """

    def __init__(self, icon_path, name, uniqueID) -> None:
        icon_path = icon_path
        name = name
        uniqueID = uniqueID
        # default empty
        self.messages = []

    def open():
        """
        opens a gui for the chat
        Args:
            none
        Returns: none
        """
        chat_box = toga.Box()
        message_contianer = toga.ScrollContainer(
            id=None,
            style=None,
            horizontal=True,
            vertical=True,
            on_scroll=None,
            content=None
            )
        for message in self.messages:
            message_list.append(
                toga.label(
                    "Click me")
            )

    def message_box(message):
        """
        parses the message to be displayed
        args:
        message: Message
            a message
        returns: toga.box
            returns a displayable message
        """
        slice = toga.Box()
        message_left = toga.label(text='')
        message_right = toga.label(text='')
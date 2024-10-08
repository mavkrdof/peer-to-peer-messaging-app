"""
this module holds the message class
"""
import peertopeermessagingapp.RSA_decrypt as RSA_decrypt
import peertopeermessagingapp.RSA_encrypt as RSA_encrypt
import json
import logging


class message:
    """
    attrs:
        content: str
            the plain text of the message
        user: <user_data>
            the user that the message is accessed by.
        sender: str
            the id of the user the message is from
        sent_time_stamp: int
            the time at which message was sent
        received_time_stamp: int
            the time at which the message was received
        message_id: str
            the id of the message
        app: app
            the main app object
        logger: logging object
            the error and info logger for the message class
    methods:
        read_in: none
            reads the message in from storage
        store: none
            stores the message
        convert_to_dict: dict
            converts the message to a dictionary
        encrypt: none  # TODO May be able to remove
            encrypts relevant data for storage
        decrypt: list[int]  # TODO May be able to remove
            decrypts message
    """

    def __init__(self, chat, message_id: str, content: str, app, sender='', sent_time=0.0, received_time=0.0) -> None:
        """
        __init__ initializes the message data object

        attrs:
            content: str
                the plain text of the message
            user: <user_data>
                the user that the message is accessed by.
            sender: str
                the id of the user the message is from
            sent_time_stamp: int
                the time at which message was sent
            received_time_stamp: int
                the time at which the message was received
            message_id: str
                the id of the message
            app: app
                the main app object
            logger: logging object
                the error and info logger for the message class
        """
        self.app = app
        self.content: str = content
        self.chat = chat
        self.sender: str = sender
        self.sent_time_stamp: float = sent_time
        self.received_time_stamp: float = received_time
        self.message_id: str = message_id
        self.logger = logging.getLogger(name='{__name__}:{self.chat}:{self.id}')

    def convert_to_dict(self) -> dict:
        """
        convert_to_dict converts the message to a dictionary

        Returns:
            dict: message data stored in a dictionary
        """
        message_dict = {
            'text': self.content,
            'chat': self.chat.identifier,
            'sender': self.sender,
            'sent_time_stamp': self.sent_time_stamp,
            'received_time_stamp': self.received_time_stamp,
            'id': self.message_id
        }
        return message_dict

    def read_in(self) -> None:
        """
        read_in reads in the message from storage
        """
        message_raw = self.chat.message_list[self.message_id]
        self.decrypt(message_data=message_raw)  # todo might not have to decrypt

    def send(self) -> None:
        message = self.convert_to_dict()
        self.app.network_manager.add_message_to_queue(message)

    def store(self) -> None:
        """
        store stores the message in encrypted form
        """
        data = self.encrypt()
        if data is None:
            self.logger.warn(
                msg='Storing invalid Message data likely due to encryption error.'
                )
        self.chat.message_list.append(data)

    def encrypt(self) -> list[int] | None:
        """
        encrypt converts the message to json and encrypts it

        Returns:
            list[int] | None: the encrypted message
        """
        message_data = {
            'plain_text': self.content,
            'sender': self.sender,
            'sent_time_stamp': self.sent_time_stamp,
            'received_time_stamp': self.received_time_stamp
        }
        message_data_json = json.dumps(obj=message_data)
        try:
            encrypted = RSA_encrypt.encrypt_data(
                public_key_n=self.chat.public_key[0],
                public_key_e=self.chat.public_key[1],
                plain_text=message_data_json
                )
        except ValueError as error:
            self.logger.error(msg=error)
            return None
        return encrypted

    def decrypt(self, message_data: list[int]) -> None:
        """
        decrypt decrypts the message data and assigns the data

        Args:
            message_data (list[int]): the data to decrypt as a list of integers
        """
        decrypted_raw: str = RSA_decrypt.decrypt_data(
            encrypted=message_data,
            private_key_d=self.chat.private_key[1],
            private_key_n=self.chat.private_key[0]
            )
        print(decrypted_raw)
        decrypted: dict = json.loads(decrypted_raw)

        # check for valid message and assign data
        if 'plain_text' in decrypted:
            self.content = decrypted['plain_text']
            # TODO: decide if plain_test should default to NONE or '' - must update tests
        else:
            self.logger.warning(
                msg=f'INVALID message | missing plain_text attribute | message id = {self.message_id}'
                )
        if 'sent_time_stamp' in decrypted:
            self.sent_time_stamp = decrypted['sent_time_stamp']
        else:
            self.logger.warning(
                msg=f'INVALID message | missing sent_time_stamp attribute | message id = {self.message_id}'
                )
        if 'received_time_stamp' in decrypted:
            self.received_time_stamp = decrypted['received_time_stamp']
        else:
            self.logger.warning(
                msg=f'INVALID message | missing received_time_stamp attribute | message id = {self.message_id}'
                )
        if 'sender' in decrypted:
            self.sender = decrypted['sender']
        else:
            self.logger.warning(
                msg=f'INVALID message | missing sender attribute | message id = {self.message_id}'
                )

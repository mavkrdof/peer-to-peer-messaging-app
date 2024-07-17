"""
this module holds the message class
"""
import peertopeermessagingapp.RSA_cryptosystem as RSA
import json
import logging


class message:
    """
    vars:
        plain_text: str
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
    methods:
        read_in: none
            reads the message in from storage
        store: none
            stores the message
        encrypt: none
            encrypts relevant data for storage
        decrypt: list[int]
            decrypts message
    """

    def __init__(self, chat, message_id: str) -> None:
        """
        __init__ initializes the message data object

        Args:
            chat (peertopeermessagingapp.chat.Chat): the chat that the message is from
            message_id (str): the id of the message
        """
        self.plain_text = None
        self.chat = chat
        self.sender = None
        self.sent_time_stamp = None
        self.received_time_stamp = None
        self.message_id = message_id

    def read_in(self) -> None:
        """
        read_in reads in the message from storage
        """
        message_raw = self.chat.message_list[self.message_id]
        self.decrypt(message_data=message_raw)

    def store(self) -> None:
        """
        store stores the message in encrypted form
        """
        data = self.encrypt()
        if data is None:
            logging.warn(
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
            'plain_text': self.plain_text,
            'sender': self.sender,
            'sent_time_stamp': self.sent_time_stamp,
            'received_time_stamp': self.received_time_stamp
        }
        message_data_json = json.dumps(obj=message_data)
        try:
            encrypted = RSA.encrypt_chunked_padded(
                public_key_n=self.chat.public_key[0],
                public_key_e=self.chat.public_key[1],
                plain_text=message_data_json
                )
        except ValueError as error:
            logging.error(msg=error)
            return None
        return encrypted

    def decrypt(self, message_data: list[int]) -> None:
        """
        decrypt decrypts the message data and assigns the data

        Args:
            message_data (list[int]): the data to decrypt as a list of integers
        """
        decrypted_raw: str = RSA.decrypt_padded(
            encrypted=message_data,
            private_key_d=self.chat.private_key[1],
            private_key_n=self.chat.private_key[0]
            )
        print(decrypted_raw)
        decrypted: dict = json.loads(decrypted_raw)

        # check for valid message and assign data
        if 'plain_text' in decrypted:
            self.plain_text = decrypted['plain_text']
            # TODO: decide if plain_test should default to NONE or '' - must update tests
        else:
            logging.warning(
                msg=f'INVALID message | missing plain_text attribute | message id = {self.message_id}'
                )
        if 'sent_time_stamp' in decrypted:
            self.sent_time_stamp = decrypted['sent_time_stamp']
        else:
            logging.warning(
                msg=f'INVALID message | missing sent_time_stamp attribute | message id = {self.message_id}'
                )
        if 'received_time_stamp' in decrypted:
            self.received_time_stamp = decrypted['received_time_stamp']
        else:
            logging.warning(
                msg=f'INVALID message | missing received_time_stamp attribute | message id = {self.message_id}'
                )
        if 'sender' in decrypted:
            self.sender = decrypted['sender']
        else:
            logging.warning(
                msg=f'INVALID message | missing sender attribute | message id = {self.message_id}'
                )

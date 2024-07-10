"""
this module holds the message class
"""
import RSA_cryptosystem as RSA
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

    def __init__(self, user, message_id) -> None:
        self.plain_text = ''
        self.user = user
        self.sender = None
        self.sent_time_stamp = None
        self.received_time_stamp = None
        self.message_id = message_id

    def read_in(self) -> None:
        message_raw = self.user.message_list[self.message_id]
        self.decrypt(message_data=message_raw)

    def store(self) -> None:
        data = self.encrypt()
        if data is None:
            logging.warn(
                msg='Storing invalid Message data likely due to encryption error.'
                )
        self.user.message_list.append(data)

    def encrypt(self) -> list[int] | None:
        message_data = {
            'plain_text': self.plain_text,
            'sender': self.sender,
            'sent_time_stamp': self.sent_time_stamp,
            'received_time_stamp': self.received_time_stamp
        }
        message_data_json = json.dumps(obj=message_data)
        try:
            encrypted = RSA.encryptChunkedPadded(
                publicKN=self.user.public_key[0],
                publicKE=self.user.public_key[1],
                plainText=message_data_json
                )
        except ValueError as error:
            logging.error(msg=error)
            return None
        return encrypted

    def decrypt(self, message_data: list[int]) -> None:
        decrypted_raw = RSA.decryptPadded(
            encrypted=message_data,
            privateKD=self.user.private_key[1],
            privateKN=self.user.private_key[0]
            )
        decrypted: dict = json.loads(decrypted_raw)

        # check for valid message and assign data
        if 'plain_text' in decrypted:
            self.plain_text = decrypted['plain_text']
            if 'sent_time_stamp' in decrypted:
                self.sent_time_stamp = decrypted['sent_time_stamp']
                if 'received_time_stamp' in decrypted:
                    self.received_time_stamp = decrypted['received_time_stamp']
                    if 'sender' in decrypted:
                        self.sender = decrypted['sender']
                    else:
                        logging.warning(
                            msg=f'INVALID message | missing sender attribute | message id = {self.message_id}'
                            )
                else:
                    logging.warning(
                        msg=f'INVALID message | missing received_time_stamp attribute | message id = {self.message_id}'
                                    )
            else:
                logging.warning(
                    msg=f'INVALID message | missing sent_time_stamp attribute | message id = {self.message_id}'
                                )
        else:
            logging.warning(
                msg=f'INVALID message | missing plain_text attribute | message id = {self.message_id}'
                            )

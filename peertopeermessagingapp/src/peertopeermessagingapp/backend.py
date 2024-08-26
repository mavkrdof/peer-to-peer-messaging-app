import logging
import time
from peertopeermessagingapp.user_data import user_data
import os
import peertopeermessagingapp.RSA_gen_keys as RSA_gen_keys
from peertopeermessagingapp.message import message


# TODO add tests for funcs
class Backend_manager:
    def __init__(self, app) -> None:
        self.__password_separator = '-'
        self.app = app
        self.user_data = user_data(app=self.app)
        abs_path: str = os.path.split(os.path.abspath(__file__))[0]
        storage_path_extension = 'storage'
        user_data_path_extension = os.path.join(storage_path_extension, 'user_data.json')
        log_filepath_extension = os.path.join(storage_path_extension, 'runtime_logs.log')
        self.log_filepath = os.path.join(abs_path, log_filepath_extension)
        self.user_data_filepath = os.path.join(abs_path, user_data_path_extension)
        self.key_gen_complexity = 1.1
        self.logger = logging.getLogger(name=__name__)
        self.logger.info('Log file created')

    def send_message(self, message_text: str, chat: str) -> None:
        msg_id = f'{time.time_ns}'
        if chat in self.user_data.get_chat_dict():
            chat_obj = self.user_data.get_chat_dict()[chat]
            msg = message(chat=chat_obj, message_id=msg_id, content=message_text, app=self.app)
            self.user_data.send_message(message=msg, chat=chat)
        else:
            self.logger.warning(f'no chat named {chat}')

    def validate_login(self, username: str, password: str) -> int:
        self.logger.debug('extracting private keys from password...')
        extracted_private_keys = self.extract_private_keys(password=password)
        if extracted_private_keys is None:
            self.logger.info('Invalid login: Invalid password format')
            return 2  # Invalid Password format
        else:
            self.logger.debug('Valid password format')
            privateKN, privateKD = extracted_private_keys
            # checks if user data for the username and pword are in storage if so reads it in else returns false
            if self.user_data.read_from_file(username=username, privateKN=privateKN, privateKD=privateKD):
                self.logger.debug('Valid Login')
                return 1  # Valid login
            else:
                self.logger.debug('Invalid login: No account with that password and username')
                return 3  # No account with that password and username

    def extract_private_keys(self, password: str) -> tuple[int, int] | None:
        if self.__password_separator in password:
            privateKN, privateKD = password.split(self.__password_separator)
            if privateKD.isdigit() and privateKN.isdigit():
                privateKD = int(privateKD)
                privateKN = int(privateKN)
                return privateKN, privateKD
        # invalid pword
        self.logger.warning('Invalid password format')
        return None

    def create_new_account(self, password_seed, username) -> None | list[int]:
        try:
            self.logger.info('Generating private and public keys using RSA encryption')
            private_key, public_key = RSA_gen_keys.gen_keys(seed=password_seed, complexity=self.key_gen_complexity)
            self.logger.info('Successfully generated private and public keys using RSA encryption ')
            self.user_data.set_username(username=username)
            self.user_data.set_encryption_keys(private_key=private_key, public_key=public_key)
            self.logger.info('Successful created user account')
        except ValueError as error:
            self.logger.error(error)
            return None
        self.logger.info('Saving User Data...')
        self.save_user_data()
        self.logger.info('Successfully saved user data')
        return private_key

    def save_user_data(self) -> None:
        self.user_data.save_to_file()

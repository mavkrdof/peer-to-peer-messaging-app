import logging
from peertopeermessagingapp.user_data import user_data
import peertopeermessagingapp.RSA_cryptosystem as RSA
import os


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

    def validate_login(self, username: str, password: str) -> int:
        extracted_private_keys = self.extract_private_keys(password=password)
        if extracted_private_keys is None:
            return 2  # Invalid Password format
        else:
            privateKD, privateKN = extracted_private_keys
            # checks if user data for the username and pword are in storage if so reads it in else returns false
            if self.user_data.read_from_file(username=username, privateKD=privateKD, privateKN=privateKN):
                return 1  # Valid login
            else:
                return 3  # No account with that password and username

    def extract_private_keys(self, password: str) -> tuple[int, int] | None:
        if self.__password_separator in password:
            privateKD, privateKN = password.split(self.__password_separator)
            if privateKD.isdigit() and privateKN.isdigit():
                privateKD = int(privateKD)
                privateKN = int(privateKN)
                return privateKD, privateKN
        # invalid pword
        self.logger.warning('Invalid password format')
        return None

    def create_new_account(self, password_seed, username) -> None | list[int]:
        try:
            self.logger.info('Generating private and public keys using RSA encryption')
            private_key, public_key = RSA.gen_keys(seed=password_seed, complexity=self.key_gen_complexity)
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

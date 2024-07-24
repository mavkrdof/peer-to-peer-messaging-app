import logging
from peertopeermessagingapp.user_data import user_data


class Backend_manager:
    def __init__(self, app) -> None:
        self.__password_separator = '-'
        self.app = app
        self.user_data = user_data(app=self.app)
        self.user_data_filepath = ''

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
        logging.warning('Invalid password format')
        return None

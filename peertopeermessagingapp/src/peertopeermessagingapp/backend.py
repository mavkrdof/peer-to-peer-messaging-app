import logging
import time
from peertopeermessagingapp.user_data import user_data
import os
import peertopeermessagingapp.RSA_gen_keys as RSA_gen_keys
from peertopeermessagingapp.message import message


# TODO add tests for funcs
class Backend_manager:
    """
     the backend manager of the application
     vars:
        logged_in: bool
            whether or not the user is logged in
        user_data: user_data
            the user data manager
        log_filepath: str
            the path to the log file
        user_data_filepath: str
            the path to the user data file
        key_gen_complexity: float
            the complexity of the key generation
        __password_separator: str
            the separator for the password
        logger: logging
            the error and info logger for the backend
        app: PeertoPeerMessagingApp
            the application class
        storage_path_extension: str
            the storage path extension
        user_data_path_extension: str
            the user data path extension
        log_filepath_extension: str
            the log file path extension
    methods:
        send_message(message_text: str, chat: str)
            deals with the backend logic for sending a message
        update_logged_in_status(status: bool)
            deals with the backend logic for updating logged in status
        save_user_data()
            deals with the backend logic for saving user data
        logout()
            deals with the backend logic for logging out
        validate_login(username: str, password: str)
            deals with the backend logic for validating login
        create_account(username: str, password: str)
            deals with the backend logic for creating account
        extract_private_key(password: str)
            deals with the backend logic for extracting private key
        change_name_server_ip(ip: str)
            deals with the backend logic for changing the name server ip
        save_user_data()
            deals with the backend logic for saving user data
        update_logged_in_status(status: bool)
            deals with the backend logic for updating logged in status
        logout()
            deals with the backend logic for logging out
        init_network()
            deals with the backend logic for initializing network
        message_received(content, sender)
            deals with the backend logic for recieving a message
    """
    def __init__(self, app) -> None:
        """
        __init__ initilizes the backend manager

        Args:
            app (app): the app class
        vars:
            logged_in: bool
                whether or not the user is logged in
            user_data: user_data
                the user data manager
            log_filepath: str
                the path to the log file
            user_data_filepath: str
                the path to the user data file
            key_gen_complexity: float
                the complexity of the key generation
            __password_separator: str
                the separator for the password
            logger: logging
                the error and info logger for the backend
            app: PeertoPeerMessagingApp
                the application class
            storage_path_extension: str
                the storage path extension
            user_data_path_extension: str
                the user data path extension
            log_filepath_extension: str
                the log file path extension
        """
        self.logged_in = False
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
        """
        send_message deals with the backend logic for sending a message

        Args:
            message_text (str): the text to be sent
            chat (str): the chat the message is being sent on
        """
        msg_id = f'{time.time_ns}'
        if chat in self.user_data.get_chat_dict():
            chat_obj = self.user_data.get_chat_dict()[chat]
            msg = message(chat=chat_obj, message_id=msg_id, content=message_text, app=self.app)
            self.user_data.send_message(message=msg, chat=chat)
        else:
            self.logger.warning(f'no chat named {chat}')

    def receive_message(self, content: dict, sender: str) -> None:
        """
        receive_message deals with the backend logic for recieving a message

        Args:
            content (dict): the content of the message
            sender (str): the sender of the message
        """
        self.logger.debug('Received message')
        if content.__contains__('chat'):
            if self.user_data.get_chat_dict().__contains__(content['chat']):
                chat = self.user_data.get_chat_dict()[content['chat']]
                if content.__contains__('sent_time'):
                    sent_time = content['sent_time']
                    chat.message_received(content=content, sender=sender, sent_time=sent_time)
                else:
                    self.logger.debug('Received message with no sent time')
            else:
                self.logger.warning(f'no chat named {content["chat"]}')
        else:
            self.logger.warning('Received message with no chat')

    def validate_login(self, username: str, password: str) -> int:
        """
        validate_login validates the login

        Args:
            username (str): the username entered
            password (str): the password entered

        Returns:
            int: an integer representing the status of the login 1: Valid login 2: Invalid password format 3: Invalid login
        """
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
                self.update_logged_in_status(status=True)
                return 1  # Valid login
            else:
                self.logger.debug('Invalid login: No account with that password and username')
                return 3  # No account with that password and username

    def extract_private_keys(self, password: str) -> tuple[int, int] | None:
        """
        extract_private_keys extracts the private keys from the password

        Args:
            password (str): the password entered

        Returns:
            tuple[int, int] | None: returns a tuple of private keys if valid else None
        """
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
        """
        create_new_account deals with the backend logic for creating a new account

        Args:
            password_seed (int): the seed for generation of RSA public and private keys 
            username (str): the username of the new account

        Returns:
            None | list[int]: the private key if successful else None
        """
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
        self.update_logged_in_status(True)
        self.logger.info('Successfully saved user data')
        return private_key

    def save_user_data(self) -> None:
        """
        save_user_data deals with the backend logic for saving user data
        """
        self.user_data.save_to_file()

    def update_logged_in_status(self, status: bool) -> None:
        """
        update_logged_in_status updates the logged in status and deals with the backend logic for updating logged in status

        Args:
            status (bool): the new logged in status
        """
        if status:
            self.logged_in = True
            self.init_network()
        else:
            self.logged_in = False
            self.user_data = user_data(app=self.app)  # clears user data

    def logout(self) -> None:
        """
        logout the backend logic for logging out
        """
        self.update_logged_in_status(status=False)

    def init_network(self) -> None:
        """
        init_network the backend logic for initializing the network
        """
        self.app.network_manager.start()

    def change_name_server_ip(self, ip) -> None:
        """
        change_name_server_ip the backend logic for changing the name server ip

        Args:
            ip (str): the new name server ip
        """
        self.app.network_manager.add_address(name='name_server', ip=ip, port=8888)  # TODO set port from constant

import json
import logging
import os
import peertopeermessagingapp.RSA_encrypt as RSA_encrypt
import peertopeermessagingapp.RSA_decrypt as RSA_decrypt
import peertopeermessagingapp.chat as chat
from peertopeermessagingapp.message import message
from dataclasses import dataclass


@dataclass
class user_data:
    """
    attrs:
        __username: str
            the username of the user
        __chats: dict
            the chats of the user
        __settings: dict
            the settings of the user
        __app: peertopeermessagingapp.app.PeertoPeerMessagingApp
            the toga application
        __user_data: dict
            the user data of the user
        __private_key: list[int]
            the private key of the user
        __public_key: list[int]
            the public key of the user
        logger: logging.Logger
            the info and error logger
        address_book: dict
            the address book of the user
    methods:
        get_address(name)
            returns an address from the address book if it exists
        get_chat_dict()
            returns the chats of the user
        set_user_data(user_data)
            sets the user data
        get_private_key(key)
            returns the private key of the user
            key can be 'n' or 'd'
        get_public_key(key)
            returns the public key of the user
            key can be 'n' or 'e'
        save_user_data()
            saves the user data to the user data file
        set_username(username)
            sets the username of the user
        get_user_data()
            returns the user data
        set_encryption_keys(private_key, public_key)
            sets the encryption keys of the user
        send_message(message, chat)
            sends a message to a chat
        read_from_file()
            reads the user data from the user data file
        no_account_data()
            runs if there is no user data file found
        decrypt_user_data(data, username, privateKN, privateKD)
            validates the password
            returns True if the password is valid
            returns False if the password is invalid
            decrypts the user data if password is valid
        encrypt_user_data(data, username, publicKN, publicKE)
            encrypts the user data
        collect_data_to_save()
            collects the data to save into a dictionary
        save_to_file()
            saves the encrypted user data to the user data file
        save_data_to(file, data)
            writes the new json to the now empty user_data file
        load_user_data_from(file)
            loads the user data from the user data file
        add_chat(chat)
            adds a chat to the user data
        remove_chat(chat)
            removes a chat from the user data
        get_known_users()
            returns a list of the known users
    """
    def __init__(self, app) -> None:  # TODO: make private variable accessible eg add funcs to access them
        """
        __init__ initialises the user data
        Args:
            app (peertopeermessagingapp.app.PeertoPeerMessagingApp): the toga application
            username (str): the username of the user
        attrs:
            __username: str
                the username of the user
            __chats: dict
                the chats of the user
            __settings: dict
                the settings of the user
            __app: peertopeermessagingapp.app.PeertoPeerMessagingApp
                the toga application
            __user_data: dict
                the user data of the user
            __private_key: list[int]
                the private key of the user
            __public_key: list[int]
                the public key of the user
            logger: logging.Logger
                the info and error logger
            address_book: dict
                the address book of the user
        """
        self.__username = None
        self.__chats = {}
        self.__settings = {}
        self.__app = app
        self.__user_data = {}  # TODO Remove
        self.__private_key: list[int] = []
        self.__public_key: list[int] = []
        self.logger = logging.getLogger(name=__name__)
        self.address_book = {}

    def get_known_users(self) -> list[str]:
        """
        get_known_users returns a list of the known users

        Returns:
            list[str]: a list of the known users
        """
        if self.address_book is None:
            self.logger.error('Address book is None')
            return []
        else:
            return list(self.address_book.keys())

    def get_address(self, name) -> dict | None:
        """
        get_address gets an address from the address book if it exists

        Args:
            name (str): the name of the address to get

        Returns:
            dict | None: the address if it exists or None if it does not exist
        """
        if self.address_book.__contains__(name):
            return self.address_book[name]
        else:
            self.logger.error(f'Address book does not contain {name}')

    def get_chat_dict(self) -> dict:
        """
        get_chat_dict returns the chats of the user

        Returns:
            dict: the chats of the user
        """
        return self.__chats

    def set_user_data(self, user_data) -> None:
        """
        set_user_data sets the user data of the user

        Args:
            user_data (dict): the new user data
        """
        self.__user_data = user_data

    def get_private_key(self, key) -> int:
        """
        get_private_key returns either private key n or d depending on the key

        Args:
            key (str): the private key to return, valid keys are 'n' or 'd'

        Raises:
            ValueError: private key is undefined
                raises ValueError if the private key is undefined
            ValueError: invalid key
                raises ValueError if the key is invalid
        Returns:
            int: the private key n or d
        """
        if self.__private_key is []:
            raise ValueError('Private key is undefined')
        else:
            match key:
                case 'n':
                    return self.__private_key[0]
                case 'd':
                    return self.__private_key[1]
                case _:
                    raise ValueError(f'Invalid key expected n or d instead got {key}')

    def get_public_key(self, key) -> int:
        """
        get_public_key returns either public key n or e depending on the key

        Args:
            key (str): the public key to return, valid keys are 'n' or 'e'

        Raises:
            ValueError: public key is undefined
                raises ValueError if the public key is undefined
            ValueError: invalid key
                raises ValueError if the key is invalid

        Returns:
            int: the public key n or e
        """
        if self.__public_key is []:
            raise ValueError('Public key is undefined')
        else:
            match key:
                case 'n':
                    return self.__public_key[0]
                case 'e':
                    return self.__public_key[1]
                case _:
                    raise ValueError(f'Invalid key expected n or e instead got {key}')

    def set_username(self, username) -> None:
        if isinstance(username, str):
            self.__username = username
        else:
            raise ValueError(f'Expected username type str instead got {type(username)}')

    def set_encryption_keys(self, private_key: list[int], public_key: list[int]) -> None:  # TODO make by expanding the private and public keys from lists to ints
        """
        set_encryption_keys sets the encryption keys of the user

        Args:
            private_key (list[int]): the private key of the user
            public_key (list[int]): the public key of the user

        Raises:
            ValueError: private_key is not an int
                raises ValueError if the private key is not an int
            ValueError: public_key is not an int
                raises ValueError if the public key is not an int
        """
        if all(isinstance(item, int) for item in private_key):
            if all(isinstance(item, int) for item in public_key):
                self.__private_key = private_key  # N, D
                self.__public_key = public_key  # N, E
                self.__user_data['public_key_n'] = public_key[0]
                self.__user_data['public_key_e'] = public_key[1]
            else:
                raise ValueError(
                    f'{__name__}:set_encryption_keys: Expected public_key type int instead got type {type(public_key)}'
                    )
        else:
            raise ValueError(
                f'{__name__}:set_encryption_keys: Expected private_key type int instead got type {type(private_key)}'
                )

    def send_message(self, message: message, chat: str):
        """
        send_message sends a message to a chat

        Args:
            message (message): the message to send
            chat (str): the name of the chat to send the message to
        """
        if self.__chats.__contains__(chat):
            self.__chats[chat].send_message(message=message)
        else:
            logging.warning(f'no chat named {chat} found.')

    def read_from_file(self, username, privateKN, privateKD) -> bool:
        """
        read_from_file reads the user data from the file
        """
        if os.path.exists(self.__app.backend.user_data_filepath):
            self.logger.debug('reading in user data file...')
            with open(file=self.__app.backend.user_data_filepath, mode='r') as user_data_file:
                user_data_dict = json.load(fp=user_data_file)
            self.logger.debug('successfully read in user data file')
            self.logger.debug('checking if user data file contains username...')
            if username in user_data_dict:
                self.logger.debug('user data dict contains username')
                self.logger.debug('validating password...')
                is_decryption_valid = self.decrypt_user_data(
                    data=user_data_dict[username],
                    username=username,
                    privateKN=privateKN,
                    privateKD=privateKD
                    )
                if is_decryption_valid:
                    logging.info('User data successfully decrypted!')
                    return True
                else:
                    self.logger.warning('no matching user data in file')
                    self.no_account_data()
                    return False
            else:
                self.logger.warning('no matching user data in file')
                self.no_account_data()
                return False
        else:
            self.logger.warning('no user data file detected')
            self.no_account_data()
            return False

    def no_account_data(self) -> None:
        """
        no_account_data runs if there is no user data file
        """
        # uses the default user data as no account info found
        self.logger.info('If this is NOT a NEW ACCOUNT make sure you have transferred data correctly!')

    # TODO refactor into different funcs
    def decrypt_user_data(self, data: dict, username: str, privateKD: int, privateKN: int) -> bool:
        """
        decrypt_user_data decrypts the user data

        Args:
            data (dict): the encrypted user data in the form of a list of integers

        Returns:
            Boolean: whether or not the decryption was successful
        """
        # check if login is valid
        self.logger.debug('decrypting decrypt checker...')
        decrypt_checker = RSA_decrypt.decrypt_data(
            encrypted=data['decrypt_checker'],
            private_key_n=privateKN,
            private_key_d=privateKD
            )
        self.logger.debug('successfully decrypted decrypt checker')
        self.logger.debug(f'validating decrypt checker \'{decrypt_checker}\'...')
        if decrypt_checker == username:
            self.logger.debug('decrypt checker valid')
            # decrypt user data
            self.logger.debug('decrypting user data...')
            user_data_decrypted = RSA_decrypt.decrypt_data(
                encrypted=data['data'],
                private_key_d=privateKD,
                private_key_n=privateKN
                )

            # format as dictionary and store in memory
            self.logger.debug('Successfully decrypted user data')
            self.logger.debug('formatting json data as dictionary...')
            self.__user_data = json.loads(user_data_decrypted)
            self.logger.debug('successfully formatted json')
            self.logger.debug('setting vars...')
            self.__username = username
            self.set_encryption_keys(
                private_key=[
                    privateKN,
                    privateKD
                    ],
                public_key=[
                    self.__user_data['public_key_n'],
                    self.__user_data['public_key_e'],
                    ]
                )
            if self.__user_data.__contains__('address_book'):
                self.address_book = self.__user_data['address_book']
            self.logger.debug('successfully set vars')
            return True
        else:
            self.logger.warning('Decrypt checker invalid')
            return False

    def encrypt_user_data(self) -> dict:
        """
        encrypt_user_data encrypts and formats the user data as json,
         and stores it in a dict under the key of the username

        Returns:
            dict: the encrypted user data in the form of a dict
        """
        encrypted_data = {
            'username': self.__username,
            'decrypt_checker': RSA_encrypt.encrypt_data(
                plain_text=self.__username,  # TODO make dict to make clearer
                public_key_n=self.get_public_key(key='n'),
                public_key_e=self.get_public_key(key='e'),
                )
        }

        data_to_save = self.collect_data_to_save()

        encrypted_data['data'] = RSA_encrypt.encrypt_data(
            plain_text=json.dumps(
                obj=data_to_save,  # TODO figure out how to store data
                ),
            public_key_n=self.get_public_key(key='n'),
            public_key_e=self.get_public_key(key='e'),
            )
        return encrypted_data

    def collect_data_to_save(self) -> dict:
        """
        collect_data_to_save collects data to save to file

        Returns:
            dict: a dictionary of data to save
        """
        chat_dict = {}
        for chat_object_name, chat_object in self.get_chat_dict().items():
            chat_dict[chat_object_name] = chat_object.convert_to_dict()
        data_to_save = {
            'private_key_n': self.get_private_key(key='n'),
            'private_key_d': self.get_private_key(key='d'),
            'public_key_n': self.get_public_key(key='n'),
            'public_key_e': self.get_public_key(key='e'),
            'theme': self.__app.GUI.theme,
            'chats': chat_dict,
            'address_book': self.address_book
        }
        return data_to_save

    def save_to_file(self) -> None:
        """
        save_to_file saves encrypted user data to file
        """
        self.logger.debug('saving user data to file...')
        user_data_dict = self.load_user_data_from(self.__app.backend.user_data_filepath)

        self.logger.debug('encrypting user data...')
        user_data_dict[self.__username] = self.encrypt_user_data()  # replaces old user data with current user data to stored user data
        self.logger.debug('successfully encrypted user data')
        self.logger.debug('formatting user data as json...')
        user_data_json: str = json.dumps(
            obj=user_data_dict,
            sort_keys=True,
            indent=4
            )  # converts dictionary to json
        self.logger.debug('successfully formatted user data as json')
        self.logger.debug('writing user data to file...')

        self.save_data_to(self.__app.backend.user_data_filepath, user_data_json)

    def save_data_to(self, file_path: str, user_data: str):
        """
        save_data_to saves user data to file

        Args:
            file_path (str): the file path to save to
            user_data (str): the user data to save
        """
        if os.path.exists(file_path):  # checks if file exists
            mode = 'w'  # overwrites existing file
            self.logger.debug('user data file found... writing to it')
        else:
            mode = 'x'  # creates new file
            self.logger.debug('No user data file... creating one')
        with open(file=file_path, mode=mode) as user_data_file:
            user_data_file.write(user_data)  # writes the new json to the now empty user_data file
        self.logger.debug('Successfully wrote user data to file')

    def load_user_data_from(self, file_path: str) -> dict:
        """
        load_user_data_from loads user data from file

        Args:
            file_path (str): the file path to load from

        Returns:
            dict: the loaded user data
        """
        if os.path.exists(file_path):  # checks if file exists
            self.logger.debug('found existing user data file reading in...')
            # reads in the user_data file
            with open(file=file_path, mode='r') as user_data_file:
                user_data_raw: str = ''.join(user_data_file.readlines())
                if user_data_raw == '':
                    user_data_dict = {}
                else:
                    user_data_dict = json.loads(user_data_raw)
            self.logger.debug('successfully read in user data file')
        else:
            self.logger.debug('no preexisting user data file found')
            user_data_dict = {}
        return user_data_dict

    def add_chat(self, name, icon) -> None:
        """
        add_chat adds a new chat to the user

        Args:
            name (str): the name of the chat
            icon (str): the icon of the chat
        """
        if self.__chats.__contains__(name):
            self.logger.warning(f'chat {name} already exists')
        else:
            new_chat = chat.Chat(app=self.__app)
            new_chat.create_chat(name=name, icon=icon)  # TODO move create_chat into init
            self.__chats[name] = (new_chat)

    def remove_chat(self, chat) -> None:
        """
        remove_chat removes a chat from the user

        Args:
            chat (_type_): _description_
        """
        if self.__chats.__contains__(chat):
            self.__chats.pop(chat)
        else:
            self.logger.warning(f'No chat called {chat} found')

    def update_settings(self, settings: dict) -> None:
        """
        update_settings updates the user settings

        Args:
            settings (dict): the new settings
        """
        self.__settings = {}
        for key, value in settings.items():
            self.__settings[key] = value

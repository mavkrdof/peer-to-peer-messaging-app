import json
import logging
import os
import peertopeermessagingapp.RSA_encrypt as RSA_encrypt
import peertopeermessagingapp.RSA_decrypt as RSA_decrypt
import peertopeermessagingapp.chat as chat
from peertopeermessagingapp.message import message


class user_data:
    """
    vars
        private_key: [int, int]
            the private key [N, D]
        public_key: [int, int]
            the public key [N, E]
    """
    def __init__(self, app) -> None:  # TODO: make private variable accessible eg add funcs to access them
        """
        __init__ initialises the user data
        Args:
            app (peertopeermessagingapp.app.PeertoPeerMessagingApp): the toga application
            username (str): the username of the user
        """
        self.__username = None
        self.__chats = {}
        self.__settings = {}
        self.__app = app
        self.__user_data = {}
        self.__private_key: list[int] = []
        self.__public_key: list[int] = []  # TODO
        self.logger = logging.getLogger(name=__name__)

    def get_chat_list(self) -> dict:
        return self.__chats

    def set_user_data(self, user_data) -> None:  # TODO make less bad
        self.__user_data = user_data

    def get_private_key(self, key) -> int:
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

    def set_encryption_keys(self, private_key, public_key) -> None:
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
        if self.__chats.__contains__(chat):
            self.__chats[chat].send_message()
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
                if self.decrypt_user_data(data=user_data_dict[username], username=username, privateKN=privateKN, privateKD=privateKD):
                    logging.info('User data successfully decrypted!')
                    self.__username = username
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

    def decrypt_user_data(self, data: dict, username: str, privateKD: int, privateKN: int) -> bool:  # TODO refactor into differnt funcs
        """
        decrypt_user_data decrypts the user data

        Args:
            data (dict): the encrypted user data in the form of a list of integers

        Returns:
            Boolean: whether or not the decryption was successful
        """
        # check if login is valid
        self.logger.debug('decrypting decrypt checker...')
        decrypt_checker = RSA_decrypt.decrypt_padded(
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
            user_data_decrypted = RSA_decrypt.decrypt_padded(
                encrypted=data['data'],
                private_key_d=privateKD,
                private_key_n=privateKN
                )
            # format as dictionary and store in memory
            self.logger.debug('Successfully decrypted user data')
            self.logger.debug('formatting json data as dictionary...')
            user_data_decrypted = user_data_decrypted[:-1] + '}'  # TODO This is a quick patch to fix a decryption error should find a better solution
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
                    self.__user_data['public_key_e'],
                    self.__user_data['public_key_n']
                    ]
                )
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
            'decrypt_checker': RSA_encrypt.encrypt_chunked_padded(
                plain_text=self.__username,  # TODO make dict to make clearer
                public_key_n=self.__public_key[0],
                public_key_e=self.__public_key[1],
                )
        }

        data_to_save = self.collect_data_to_save()

        encrypted_data['data'] = RSA_encrypt.encrypt_chunked_padded(
            plain_text=json.dumps(
                obj=data_to_save,  # TODO figure out how to store data
                ),
            public_key_n=self.__public_key[0],
            public_key_e=self.__public_key[1],
            )
        return encrypted_data

    def collect_data_to_save(self) -> dict:
        chat_dict = {}
        for chat_object_name, chat_object in self.get_chat_list().items():
            chat_dict[chat_object_name] = chat_object.convert_to_dict()
        data_to_save = {
            'private_key_n': self.get_private_key(key='n'),
            'private_key_d': self.get_private_key(key='d'),
            'public_key_n': self.get_public_key(key='n'),
            'public_key_e': self.get_public_key(key='e'),
            'theme': self.__app.GUI.theme,
            'chats': chat_dict
        }
        return data_to_save

    def save_to_file(self) -> None:
        """
        save_to_file saves encrypted user data to file
        """
        self.logger.debug('saving user data to file...')
        if os.path.exists(self.__app.backend.user_data_filepath):  # checks if file exists
            self.logger.debug('found existing user data file reading in...')
            with open(file=self.__app.backend.user_data_filepath, mode='r') as user_data_file:  # reads in the user_data file
                user_data_raw: str = ''.join(user_data_file.readlines())
                if user_data_raw == '':
                    user_data_dict = {}
                else:
                    user_data_dict = json.loads(user_data_raw)
            self.logger.debug('successfully read in user data file')
        else:
            self.logger.debug('no preexisting user data file found')
            user_data_dict = {}
        self.logger.debug('encrypting user data...')
        user_data_dict[self.__username] = self.encrypt_user_data()  # appends current user data to stored user data
        self.logger.debug('successfully encrypted user data')
        self.logger.debug('formatting user data as json...')
        user_data_json = json.dumps(
            obj=user_data_dict,
            sort_keys=True, indent=4
            )  # converts dictionary to json
        self.logger.debug('successfully formatted user data as json')
        self.logger.debug('writing user data to file...')
        if os.path.exists(self.__app.backend.user_data_filepath):
            mode = 'w'
            self.logger.debug('user data file found... writing to it')
        else:
            mode = 'x'
            self.logger.debug('No user data file... creating one')
        with open(file=self.__app.backend.user_data_filepath, mode=mode) as user_data_file:
            user_data_file.write(user_data_json)  # writes the new json to the now empty user_data file
        self.logger.debug('Successfully wrote user data to file')

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
            new_chat = chat.Chat()
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

    def get_chats(self) -> None:
        """
        get_chats returns a list of the users chats
        """
        pass

    def update_settings(self, settings: dict) -> None:
        """
        update_settings updates the user settings

        Args:
            settings (dict): the new settings
        """
        self.__settings = {}
        for key, value in settings.items():
            self.__settings[key] = value

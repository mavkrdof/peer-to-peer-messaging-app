import json
import logging
import peertopeermessagingapp.RSA_cryptosystem as RSA
import peertopeermessagingapp.chat as chat


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
        self.__chats = []
        self.__settings = {}
        self.__app = app
        self.__user_data = {}
        self.__private_key = None
        self.__public_key = None
        self.logger = logging.getLogger(name=__name__)

    def get_private_key(self) -> int:
        if self.__private_key is None:
            raise ValueError('Private key is undefined')
        else:
            return self.__private_key

    def get_public_key(self) -> int:
        if self.__public_key is None:
            raise ValueError('Public key is undefined')
        else:
            return self.__public_key

    def set_username(self, username) -> None:
        if isinstance(username, str):
            self.__username = username
        else:
            raise ValueError(f'Expected username type str instead got {type(username)}')

    def set_encryption_keys(self, private_key, public_key) -> None:
        if all(isinstance(item, int) for item in private_key):
            if all(isinstance(item, int) for item in public_key):
                self.__private_key = private_key
                self.__public_key = public_key
            else:
                raise ValueError(
                    f'{__name__}:set_encryption_keys: Expected public_key type int instead got type {type(public_key)}'
                    )
        else:
            raise ValueError(
                f'{__name__}:set_encryption_keys: Expected private_key type int instead got type {type(private_key)}'
                )

    def read_from_file(self, username, privateKD, privateKN) -> bool:
        """
        read_from_file reads the user data from the file
        """
        with open(file=self.__app.backend.user_data_filepath, mode='r') as user_data_file:
            user_data_dict = json.load(fp=user_data_file)
        if username in user_data_dict:
            if self.decrypt_user_data(data=user_data_dict[username], username=username, privateKD=privateKD, privateKN=privateKN):
                logging.info('User data successfully decrypted!')
                self.__username = username
                return True
            else:
                self.no_account_data()
                return False
        else:
            self.no_account_data()
            return False

    def no_account_data(self) -> None:
        """
        no_account_data runs if there is no user data file
        """
        # uses the default user data as no account info found
        logging.warning('WARNING: no user data file detected')  # DEBUG
        logging.info('If this is NOT a NEW ACCOUNT make sure you have transferred data correctly!')

    def decrypt_user_data(self, data, username, privateKN, privateKD) -> bool:
        """
        decrypt_user_data decrypts the user data

        Args:
            data (list[int]): the encrypted user data in the form of a list of integers

        Returns:
            Boolean: whether or not the decryption was successful
        """
        decrypt_checker = RSA.decrypt_padded(
            encrypted=data['decrypt_checker'],
            private_key_n=privateKN,
            private_key_d=privateKD
            )
        if decrypt_checker == username:
            user_data_decrypted = RSA.decrypt_padded(
                encrypted=data['user_data'],
                private_key_d=privateKD,
                private_key_n=privateKN
                )
            self.__user_data = json.loads(user_data_decrypted)
            self.__username = username
            self.private_key = [privateKD, privateKN]
            return True
        else:
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
            'decrypt_checker': '',
            'data': ''
        }
        encrypted_data['data'] = RSA.encrypt_chunked_padded(
            plain_text=json.dumps(
                obj=self.__user_data,
                sort_keys=True,
                indent=4
                ),
            public_key_e=self.__user_data['publicKE'],
            public_key_n=self.__user_data['publicKN']
            )
        return encrypted_data

    def save_to_file(self) -> None:
        """
        save_to_file saves encrypted user data to file
        """
        with open(file=self.__app.user_data_filepath, mode='r') as user_data_file:
            user_data_dict = json.load(fp=user_data_file)
        user_data_dict[self.__username] = self.encrypt_user_data()
        user_data_json = json.dumps(
            obj=user_data_dict,
            sort_keys=True, indent=4
            )
        with open(file=self.__app.user_data_filepath, mode='w') as user_data_file:
            user_data_file.write(user_data_json)

    def add_chat(self, name, icon) -> None:
        """
        add_chat adds a new chat to the user

        Args:
            name (str): the name of the chat
            icon (str): the icon of the chat
        """
        new_chat = chat.Chat()
        new_chat.create_chat(name=name, icon=icon)
        self.__chats.append(chat)

    def remove_chat(self, chat) -> None:
        """
        remove_chat removes a chat from the user

        Args:
            chat (_type_): _description_
        """
        self.__chats.remove(chat)

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

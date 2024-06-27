import json
import peertopeermessagingapp.RSA_cryptosystem as RSA

class user_data:
    """
    """
    def __init__(self, app, username) -> None:  # TODO: make private variable accessible eg add funcs to access them
        self.__username = username
        self.__chats = []
        self.__settings = {}
        self.__app = app
        self.__user_data = {}

    def read_from_file(self) -> None:
        with open(file=self.__app.user_data_filepath, mode='r') as user_data_file:
            user_data_dict = json.load(fp=user_data_file)
        if self.__username in user_data_dict:
            self.decrypt_user_data(data=user_data_dict[self.__username])
        else:
            # runs with the default user data as is new account
            print('WARNING: no user data file detected')  # DEBUG
            print('If this is not a NEW ACCOUNT make sure you have transferred data correctly!')

    def decrypt_user_data(self, data) -> None:
        decrypt_checker = RSA.decryptPadded(
            encrypted=data['decrypt_checker'],
            privateKN=self.__user_data['privateKN'],
            privateKD=self.__user_data['privateKD']
            )
        if decrypt_checker == data['username']:
            user_data_decrypted = RSA.decryptPadded(
                encrypted=data['user_data'],
                privateKD=self.__user_data['privateKD'],
                privateKN=self.__user_data['privateKN']
                )
            self.__user_data = json.loads(user_data_decrypted)
        else:
            return None

    def encrypt_user_data(self) -> dict:
        encrypted_data = {
            'username': self.__username,
            'decrypt_checker': '',
            'data': ''
        }
        encrypted_data['data'] = RSA.encryptChunkedPadded(
            plainText=json.dumps(
                obj=self.__user_data,
                sort_keys=True,
                indent=4
                ),
            publicKE=self.__user_data['publicKE'],
            publicKN=self.__user_data['publicKN']
            )
        return encrypted_data

    def save_to_file(self) -> None:
        with open(file=self.__app.user_data_filepath, mode='r') as user_data_file:
            user_data_dict = json.load(fp=user_data_file)
        user_data_dict[self.__username] = self.encrypt_user_data()
        user_data_json = json.dumps(
            obj=user_data_dict,
            sort_keys=True, indent=4
            )
        with open(file=self.__app.user_data_filepath, mode='w') as user_data_file:
            user_data_file.write(user_data_json)

    def add_chat(self, chat) -> None:
        self.__chats.append(chat)

    def remove_chat(self, chat) -> None:
        self.__chats.remove(chat)

    def get_chats(self) -> None:
        pass

    def update_settings(self, settings: dict) -> None:
        for key, value in settings.items():
            self.__settings[key] = value

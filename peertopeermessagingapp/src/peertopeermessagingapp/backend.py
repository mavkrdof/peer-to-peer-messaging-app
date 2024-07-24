from peertopeermessagingapp.user_data import user_data

class Backend_manager:
    def __init__(self, app) -> None:
        self.app = app
        self.user_data = user_data(app=self.app)

    def validate_login(self, username, password) -> bool:
        privateKD, privateKN = self.extract_private_keys(password=password)
        return self.user_data.read_from_file(username=username, privateKD=privateKD, privateKN=privateKN)

    def extract_private_keys(self, password) -> tuple[int, int]:
        privateKD, privateKN = 1, 1
        return privateKD, privateKN

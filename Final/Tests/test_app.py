import pytest
from src.peertopeermessagingapp.user_data import user_data
from src.peertopeermessagingapp.RSA_encrypt import encrypt_data
from src.peertopeermessagingapp.RSA_decrypt import decrypt_data
from src.peertopeermessagingapp.RSA_gen_keys import gen_keys
from src.peertopeermessagingapp.message import message
import json
import src.peertopeermessagingapp.network_manager as network_manager


class Test_Encrypt_data:

    # encrypts plain text correctly with valid public keys and plain text
    def test_encrypts_and_decrypts_plain_text_correctly(self) -> None:
        private, public = gen_keys(
            seed=10,
            complexity=2
        )
        plainText = "hello"
        result = encrypt_data(
            public_key_n=public[0],
            public_key_e=public[1],
            plain_text=plainText
            )
        decrypted = decrypt_data(
            encrypted=result,
            private_key_d=private[1],
            private_key_n=private[0]
        )
        assert decrypted == plainText

    # raises ValueError if publicKN is not an integer
    def test_raises_value_error_if_publicKN_not_int(self) -> None:
        publicKN = "not_an_int"
        publicKE = 17
        plainText = "hello"
        with pytest.raises(ValueError, match="expected publicKN type int instead got type <class 'str'>"):
            encrypt_data(
                public_key_n=publicKN,
                public_key_e=publicKE,
                plain_text=plainText
                )

    # handles plain text with special characters
    def test_handles_plain_text_with_special_characters(self):
        private, public = gen_keys(
            seed=10,
            complexity=2
        )
        plainText = "hello$%$_#@_@!)"
        result = encrypt_data(
            public_key_n=public[0],
            public_key_e=public[1],
            plain_text=plainText
            )
        decrypted = decrypt_data(
            encrypted=result,
            private_key_d=private[1],
            private_key_n=private[0]
        )
        assert decrypted == plainText

    # processes plain text of varying lengths
    def test_encrypts_plain_text_length_varying_correctly(self) -> None:
        private, public = gen_keys(
            seed=10,
            complexity=2
        )
        test_text = ["hello",
                     'hello world',
                     'h',
                     'f8h328h2fhsho[ecdnano[h[hr[238ehd[oshfofhwodfhweo[fh'
                     ]
        for plain_text in test_text:
            result = encrypt_data(
                public_key_n=public[0],
                public_key_e=public[1],
                plain_text=plain_text
                )
            decrypted = decrypt_data(
                encrypted=result,
                private_key_d=private[1],
                private_key_n=private[0]
            )
            assert decrypted == plain_text


class Test_message_encrypt:

    # Encrypts valid message data correctly with the correct module import
    def test_encrypts_valid_message_data_correctly(self, mocker):
        mock_user = mocker.Mock()
        mock_user.public_key = (12345, 67890)
        msg = message(app=None, chat=mock_user, message_id="1", content="")
        msg.content = "Hello, World!"
        msg.sender = "user_123"
        msg.sent_time_stamp = 1622547800
        msg.received_time_stamp = 1622547900

        encrypted_data = msg.encrypt()
        valid_encrypted_data = [
            3264, 11851, 5449, 5844, 5989, 1110, 1585, 8695,
            10021, 121, 1275, 10021, 11851, 10354, 6994,
            11851, 10389, 121, 5844, 5844, 10356, 2086, 6994,
            849, 10356, 9786, 5844, 3700, 7344, 11851, 2086,
            6994, 11851, 10840, 121, 1585, 3700, 121, 9786,
            11851, 10354, 6994, 11851, 10284, 10840, 121,
            9786, 8695, 7471, 1555, 2511, 11851, 2086, 6994,
            11851, 10840, 121, 1585, 10021, 8695, 10021, 1110,
            646, 121, 8695, 10840, 10021, 5989, 646, 5449, 11851, 10354,
            6994, 7471, 11211, 1555, 1555, 6919, 9124, 8290, 5056, 2784,
            2784, 2086, 6994, 11851, 9786, 121, 7536, 121, 1110, 5119, 121, 3700,
            8695, 10021, 1110, 646, 121, 8695, 10840, 10021, 5989, 646, 5449,
            11851, 10354, 6994, 7471, 11211, 1555, 1555, 6919, 9124,
            8290, 129, 2784, 2784, 6490
            ]
        assert encrypted_data == valid_encrypted_data

    # handles empty plain_text without errors
    def test_handles_empty_plain_text_without_errors(self, mocker):
        mock_user = mocker.Mock()
        mock_user.public_key = (12345, 67890)  # TODO
        msg = message(app=None, chat=mock_user, message_id="2", content="")
        msg.content = ""
        msg.sender = "user_123"
        msg.sent_time_stamp = 1622547800
        msg.received_time_stamp = 1622547900

        encrypted_data = msg.encrypt()
        valid_encrypted_data = [
            3264, 11851, 5449, 5844, 5989, 1110, 1585, 8695,
            10021, 121, 1275, 10021, 11851, 10354, 6994, 11851,
            11851, 2086, 6994, 11851, 10840, 121, 1585, 3700,
            121, 9786, 11851, 10354, 6994, 11851, 10284, 10840,
            121, 9786, 8695, 7471, 1555, 2511, 11851, 2086, 6994,
            11851, 10840, 121, 1585, 10021, 8695, 10021, 1110,
            646, 121, 8695, 10840, 10021, 5989, 646, 5449, 11851,
            10354, 6994, 7471, 11211, 1555, 1555, 6919, 9124,
            8290, 5056, 2784, 2784, 2086, 6994, 11851, 9786,
            121, 7536, 121, 1110, 5119, 121, 3700, 8695, 10021,
            1110, 646, 121, 8695, 10840, 10021, 5989, 646, 5449,
            11851, 10354, 6994, 7471, 11211, 1555, 1555, 6919,
            9124, 8290, 129, 2784, 2784, 6490
            ]
        assert encrypted_data == valid_encrypted_data

    # ensures logging captures the correct error messages
    def test_logging_error_on_encryption_failure(self, mocker, caplog):
        import logging

        mock_user = mocker.Mock()
        mock_user.public_key = ('force error', 67890)
        # an encryption key as type string will cause an encryption failure
        msg = message(app=None, chat=mock_user, message_id="1", content='')
        msg.content = "Hello, World!"
        msg.sender = "user_123"
        msg.sent_time_stamp = 1622547800
        msg.received_time_stamp = 1622547900

        with caplog.at_level(logging.ERROR):
            encrypted_data = msg.encrypt()

            assert f"expected publicKN type int instead got type {type('force error')}" in caplog.text
            assert encrypted_data is None


class Test_message_decrypt:

    # correctly decrypts a valid encrypted message
    def test_correctly_decrypts_valid_encrypted_message(self, mocker):

        # Mock user and RSA decryption
        mock_user = mocker.Mock()
        mock_user.private_key = (12345, 67890)
        mock_user.message_list = {1: [111, 222, 333]}
        decrypted_data = json.dumps({
            'plain_text': 'Hello, World!',
            'sender': 'user123',
            'sent_time_stamp': 1622547800,
            'received_time_stamp': 1622547900
        })
        mocker.patch('src.peertopeermessagingapp.message.RSA_decrypt.decrypt_data', return_value=decrypted_data)

        # Initialize message object and call decrypt
        msg = message(app=None, chat=mock_user, message_id='1', content='')
        msg.decrypt(message_data=[111, 222, 333])  # Random data

        # Assertions
        assert msg.content == 'Hello, World!'
        assert msg.sender == 'user123'
        assert msg.sent_time_stamp == 1622547800
        assert msg.received_time_stamp == 1622547900

    # logs warning for missing plain_text attribute
    def test_logs_warning_for_missing_plain_text_attribute(self, mocker, caplog):
        import logging

        # Mock user and RSA decryption
        mock_user = mocker.Mock()
        mock_user.private_key = (12345, 67890)
        mock_user.message_list = {1: [111, 222, 333]}
        decrypted_data = json.dumps({
            'sender': 'user123',
            'sent_time_stamp': 1622547800,
            'received_time_stamp': 1622547900
        })
        mocker.patch('src.peertopeermessagingapp.message.RSA_decrypt.decrypt_data', return_value=decrypted_data)
        # Initialize message object and call decrypt
        msg = message(app=None, chat=mock_user, message_id='1', content='')
        msg.decrypt(message_data=[111, 222, 333])

        caplog.at_level(logging.WARNING)

        # Assertions
        assert msg.content == ''
        assert msg.sender == 'user123'
        assert msg.sent_time_stamp == 1622547800
        assert msg.received_time_stamp == 1622547900
        assert f'INVALID message | missing plain_text attribute | message id = {msg.message_id}' in caplog.text


class Test_user_data_store_load:

    def test_encrypt_user_data(self, mocker):
        app = mocker.Mock()
        app.GUI = mocker.Mock()
        app.GUI.theme = {'thing': 'test'}
        print('d')
        user = user_data(app)  # None is placeholder as unused
        user.set_username('test1')
        user.set_encryption_keys([323, 17], [323, 65537])
        user.set_user_data({'public_key_n': 323, 'public_key_e': 65537})
        encrypted_user_data = user.encrypt_user_data()
        valid_decrypt_checker = [
                    48, 16, 115, 48, 83
                ]
        assert encrypted_user_data['decrypt_checker'] == valid_decrypt_checker

    def test_load(self):
        user = user_data(None)  # None is placeholder as unused
        username = 'test1'
        data = {
            'decrypt_checker': [48, 16, 115, 48, 83],
            'data': [
                55, 204, 180, 114, 173, 271, 29, 48,
                16, 95, 141, 16, 87, 95, 280, 204,
                58, 117, 136, 84, 136, 282, 117,
                204, 180, 114, 173, 271, 29, 48, 16,
                95, 141, 16, 87, 95, 270, 204, 58,
                117, 83, 123, 282, 117, 204, 180, 32,
                13, 193, 173, 252, 95, 141, 16, 87, 95,
                280, 204, 58, 117, 136, 84, 136, 282,
                117, 204, 180, 32, 13, 193, 173, 252,
                95, 141, 16, 87, 95, 16, 204, 58, 117,
                139, 223, 223, 136, 123, 282, 117, 204,
                48, 36, 16, 262, 16, 204, 58, 117, 55,
                204, 48, 36, 173, 280, 69, 204, 58, 117,
                204, 48, 16, 115, 48, 204, 159, 282, 117,
                204, 252, 36, 29, 48, 115, 204, 58, 117,
                55, 159, 159
                ]
            }
        decrypted_user_data = user.decrypt_user_data(data=data, username=username, privateKN=323, privateKD=17)
        assert decrypted_user_data


class Test_network_messaging:
    def test_message_create(self, mocker) -> None:
        nm = network_manager.Network_manager(app=None)
        nm.own_address = {
            'name': 'self name'
        }
        target_name = 'test_address'
        nm.address_book[target_name] = {
            'name': target_name,
            'ip': '',
            'port': 0,
            'public_key_e': 0,
            'public_key_n': 0
        }
        content = {}
        message = nm.create_message(
            content=content,
            command='command',
            target=target_name
        )
        content_json = json.dumps(content)
        expected_message = json.dumps(
            {
                'command': 'command',
                'content': content_json.replace('\n', ''),
                'sender': 'self name'
            }
        )
        assert message == expected_message + '\n'

    def test_parse_message(self, mocker) -> None:
        nm = network_manager.Network_manager(None)
        expected_message = {
            'content': 'test content',
            'command': 'test content',
            'target_name': 'test name'
        }
        message_to_parse = json.dumps(expected_message)
        parsed_message = nm.parse_message(message_to_parse)
        assert parsed_message == expected_message

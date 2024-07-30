import pytest
# from src.peertopeermessagingapp.user_data import user_data as user_data
from src.peertopeermessagingapp.RSA_cryptosystem import encrypt_chunked_padded, decrypt_padded, gen_keys
from src.peertopeermessagingapp.message import message
import json
from peertopeermessagingapp.user_data import user_data


class Test_Encrypt_Chunked_Padded:

    # encrypts plain text correctly with valid public keys and plain text
    def test_encrypts_and_decrypts_plain_text_correctly(self) -> None:
        private, public = gen_keys(
            seed=10,
            complexity=2
        )
        plainText = "hello"
        result = encrypt_chunked_padded(
            public_key_n=public[0],
            public_key_e=public[1],
            plain_text=plainText
            )
        decrypted = decrypt_padded(
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
            encrypt_chunked_padded(
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
        result = encrypt_chunked_padded(
            public_key_n=public[0],
            public_key_e=public[1],
            plain_text=plainText
            )
        decrypted = decrypt_padded(
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
            result = encrypt_chunked_padded(
                public_key_n=public[0],
                public_key_e=public[1],
                plain_text=plain_text
                )
            decrypted = decrypt_padded(
                encrypted=result,
                private_key_d=private[1],
                private_key_n=private[0]
            )
            assert decrypted == plain_text

# the below are to annoying to test take too much processing time
# TODO optimise key generation

    # def test_gen_key_with_varying_complexity(self) -> None:
    #     for complexity in range(1, 4):
    #         seed = 10
    #         private, public = genKeys(
    #             seed=seed,
    #             complexity=complexity
    #             )
    #         plainText = "hello"
    #         result = encryptChunkedPadded(
    #             publicKN=public[0],
    #             publicKE=public[1],
    #             plainText=plainText
    #             )
    #         decrypted = decrypt_padded(
    #             encrypted=result,
    #             privateKD=private[1],
    #             privateKN=private[0]
    #         )
    #         assert decrypted == plainText

    # def test_gen_key_with_varying_seed(self) -> None:
    #     for seed in range(10, 22, 4):
    #         seed *= 10
    #         private, public = genKeys(
    #             seed=seed,
    #             complexity=2
    #             )
    #         plainText = "hello"
    #         result = encryptChunkedPadded(
    #             publicKN=public[0],
    #             publicKE=public[1],
    #             plainText=plainText
    #             )
    #         decrypted = decrypt_padded(
    #             encrypted=result,
    #             privateKD=private[1],
    #             privateKN=private[0]
    #         )
    #         assert decrypted == plainText


class Test_message_encrypt:

    # Encrypts valid message data correctly with the correct module import
    def test_encrypts_valid_message_data_correctly(self, mocker):
        mock_user = mocker.Mock()
        mock_user.public_key = (12345, 67890)
        msg = message(chat=mock_user, message_id="1")
        msg.plain_text = "Hello, World!"
        msg.sender = "user_123"
        msg.sent_time_stamp = 1622547800
        msg.received_time_stamp = 1622547900

        encrypted_data = msg.encrypt()
        valid_encrypted_data = [
            6211, 8659, 3094, 195, 6190, 3985, 2511, 4285,
            2440, 2770, 1080, 10609, 1120, 8680, 5044, 8371,
            4416, 11154, 6076, 6211, 1654, 7255, 11859, 9576,
            4285, 5061, 5086, 4716, 6745, 121, 1120, 8359, 5961,
            1741, 10540, 121, 9025, 4875, 2511, 1120, 11149, 5961,
            106, 10356, 10021, 2511, 4285, 4086, 1375, 7396, 9271,
            841, 2296, 5961, 2065, 6411, 4116, 7570, 10540, 8374,
            5545, 5271, 4069, 9115, 3199, 1, 1375, 1975, 5980, 9751,
            1585, 8695, 8781, 11700, 6076, 2511, 1171, 874, 2806,
            1794, 8359, 4285, 4875, 7080, 7570, 10750, 8430, 5955, 3001, 9340
            ]
        assert encrypted_data == valid_encrypted_data

    # handles empty plain_text without errors
    def test_handles_empty_plain_text_without_errors(self, mocker):
        mock_user = mocker.Mock()
        mock_user.public_key = (12345, 67890)  # TODO
        msg = message(chat=mock_user, message_id="2")
        msg.plain_text = ""
        msg.sender = "user_123"
        msg.sent_time_stamp = 1622547800
        msg.received_time_stamp = 1622547900

        encrypted_data = msg.encrypt()
        valid_encrypted_data = [
            6211, 8659, 3094, 195, 6190, 3985, 2511, 4285, 2440, 2770,
            1080, 10609, 1120, 511, 11154, 3196, 10540, 3210, 9271,
            10356, 9346, 2065, 3199, 6679, 106, 10356, 7065, 11950,
            10540, 11461, 9115, 3199, 8230, 4596, 4596, 6085, 8781,
            11700, 6076, 2511, 1171, 874, 2806, 1794, 8359, 4285, 4875,
            7080, 7570, 10750, 8430, 5830, 3001, 9361, 4285, 5061, 2406,
            9556, 1585, 6309, 4596, 9576, 9271, 9556, 6610, 9585, 106,
            646, 10501, 2440, 1080, 10609, 11950, 8365, 1555, 4555,
            3600, 5884, 1335, 9024
            ]
        assert encrypted_data == valid_encrypted_data

    # ensures logging captures the correct error messages
    def test_logging_error_on_encryption_failure(self, mocker, caplog):
        import logging

        mock_user = mocker.Mock()
        mock_user.public_key = ('force error', 67890)
        # an encryption key as type string will cause an encryption failure
        msg = message(chat=mock_user, message_id="1")
        msg.plain_text = "Hello, World!"
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
        mocker.patch('src.peertopeermessagingapp.message.RSA.decrypt_padded', return_value=decrypted_data)

        # Initialize message object and call decrypt
        msg = message(chat=mock_user, message_id=1)
        msg.decrypt(message_data=[111, 222, 333])  # Random data

        # Assertions
        assert msg.plain_text == 'Hello, World!'
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
        mocker.patch('src.peertopeermessagingapp.message.RSA.decrypt_padded', return_value=decrypted_data)
        # TODO: take note of the fact that mocker calls must not be too the
        # TODO cont: actual module but to the module calling that module
        # Initialize message object and call decrypt
        msg = message(chat=mock_user, message_id=1)
        msg.decrypt(message_data=[111, 222, 333])

        caplog.at_level(logging.WARNING)

        # Assertions
        assert msg.plain_text is None
        assert msg.sender == 'user123'
        assert msg.sent_time_stamp == 1622547800
        assert msg.received_time_stamp == 1622547900
        assert f'INVALID message | missing plain_text attribute | message id = {msg.message_id}' in caplog.text


class Test_user_data_store_load:

    def test_encrypt_user_data(self):
        user = user_data(None)  # None is placeholder as unused
        user.set_username('test1')
        user.set_encryption_keys([323, 17], [323, 65537])
        user.set_user_data({'public_key_n': 323, 'public_key_e': 65537})
        encrypted_user_data = user.encrypt_user_data()
        valid_decrypt_checker = [
                    45,
                    45,
                    101,
                    78,
                    45,
                    185,
                    45,
                    298,
                    83
                ]
        assert encrypted_user_data['decrypt_checker'] == valid_decrypt_checker

    def test_load(self):
        user = user_data(None)  # None is placeholder as unused
        username = 'test1'
        data = {
            'decrypt_checker': [45, 45, 101, 78, 45, 185, 45, 298, 83],
            'data': [
                45,
                45,
                176,
                241,
                279,
                46,
                45,
                155,
                13,
                78,
                251,
                175,
                264,
                243,
                95,
                78,
                224,
                1,
                46,
                78,
                95,
                45,
                0,
                204,
                175,
                233,
                117,
                175,
                78,
                84,
                175,
                78,
                282,
                241,
                20,
                204,
                45,
                276,
                85,
                264,
                251,
                297,
                78,
                84,
                252,
                264,
                136,
                296,
                78,
                45,
                276,
                264,
                136,
                1,
                241,
                295,
                58,
                241,
                20,
                139,
                175,
                64,
                223,
                175,
                78,
                123,
                46,
                175
                ]
            }
        decrypted_user_data = user.decrypt_user_data(data, username, privateKN=323, privateKD=17)
        assert decrypted_user_data

import pytest
# from src.peertopeermessagingapp.user_data import user_data as user_data
from src.peertopeermessagingapp.RSA_cryptosystem import encryptChunkedPadded, decryptPadded, genKeys
from src.peertopeermessagingapp.message import message


class Test_Encrypt_Chunked_Padded:

    # encrypts plain text correctly with valid public keys and plain text
    def test_encrypts_and_decrypts_plain_text_correctly(self) -> None:
        private, public = genKeys(
            seed=10,
            complexity=2
        )
        plainText = "hello"
        result = encryptChunkedPadded(
            publicKN=public[0],
            publicKE=public[1],
            plainText=plainText
            )
        decrypted = decryptPadded(
            encrypted=result,
            privateKD=private[1],
            privateKN=private[0]
        )
        assert decrypted == plainText

    # raises ValueError if publicKN is not an integer
    def test_raises_value_error_if_publicKN_not_int(self) -> None:
        publicKN = "not_an_int"
        publicKE = 17
        plainText = "hello"
        with pytest.raises(ValueError, match="expected publicKN type int instead got type <class 'str'>"):
            encryptChunkedPadded(
                publicKN=publicKN,
                publicKE=publicKE,
                plainText=plainText
                )

    # handles plain text with special characters
    def test_handles_plain_text_with_special_characters(self):
        private, public = genKeys(
            seed=10,
            complexity=2
        )
        plainText = "hello$%$_#@_@!)"
        result = encryptChunkedPadded(
            publicKN=public[0],
            publicKE=public[1],
            plainText=plainText
            )
        decrypted = decryptPadded(
            encrypted=result,
            privateKD=private[1],
            privateKN=private[0]
        )
        assert decrypted == plainText

    # processes plain text of varying lengths
    def test_encrypts_plain_text_length_varying_correctly(self) -> None:
        private, public = genKeys(
            seed=10,
            complexity=2
        )
        test_text = ["hello",
                     'hello world',
                     'h',
                     'f8h328h2fhsho[ecdnano[h[hr[238ehd[oshfofhwodfhweo[fh'
                     ]
        for plain_text in test_text:
            result = encryptChunkedPadded(
                publicKN=public[0],
                publicKE=public[1],
                plainText=plain_text
                )
            decrypted = decryptPadded(
                encrypted=result,
                privateKD=private[1],
                privateKN=private[0]
            )
            assert decrypted == plain_text

# the below are to annoying to test take too much processing time

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
    #         decrypted = decryptPadded(
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
    #         decrypted = decryptPadded(
    #             encrypted=result,
    #             privateKD=private[1],
    #             privateKN=private[0]
    #         )
    #         assert decrypted == plainText


class Test_encrypt:

    # Encrypts valid message data correctly with the correct module import
    def test_encrypts_valid_message_data_correctly(self, mocker):
        mock_user = mocker.Mock()
        mock_user.public_key = (12345, 67890) # TODO
        msg = message(user=mock_user, message_id="1")
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
        msg = message(user=mock_user, message_id="2")
        msg.plain_text = ""
        msg.sender = "user_123"
        msg.sent_time_stamp = 1622547800
        msg.received_time_stamp = 1622547900

        encrypted_data = msg.encrypt()
        valid_encrypted_data = [
            6211, 8659, 3094, 195, 6190, 3985, 2511, 4285, 2440, 2770, 1080, 10609, 1120, 511, 11154, 3196, 10540, 3210, 9271, 10356, 9346, 2065, 3199, 6679, 106, 10356, 7065, 11950, 10540, 11461, 9115, 3199, 8230, 4596, 4596, 6085, 8781, 11700, 6076, 2511, 1171, 874, 2806, 1794, 8359, 4285, 4875, 7080, 7570, 10750, 8430, 5830, 3001, 9361, 4285, 5061, 2406, 9556, 1585, 6309, 4596, 9576, 9271, 9556, 6610, 9585, 106, 646, 10501, 2440, 1080, 10609, 11950, 8365, 1555, 4555, 3600, 5884, 1335, 9024
            ]
        assert encrypted_data == valid_encrypted_data

    # ensures logging captures the correct error messages
    def test_logging_error_on_encryption_failure(self, mocker, caplog):
        import logging

        mock_user = mocker.Mock()
        mock_user.public_key = ('force error', 67890)  # an encryption key as type sting will cause an encryption failure
        msg = message(user=mock_user, message_id="1")
        msg.plain_text = "Hello, World!"
        msg.sender = "user_123"
        msg.sent_time_stamp = 1622547800
        msg.received_time_stamp = 1622547900

        with caplog.at_level(logging.ERROR):
            encrypted_data = msg.encrypt()

            assert f"expected publicKN type int instead got type {type('force error')}" in caplog.text
            assert encrypted_data is None

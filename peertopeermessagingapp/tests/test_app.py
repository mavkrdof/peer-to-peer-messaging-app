import pytest
# from src.peertopeermessagingapp.user_data import user_data as user_data
from src.peertopeermessagingapp.RSA_cryptosystem import encryptChunkedPadded, decryptPadded, genKeys


class TestEncryptchunkedpadded:

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
    def test_raises_value_error_if_publickn_not_int(self) -> None:
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
                     'f8h328h2fhsho[ecdnano[h[hr[238ehd[oshfofhwodfhweo[fhe[ofhwe[oh[or2hq3oihq[ofh[fouwehf[oiehfweofhfwe[ofhweo[uhewufhewo[uewho[uewh[ffewh[ouewhf[owuehfwo[ehfwe[iewf]]]]]]]]]]]]]]]]]]]]]']
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

    def test_gen_key_with_varying_complexity(self) -> None:
        for complexity in range(1, 4):
            seed = 10
            private, public = genKeys(
                seed=seed,
                complexity=complexity
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

    def test_gen_key_with_varying_seed(self) -> None:
        for seed in range(10, 20):
            seed *= 10
            private, public = genKeys(
                seed=seed,
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

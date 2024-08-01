# # TODO fix decryption/encryption errors
import logging


def decrypt_padded(encrypted: list[int], private_key_n: int, private_key_d: int) -> str:
    """
    decrypts encrypted text
    args:
        encrypted: list[int]
            a list of encrypted chunks
        private_key_n: int
            private key n
        private_key_d: int
            private key d
    returns:
        decrypted: str
            decrypted text
    """
    logging.debug(f'{__name__}:decrypt_padded: validating args...')
    if isinstance(private_key_n, int):
        if isinstance(private_key_d, int):
            if isinstance(encrypted, list):
                if False not in [False for i in encrypted if not isinstance(i, int)]:
                    logging.debug(f'{__name__}:decrypt_padded: args valid')
                    logging.debug(f'{__name__}:decrypt_padded: decrypting data...')
                    logging.debug(f'{__name__}:decrypt_padded: decrypting into base 10...')
                    decrypted_base10 = []
                    for e_chunk in encrypted:
                        logging.debug(f'{__name__}:decrypt_padded: decrypting on item...')
                        decrypted_base10.append(
                            str(
                                object=decrypt(
                                    private_key_n=private_key_n,
                                    private_key_d=private_key_d,
                                    to_decrypt=e_chunk
                                    )
                                )
                            )
                        logging.debug(f'{__name__}:decrypt_padded: successfully decrypted item')
                    logging.debug(f'{__name__}:decrypt_padded: successfully decrypted data into base 10')
                    logging.debug(f'{__name__}:decrypt_padded: cleaning base 10 decrypted data...')
                    clean_decrypted_base_10 = ""
                    length = len(str(private_key_n)) - 1
                    for chunk in decrypted_base10:
                        while len(chunk) < length:
                            chunk = "0" + chunk
                        clean_decrypted_base_10 += chunk
                    logging.debug(f'{__name__}:decrypt_padded: Successfully cleaned base 10 decrypted data')
                    logging.debug(f'{__name__}:decrypt_padded: Splitting clean base 10 decrypted data')
                    decrypted_split_base_10 = []
                    splitLen = 3  # as the length of asci codes
                    for i in range(int(len(clean_decrypted_base_10) / splitLen)):
                        decrypted_split_base_10.append(
                            int(
                                clean_decrypted_base_10[splitLen*i:splitLen*i+splitLen]
                                )
                            )
                    logging.debug(f'{__name__}:decrypt_padded: successfully split clean base 10 decrypted data into sets of {splitLen}')
                    logging.debug(f'{__name__}:decrypt_padded: converting base 10 to str...')
                    decrypted = base_10_to_string(base10_list=decrypted_split_base_10[1:])
                    logging.debug(f'{__name__}:decrypt_padded: successfully converted base 10 to str')
                    logging.debug(f'{__name__}:decrypt_padded: successfully decrypted data')
                    return decrypted
                else:
                    raise ValueError(
                        f"expected encrypted type list[int] instead got {[type(i) for i in encrypted]}"
                        )
            else:
                raise ValueError(
                    f"expected encrypted type list instead got type {type(encrypted)}"
                    )
        else:
            raise ValueError(
                f"expected privateKN type int instead got type {type(private_key_n)}"
                )
    else:
        raise ValueError(
            f"expected privateKD type int instead got type {type(private_key_d)}"
            )


def decrypt(private_key_n, private_key_d, to_decrypt) -> int:
    """
    decrypts data
    args:
        private_key_n: int
            the private key n
        private_keyE: int
            the private key e
        to encrypt: int
            the data to encrypt must be < Public/private_key N
    """
    if isinstance(private_key_n, int):
        if isinstance(private_key_d, int):
            if isinstance(to_decrypt, int):
                decrypted = (to_decrypt**private_key_d) % private_key_n
                return decrypted
            else:
                raise ValueError(
                    f"expected to_encrypt type int instead got type {type(to_decrypt)}"
                    )
        else:
            raise ValueError(
                f"expected private_keyE type int instead got type {type(private_key_d)}"
                )
    else:
        raise ValueError(
            f"expected private_key_n type int instead got type {type(private_key_n)}"
            )


def base_10_to_string(base10_list) -> str:
    """
    converts string to base 10
    args:
    base10_list: list[int]
        the string to convert
    returns: int
        base 10 version
    """
    if isinstance(base10_list, list):
        if False not in [False for i in base10_list if not isinstance(i, int)]:
            char_list = [chr(i) for i in base10_list]
            clean_str = "".join(char_list)
            return clean_str
        else:
            raise ValueError(
                f"expected base10_list type list[int] instead got {[type(i) for i in base10_list]}"
                )
    else:
        raise ValueError(
            f"expected base10_list type list instead got type {type(base10_list)}"
            )

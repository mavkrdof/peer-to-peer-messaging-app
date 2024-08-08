def encrypt(public_key_n, public_key_e, to_encrypt) -> int:
    """
    encrypts data
    args:
        public_key_n: int
            the public key n
        public_key_e: int
            the public key e
        to_encrypt: int
            data to encrypt must be int and < Public/private_key N
    """
    if isinstance(public_key_n, int):
        if isinstance(public_key_e, int):
            if isinstance(to_encrypt, int):
                if to_encrypt < public_key_n:
                    encrypted = (to_encrypt**public_key_e) % public_key_n
                    return encrypted
                else:
                    raise ValueError(
                        "expected to_encrypt < public_key_n instead got >"
                        )
            else:
                raise ValueError(
                    f"expected to_encrypt type int instead got type {type(to_encrypt)}"
                    )
        else:
            raise ValueError(
                f"expected public_key_e type int instead got type {type(public_key_e)}"
                )
    else:
        raise ValueError(
            f"expected public_key_n type int instead got type {type(public_key_n)}"
            )


def encrypt_data(public_key_n=None, public_key_e=None, plain_text=None) -> list[int]:
    """
    encrypts plain text
    args:
        public_key_n: int
            public key n
        public_key_e: int
            public key e
        plain_text: str
            plain text
    returns:
        encrypted: list[int]
            encrypted data
    """
    if isinstance(public_key_n, int):
        if isinstance(public_key_e, int):
            if isinstance(plain_text, str):
                data = str_to_base10_by_char(string=plain_text)
                encrypted = []
                for chunk in data:
                    encrypted.append(
                        encrypt(
                            public_key_n=public_key_n,
                            public_key_e=public_key_e,
                            to_encrypt=chunk
                            )
                        )
                return encrypted
            else:
                raise ValueError(
                    f"expected plainText type str instead got type {type(plain_text)}"
                    )
        else:
            raise ValueError(
                f"expected publicKE type int instead got type {type(public_key_e)}"
                )
    else:
        raise ValueError(
            f"expected publicKN type int instead got type {type(public_key_n)}"
            )


def str_to_base10_by_char(string) -> list[int]:
    """
    converts string to base 10
    args:
    string: str
        the string to convert
    returns: int
        base 10 version
    """
    if isinstance(string, str):
        int_str_list = [ord(i) for i in string]
        return int_str_list
    else:
        raise ValueError(f"expected string type str instead got type {type(string)}")

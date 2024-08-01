# # TODO fix decryption/encryption errors
import math_stuff


def encrypt_chunked_padded(public_key_n=None, public_key_e=None, plain_text=None) -> list[int]:
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
                data = str_to_base10_padded(string=plain_text)
                data_chunks = chunk_data(data=data, public_key_n=public_key_n)
                encrypted = []
                for chunk in data_chunks:
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


def str_to_base10_padded(string) -> int:
    """
    converts string to base 10 - fixes errors in strToBase10 by adding padding that cancels out when unconverted
    args:
    string: str
        the string to convert
    returns: int
        base 10 version
    """
    if isinstance(string, str):
        int_str_list = [str(ord(i)).rjust(3, '0') for i in string]
        clean_int = 111
        for num in int_str_list:
            clean_int = math_stuff.append_to_int(num=clean_int, to_add=num)
        return clean_int
    else:
        raise ValueError(f"expected string type str instead got type {type(string)}")


def chunk_data(data, public_key_n) -> list[int]:
    """
    chunks the data into sizes manageable by encrypted.
    can only encrypt data smaller than public key n
    args:
        data: int
            raw unchanged data
        public_key_n: int
            the public key n
    returns:
        chunked_data: list[int]
            the chunked data
    """
    if isinstance(data, int):
        if isinstance(public_key_n, int):
            if public_key_n > 9:
                if data < public_key_n:
                    return [data]
                else:
                    length = len(str(public_key_n)) - 1
                    chunks = round(len(str(data)) / length)
                    chunked_data = []
                    for i in range(chunks):
                        chunked_data.append(int(str(data)[i*length: (i+1)*length]))
                    return chunked_data
            else:
                raise ValueError("public_key_n must be greater than 9 to accurately encrypt data")
        else:
            raise ValueError(f"expected public_key_n type int instead got type {type(public_key_n)}")
    else:
        raise ValueError(f"expected data type int instead got type {type(data)}")


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

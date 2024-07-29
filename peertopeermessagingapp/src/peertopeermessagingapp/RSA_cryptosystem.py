import logging
import random  # NOT required if NOT using prime from cache
import csv
import time  # NOT required if NOT using prime from cache
import peertopeermessagingapp.math_stuff as math_stuff
"""
a module implementing RSA encryption
Inspiration: https://en.wikipedia.org/wiki/RSA_(cryptosystem)#Operation
Author: Connor Cuffe
"""


def generate_2_prime_numbers(generator_seed, complexity: int | float = 2) -> tuple[int, int]:  # TODO optimise
    """
    a simple algorithm too generate 2 prime numbers
    args:
        generatorSeed: int
            a large integer used to generate the prime numbers - low performance with large seed
        complexity: int | float
            the complexity of the prime numbers - low performance with high complexity. default 2
    returns:
        p, q: int, int
            prime nums
    """
    if isinstance(generator_seed, int):
        if isinstance(complexity, (int, float)):
            logging.info('finding prime number p...')
            p_start_time = time.time()
            p = math_stuff.find_nearest_prime(
                number=round(generator_seed ** round(complexity/2)), search_direction=1
                )
            p_end_time = time.time() - p_start_time
            logging.info(f'found prime number p after {p_end_time} Seconds')
            logging.info('finding prime number q...')
            q_start_time = time.time()
            q = math_stuff.find_nearest_prime(
                number=round(generator_seed ** complexity), search_direction=1
                )
            q_end_time = time.time() - q_start_time
            logging.info(f'found prime number q after {q_end_time} Seconds')
            logging.info('found prime number successfully')
            return p, q
        else:
            raise ValueError(f"expected complexity type int instead got {type(complexity)}")
    else:
        raise ValueError(f"expected generatorSeed type int instead got {type(generator_seed)}")


def random_prime_nums_from_cache(cache, error_handling=False, complexity=100) -> int:
    """
    a simple algorithm to generate a prime number from a cache of primes
    - stable performance no matter size of desired prime unless error checking is enabled
    - requires a large cache file for best security.
    - less secure
    args:
        cache: int
            the prime cache
        error_handling: bool
            whether or not to do error handling
        complexity: int
            the complexity default 100
    returns:
        prime: int
            a prime num
    """
    with open(cache, "r") as file:
        prime_cache = list(set(list(csv.reader(file))[0][:complexity]))
    seed = random.randint(0, len(prime_cache)-1)
    prime = "str"
    try:
        prime = int(prime_cache[seed])
    except ValueError:
        raise ValueError(f"prime Cache Invalid {prime}")
    if error_handling:
        if math_stuff.is_prime(prime):  # reduces efficiency as is_prime is expensive.
            return prime
        else:
            raise ValueError(f"prime Cache Invalid: {prime}")
    else:
        return prime


def gen_2_prime_nums_from_cache(cache) -> tuple[int, int]:
    """
    a simple algorithm to generate
    2 prime number from a cache of prime - less secure
    args:
        cache: int
            the prime cache
    returns:
        p, q: int, int
            2 prime nums
    """
    return (
        random_prime_nums_from_cache(
            cache=cache,
            error_handling=True,
            complexity=100
            ),
        random_prime_nums_from_cache(
            cache=cache,
            error_handling=True,
            complexity=100
            )
    )


def create_key(p, q) -> tuple[list[int], list[int]]:
    """
    creates public and private keys based on to prime numbers
    args:
        p: int
            prime num 1 - should be large and unpredictable for best security - low performance with large ints
        q: int
            prime num 2 - should be large and unpredictable for best security - low performance with large ints
        returns:
            public_key: list[int, int]
            private_key: list[int, int]
    """
    create_key_start_time = time.time()
    if isinstance(p, int):
        if isinstance(q, int):
            logging.info('starting calculate keys...')

            # calculate n
            n = p * q
            if n > 9:  # checks if n valid
                logging.info('n successfully calculated')

                # calculate carmichael number for n (k)
                logging.info('calculating carmichael...')
                carmichael_start_time = time.time()
                k = math_stuff.carmichael(n=n)  # TODO optimise takes 90 percent of time
                logging.info(f'successfully calculated carmichael in {time.time() - carmichael_start_time}s')

                # calculate number co_prime to k (e)
                logging.info('finding prime co_prime (e)...')
                e_start_time = time.time()
                # this if statement if makes calculating e hundreds of times faster
                # used to take 9 secs for key < 20 now takes 0 seconds
                if math_stuff.is_co_prime(65537, k):
                    e = 65537
                else:
                    logging.info('calculating co-prime list...')
                    co_prime_start_time = time.time()
                    co_prime_list = math_stuff.find_co_prime(a=k)
                    logging.info(f'successful calculated co-prime list in {time.time() - co_prime_start_time}s')
                    e = None
                    co_prime_list.reverse()  # reverses co-prime list therefore will find largest co-prime first
                    for count, co_prime in enumerate(co_prime_list):
                        logging.info(f'finding e {(count / len(co_prime_list)) * 100}%')
                        if math_stuff.is_prime(n=co_prime):
                            e = co_prime
                            break
                logging.info(f'found e in {time.time() - e_start_time}s')

                # calculate modular multiplicative inverse (d)
                logging.info('finding modular multiplicative inverse (d)...')
                d_start_time = time.time()
                d = math_stuff.find_modular_multiplicative_inverse(
                    a=e,
                    m=k
                    )
                logging.info(f'successfully found d in {time.time() - d_start_time}')

                # format and return keys
                public_key = [n, e]
                private_key = [n, d]
                logging.info(f'returning asymmetric encryption keys after {time.time() - create_key_start_time}')
                return public_key, private_key
            else:
                raise ValueError(
                    f'{__name__}:create_key: n must be greater than 9 instead got {n}'
                )
        else:
            raise ValueError(
                "{__name__}:create_key: expected q type int instead got type {type(q)}"
                )
    else:
        raise ValueError(
            "{__name__}:create_key: expected p type int instead got type {type(p)}"
            )


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


def str_to_base_10(string) -> int:
    """
    converts string to base 10 - error prone when uncovering as not all 3 ints long
    args:
    string: str
        the string to convert
    returns: int
        base 10 version
    """
    if isinstance(string, str):
        int_list = [ord(i) for i in string]
        clean_int = int_list[0]
        for num in int_list[1:]:
            clean_int = math_stuff.append_to_int(clean_int, num)
        return clean_int
    else:
        raise ValueError(
            f"expected string type str instead got type {type(string)}"
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


def str_to_base10_list(string) -> list[int]:
    """
    converts string to base 10 - fixes errors in strToBase10
    args:
    string: str
        the string to convert
    returns: list[int]
        base 10 version
    """
    if isinstance(string, str):
        int_list = [ord(i) for i in string]
        return int_list
    else:
        raise ValueError(
            f"expected string type str instead got type {type(string)}"
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


def decrypt_padded(encrypted, private_key_n, private_key_d) -> str:
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
    if isinstance(private_key_n, int):
        if isinstance(private_key_d, int):
            if isinstance(encrypted, list):
                if False not in [False for i in encrypted if not isinstance(i, int)]:
                    decrypted_base10 = []
                    for e_chunk in encrypted:
                        decrypted_base10.append(
                            str(
                                object=decrypt(
                                    private_key_n=private_key_n,
                                    private_key_d=private_key_d,
                                    to_decrypt=e_chunk
                                    )
                                )
                            )
                    clean_decrypted_base_10 = ""
                    length = len(str(private_key_n)) - 1
                    for chunk in decrypted_base10:
                        while len(chunk) < length:
                            chunk = "0" + chunk
                        clean_decrypted_base_10 += chunk
                    decrypted_split_base_10 = []
                    splitLen = 3
                    for i in range(int(len(clean_decrypted_base_10) / splitLen)):
                        decrypted_split_base_10.append(
                            int(
                                clean_decrypted_base_10[splitLen*i:splitLen*i+splitLen]
                                )
                            )
                    decrypted = base_10_to_string(base10_list=decrypted_split_base_10[1:])
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


def gen_keys(seed, complexity) -> tuple[list[int], list[int]]:
    """
    generates prime numbers and then
    gens public and private keys for RSA encryption.
    args:
        seed: int
            the seed for the primes
        complexity: int
            the complexity of the primes
    returns: private key: list[int, int], public key: list[int, int]
        the private and public keys
    """
    if isinstance(seed, int):
        if isinstance(complexity, (float, int)):
            if seed > 9:
                if complexity >= 1:
                    logging.info('generating keys...')
                    logging.info('generating prime numbers...')
                    p, q = generate_2_prime_numbers(
                        generator_seed=seed, complexity=complexity
                        )  # only needs to run once at creation of account
                    logging.info('prime numbers successfully generated')
                    # larger num = better but longer initial calc time
                    logging.info('calculating keys from prime numbers...')
                    public_key, private_key = create_key(p, q)  # only needs to run once at creation of account
                    logging.info('keys successfully calculated')
                    logging.info('gen keys finished successfully')
                    return private_key, public_key
                else:
                    raise ValueError(
                        f'{__name__}:gen_keys: expected complexity greater than or = to 1 instead got {complexity}'
                    )
            else:
                raise ValueError(
                    f'{__name__}:gen_keys: expected seed greater than 9 instead got {seed}'
                )
        else:
            raise ValueError(
                f"{__name__}:gen_keys: expected complexity type int instead got type {type(complexity)}"
                )
    else:
        raise ValueError(
            f"{__name__}:gen_keys: expected seed type int instead got type {type(seed)}"
            )


if __name__ == '__main__':
    private_key, public_key = gen_keys(
        seed=random.randint(0, 10),
        complexity=2
        )
    while True:
        message = input(
            "Message: "
            )
        e = encrypt_chunked_padded(
            public_key_n=public_key[0],
            public_key_e=public_key[1],
            plain_text=message
            )
        print(e)
        print(
            decrypt_padded(
                encrypted=e,
                private_key_n=private_key[0],
                private_key_d=private_key[1]
                )
            )

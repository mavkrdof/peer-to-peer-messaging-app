import logging
import math_stuff
import time


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

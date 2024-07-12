"""
a module with a bunch of math stuff used by RSA cryptosystem
"""


def carmichael(n) -> int:
    """
    finds the number k.
    that all co_primes of n when to the power of k is mod n = 1
    (for num all x x**k % n = 1)
    args:
        n: int
            the value n
    returns: int
        the values k
    """
    if isinstance(n, int):
        co_primes = find_co_prime(n)
        k = 1
        while not all(x**k % n == 1 for x in co_primes):
            k += 1
        return k
    else:
        raise ValueError(
            f"expected n type int instead got type {type(n)}"
            )


def find_nearest_prime(number, search_direction=1) -> int:
    """
    finds the nearest prime to number in the search_direction
    args:
        number: int
            the number to find the nearest prime to
        search_direction: 1 or -1
            the direction to search
    returns: int
        the nearest prime number to number
    """
    if isinstance(number, int):
        if search_direction == 1 or -1:
            if number % 2 == 0:
                number += 1
            else:
                number += 2
            while not is_prime(number):
                number += 2 * search_direction
            return number
        else:
            raise ValueError(
                f"expected search_direction 1 or 0 instead got type {search_direction}"
                )
    else:
        raise ValueError(
            f"expected number type int instead got type {type(number)}"
            )


def find_co_prime(a) -> list[int]:
    """
    finds co_primes of a - values that their only greatest common divisor is 1 ignores one cause one is coPrime to all
    args:
        a: int
            values a
    returns:
        all co_primes of a
    """
    if isinstance(a, int):
        co_primes = []
        for x in range(2, a):
            if is_co_prime(a=x, b=a):
                co_primes.append(x)
        return co_primes
    else:
        raise ValueError(
            f"expected a type int instead got type {type(a)}"
            )


def find_modular_multiplicative_inverse(a, m) -> int:
    """
    finds the modular multiplicative inverse x of a to m
    args:
        a: int
            the value for a for a*x % m = 1
        m: int
            the value for m for a*x % m = 1
    returns: int
        the modular multiplicative inverse of a and m
    """
    if isinstance(a, int) or isinstance(a, float):
        if isinstance(m, int) or isinstance(m, float):
            x = 1
            while True:  # TODO ensure this is not an infinite loop
                if (a * x) % m == 1:
                    return x
                x += 1
        else:
            raise ValueError(
                f"expected m type int, float instead got type {type(m)}"
                )
    else:
        raise ValueError(
            f"expected a type int, float instead got type {type(a)}"
            )


def is_prime(n) -> bool:
    """
    checks if n is prime
    args:
        n: int
            the value to check if prime
    returns: bool
        if prime
    """
    if isinstance(n, int):
        for i in range(2, n):
            if (n % i) == 0:
                return False
        return True
    raise ValueError(
        f"expected n type int instead got type {type(n)}"
        )


def is_co_prime(a, b) -> bool:
    """
    checks if a is coPrime to b
    args:
        a: int
            value a
        b: int
            value b
    returns: bool
        if a is coPrime to b
    """
    if isinstance(a, int):
        if isinstance(b, int):
            if greatest_common_divisor(a, b) == 1:
                return True
            else:
                return False
        else:
            raise ValueError(
                f"expected b type int instead got type {type(b)}"
                )
    else:
        raise ValueError(
            f"expected a type int instead got type {type(a)}"
            )


def greatest_common_divisor(x, y) -> int:
    """
    finds the gdc of x, y
    args:
        x: int
            one of the values to find gdc of
        y: int
            one of the values to find gdc of
    returns: int
        the gdc of x and y
    """
    if isinstance(x, int):
        if isinstance(y, int):
            gdc = 0
            for num in range(1, min(x, y)+1):
                if x % num == 0 and y % num == 0:
                    gdc = num
            return gdc
        else:
            raise ValueError(
                f"expected y type int instead got type {type(y)}"
                )
    else:
        raise ValueError(
            f"expected x type int instead got type {type(x)}"
            )


def append_to_int(num, to_add) -> int:
    """
    appends integers to an integer eg: num = 134, to_add = 23: Returns 13423
    args:
        num: int or str nums only
            the number to append to
        to_add: int or str nums only
            the number to append
    returns:
        to_add appended to Num: int
    """
    if isinstance(num, int) or (isinstance(num, str) and num.isnumeric()):
        if isinstance(to_add, int) or (isinstance(to_add, str) and to_add.isnumeric()):
            to_addStr = str(to_add)
            strNum = str(num)
            final = int(strNum + to_addStr)
            return final
        else:
            raise ValueError(
                f"expected to_add type int or num str instead got type {type(to_add)}"
                )
    else:
        raise ValueError(
            f"expected num type int or num str instead got type {type(num)}"
            )

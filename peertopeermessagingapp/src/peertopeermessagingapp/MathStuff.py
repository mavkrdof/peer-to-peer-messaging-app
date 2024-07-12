"""
a module with a bunch of math stuff used by RSA cryptosystem
"""


def carmichael(n) -> int:
    """
    finds the number k.
    that all coPrimes of n when to the power of k is mod n = 1
    (for num all x x**k % n = 1)
    args:
        n: int
            the value n
    returns: int
        the values k
    """
    if isinstance(n, int):
        coPrimes = FindCoPrime(n)
        k = 1
        while not all(x**k % n == 1 for x in coPrimes):
            k += 1
        return k
    else:
        raise ValueError(
            f"expected n type int instead got type {type(n)}"
            )


def FindNearestPrime(number, searchDirection=1) -> int:
    """
    finds the nearest prime to number in the searchDirection
    args:
        number: int
            the number to find the nearest prime to
        searchDirection: 1 or -1
            the direction to search
    returns: int
        the nearest prime number to number
    """
    if isinstance(number, int):
        if searchDirection == 1 or -1:
            if number % 2 == 0:
                number += 1
            else:
                number += 2
            while not isPrime(number):
                number += 2 * searchDirection
            return number
        else:
            raise ValueError(
                f"expected searchDirection 1 or 0 instead got type {searchDirection}"
                )
    else:
        raise ValueError(
            f"expected number type int instead got type {type(number)}"
            )


def FindCoPrime(a):
    """
    finds coPrimes of a - values that their only greatest common divisor is 1 ignores one cause one is coPrime to all
    args:
        a: int
            values a
    returns:
        all coPrimes of a
    """
    if isinstance(a, int):
        coPrimes = []
        for x in range(2, a):
            if isCoPrime(x, a):
                coPrimes.append(x)
        return coPrimes
    else:
        raise ValueError(
            f"expected a type int instead got type {type(a)}"
            )


def FindModularMultiplicativeInverse(a, m) -> int | None:
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
            notFound = True
            x = 1
            while notFound:
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


def isPrime(n) -> bool:
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


def isCoPrime(a, b) -> bool:
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
            if greatestCommonDivisor(a, b) == 1:
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


def greatestCommonDivisor(x, y) -> int:
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


def appendToInt(num, toAdd) -> int:
    """
    appends integers to an integer eg: num = 134, toAdd = 23: Returns 13423
    args:
        num: int or str nums only
            the number to append to
        toAdd: int or str nums only
            the number to append
    returns:
        toAdd appended to Num: int
    """
    if isinstance(num, int) or (isinstance(num, str) and num.isnumeric()):
        if isinstance(toAdd, int) or (isinstance(toAdd, str) and toAdd.isnumeric()):
            toAddStr = str(toAdd)
            strNum = str(num)
            final = int(strNum + toAddStr)
            return final
        else:
            raise ValueError(
                f"expected toAdd type int or num str instead got type {type(toAdd)}"
                )
    else:
        raise ValueError(
            f"expected num type int or num str instead got type {type(num)}"
            )

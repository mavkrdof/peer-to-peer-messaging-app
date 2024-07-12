import random  # NOT required if NOT using prime from cache
import csv  # NOT required if NOT using prime from cache
import peertopeermessagingapp.MathStuff as math_stuff
"""
a module implementing RSA encryption
"""


def generate2PrimeNumbers(generatorSeed, complexity=2) -> tuple[int, int]:
    """
    a simple algorithm too generate 2 prime numbers
    args:
        generatorSeed: int
            a large integer used to generate the prime numbers - low performance with large seed
        complexity: int
            the complexity of the prime numbers - low performance with high complexity. default 2
    returns:
        p, q: int, int
            prime nums
    """
    if isinstance(generatorSeed, int):
        if isinstance(complexity, int):
            p = math_stuff.FindNearestPrime(
                number=generatorSeed ** round(complexity/2), searchDirection=1
                )
            q = math_stuff.FindNearestPrime(
                number=generatorSeed ** complexity, searchDirection=1
                )
            return p, q
        else:
            raise ValueError(f"expected complexity type int instead got {type(complexity)}")
    else:
        raise ValueError(f"expected generatorSeed type int instead got {type(generatorSeed)}")


def randomPrimeNumsFromCache(cache, errorHandling=False, complexity=100) -> int:
    """
    a simple algorithm to generate a prime number from a cache of primes
    - stable performance no matter size of desired prime unless error checking is enabled
    - requires a large cache file for best security.
    - less secure
    args:
        cache: int
            the prime cache
        errorHandling: bool
            whether or not to do error handling
        complexity: int
            the complexity default 100
    returns:
        prime: int
            a prime num
    """
    with open(cache, "r") as file:
        primeCache = list(set(list(csv.reader(file))[0][:complexity]))
    seed = random.randint(0, len(primeCache)-1)
    prime = "str"
    try:
        prime = int(primeCache[seed])
    except ValueError:
        raise ValueError(f"prime Cache Invalid {prime}")
    if errorHandling:
        if math_stuff.isPrime(prime):  # reduces efficiency as isPrime is expensive.
            return prime
        else:
            raise ValueError(f"prime Cache Invalid: {prime}")
    else:
        return prime


def gen2PrimeNumsFromCache(cache) -> tuple[int, int]:
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
        randomPrimeNumsFromCache(
            cache=cache,
            errorHandling=True,
            complexity=100
            ),
        randomPrimeNumsFromCache(
            cache=cache,
            errorHandling=True,
            complexity=100
            )
    )


def createKey(p, q) -> tuple[list[int], list[int]]:
    """
    creates public and private keys based on to prime numbers
    args:
        p: int
            prime num 1 - should be large and unpredictable for best security - low performance with large ints
        q: int
            prime num 2 - should be large and unpredictable for best security - low performance with large ints
        returns:
            publicKey: list[int, int]
            privateKey: list[int, int]
    """
    if isinstance(p, int):
        if isinstance(q, int):
            if math_stuff.isPrime(p):
                if math_stuff.isPrime(q):
                    n = p * q
                    if n > 9:
                        k = math_stuff.carmichael(n=n)
                        coPrimeList = math_stuff.FindCoPrime(a=k)
                        e = None
                        for coPrime in coPrimeList:
                            if math_stuff.isPrime(n=coPrime):
                                e = coPrime
                        d = math_stuff.FindModularMultiplicativeInverse(
                            a=e,
                            m=k
                            )
                        publicKey = [n, e]
                        privateKey = [n, d]
                        return publicKey, privateKey
                    else:
                        raise ValueError(
                            "n must be greater than 9 to accurately encrypt data"
                            )
                else:
                    raise ValueError(
                        "expected q to be prime instead got not prime"
                        )
            else:
                raise ValueError(
                    "expected p to be prime instead got not prime"
                    )
        else:
            raise ValueError(
                "expected q type int instead got type {type(q)}"
                )
    else:
        raise ValueError(
            "expected p type int instead got type {type(p)}"
            )


def chunkData(data, publicKeyN) -> list[int]:
    """
    chunks the data into sizes manageable by encrypted.
    can only encrypt data smaller than public key n
    args:
        data: int
            raw unchanged data
        publicKeyN: int
            the public key n
    returns:
        chunkedData: list[int]
            the chunked data
    """
    if isinstance(data, int):
        if isinstance(publicKeyN, int):
            if publicKeyN > 9:
                if data < publicKeyN:
                    return [data]
                else:
                    length = len(str(publicKeyN)) - 1
                    chunks = round(len(str(data)) / length)
                    chunkedData = []
                    for i in range(chunks):
                        chunkedData.append(int(str(data)[i*length: (i+1)*length]))
                    return chunkedData
            else:
                raise ValueError("publicKeyN must be greater than 9 to accurately encrypt data")
        else:
            raise ValueError(f"expected publicKeyN type int instead got type {type(publicKeyN)}")
    else:
        raise ValueError(f"expected data type int instead got type {type(data)}")


def encrypt(publicKeyN, publicKeyE, toEncrypt) -> int:
    """
    encrypts data
    args:
        publicKeyN: int
            the public key n
        publicKeyE: int
            the public key e
        toEncrypt: int
            data to encrypt must be int and < Public/PrivateKey N
    """
    if isinstance(publicKeyN, int):
        if isinstance(publicKeyE, int):
            if isinstance(toEncrypt, int):
                if toEncrypt < publicKeyN:
                    encrypted = (toEncrypt**publicKeyE) % publicKeyN
                    return encrypted
                else:
                    raise ValueError(
                        "expected toEncrypt < publicKeyN instead got >"
                        )
            else:
                raise ValueError(
                    f"expected toEncrypt type int instead got type {type(toEncrypt)}"
                    )
        else:
            raise ValueError(
                f"expected publicKeyE type int instead got type {type(publicKeyE)}"
                )
    else:
        raise ValueError(
            f"expected publicKeyN type int instead got type {type(publicKeyN)}"
            )


def decrypt(privateKeyN, privateKeyD, toDecrypt) -> int:
    """
    decrypts data
    args:
        privateKeyN: int
            the private key n
        privateKeyE: int
            the private key e
        to encrypt: int
            the data to encrypt must be < Public/PrivateKey N
    """
    if isinstance(privateKeyN, int):
        if isinstance(privateKeyD, int):
            if isinstance(toDecrypt, int):
                decrypted = (toDecrypt**privateKeyD) % privateKeyN
                return decrypted
            else:
                raise ValueError(
                    f"expected toEncrypt type int instead got type {type(toDecrypt)}"
                    )
        else:
            raise ValueError(
                f"expected privateKeyE type int instead got type {type(privateKeyD)}"
                )
    else:
        raise ValueError(
            f"expected privateKeyN type int instead got type {type(privateKeyN)}"
            )


def strToBase10(string) -> int:
    """
    converts string to base 10 - error prone when uncovering as not all 3 ints long
    args:
    string: str
        the string to convert
    returns: int
        base 10 version
    """
    if isinstance(string, str):
        intList = [ord(i) for i in string]
        cleanInt = intList[0]
        for num in intList[1:]:
            cleanInt = math_stuff.appendToInt(cleanInt, num)
        return cleanInt
    else:
        raise ValueError(
            f"expected string type str instead got type {type(string)}"
            )


def strToBase10Padded(string) -> int:
    """
    converts string to base 10 - fixes errors in strToBase10 by adding padding that cancels out when unconverted
    args:
    string: str
        the string to convert
    returns: int
        base 10 version
    """
    if isinstance(string, str):
        intStrList = [str(ord(i)).rjust(3, '0') for i in string]
        cleanInt = 111
        for num in intStrList:
            cleanInt = math_stuff.appendToInt(cleanInt, num)
        return cleanInt
    else:
        raise ValueError(f"expected string type str instead got type {type(string)}")


def strToBase10List(string) -> list[int]:
    """
    converts string to base 10 - fixes errors in strToBase10
    args:
    string: str
        the string to convert
    returns: list[int]
        base 10 version
    """
    if isinstance(string, str):
        intList = [ord(i) for i in string]
        return intList
    else:
        raise ValueError(
            f"expected string type str instead got type {type(string)}"
            )


def base10ToString(base10List) -> str:
    """
    converts string to base 10
    args:
    base10List: list[int]
        the string to convert
    returns: int
        base 10 version
    """
    if isinstance(base10List, list):
        if False not in [False for i in base10List if not isinstance(i, int)]:
            charList = [chr(i) for i in base10List]
            cleanStr = "".join(charList)
            return cleanStr
        else:
            raise ValueError(
                f"expected base10List type list[int] instead got {[type(i) for i in base10List]}"
                )
    else:
        raise ValueError(
            f"expected base10List type list instead got type {type(base10List)}"
            )


def decryptPadded(encrypted, privateKN, privateKD) -> str:
    """
    decrypts encrypted text
    args:
        encrypted: list[int]
            a list of encrypted chunks
        privateKN: int
            private key n
        privateKD: int
            private key d
    returns:
        decrypted: str
            decrypted text
    """
    if isinstance(privateKN, int):
        if isinstance(privateKD, int):
            if isinstance(encrypted, list):
                if False not in [False for i in encrypted if not isinstance(i, int)]:
                    decryptedBase10 = []
                    for eChunk in encrypted:
                        decryptedBase10.append(
                            str(
                                object=decrypt(
                                    privateKeyN=privateKN,
                                    privateKeyD=privateKD,
                                    toDecrypt=eChunk
                                    )
                                )
                            )
                    cleanDecryptedBase10 = ""
                    length = len(str(privateKN)) - 1
                    for chunk in decryptedBase10:
                        while len(chunk) < length:
                            chunk = "0" + chunk
                        cleanDecryptedBase10 += chunk
                    decryptedSplitBase10 = []
                    splitLen = 3
                    for i in range(int(len(cleanDecryptedBase10) / splitLen)):
                        decryptedSplitBase10.append(
                            int(
                                cleanDecryptedBase10[splitLen*i:splitLen*i+splitLen]
                                )
                            )
                    decrypted = base10ToString(decryptedSplitBase10[1:])
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
                f"expected privateKN type int instead got type {type(privateKN)}"
                )
    else:
        raise ValueError(
            f"expected privateKD type int instead got type {type(privateKD)}"
            )


def encryptChunkedPadded(publicKN=None, publicKE=None, plainText=None) -> list[int]:
    """
    encrypts plain text
    args:
        publicKN: int
            public key n
        publicKE: int
            public key e
        plainText: str
            plain text
    returns:
        encrypted: list[int]
            encrypted data
    """
    if isinstance(publicKN, int):
        if isinstance(publicKE, int):
            if isinstance(plainText, str):
                data = strToBase10Padded(string=plainText)
                dataChunks = chunkData(data=data, publicKeyN=publicKN)
                encrypted = []
                for chunk in dataChunks:
                    encrypted.append(
                        encrypt(
                            publicKeyN=publicKN,
                            publicKeyE=publicKE,
                            toEncrypt=chunk
                            )
                        )
                return encrypted
            else:
                raise ValueError(
                    f"expected plainText type str instead got type {type(plainText)}"
                    )
        else:
            raise ValueError(
                f"expected publicKE type int instead got type {type(publicKE)}"
                )
    else:
        raise ValueError(
            f"expected publicKN type int instead got type {type(publicKN)}"
            )


def genKeys(seed, complexity) -> tuple[list[int], list[int]]:
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
        if isinstance(complexity, int):
            if seed > 9:
                if complexity >= 1:
                    p, q = generate2PrimeNumbers(
                        generatorSeed=seed, complexity=complexity
                        )  # only needs to run once at creation of account
                    # larger num = better but longer initial calc time
                    publicKey, privateKey = createKey(p, q)  # only needs to run once at creation of account
                    return privateKey, publicKey
                else:
                    raise ValueError(
                        f'expected complexity greater than or = to 1 instead got {complexity}'
                    )
            else:
                raise ValueError(
                    f'expected seed greater than 9 instead got {seed}'
                )
        else:
            raise ValueError(
                f"expected complexity type int instead got type {type(complexity)}"
                )
    else:
        raise ValueError(
            f"expected seed type int instead got type {type(seed)}"
            )


if __name__ == '__main__':
    privateKey, publicKey = genKeys(
        seed=random.randint(0, 10),
        complexity=2
        )
    while True:
        message = input(
            "Message: "
            )
        e = encryptChunkedPadded(
            publicKN=publicKey[0],
            publicKE=publicKey[1],
            plainText=message
            )
        print(e)
        print(
            decryptPadded(
                encrypted=e,
                privateKN=privateKey[0],
                privateKD=privateKey[1]
                )
            )

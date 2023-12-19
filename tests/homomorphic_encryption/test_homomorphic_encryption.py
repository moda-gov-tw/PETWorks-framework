from unittest.mock import patch
from PETWorks.homomorphic_encryption import (
    generateKey,
    encrypt,
    decrypt,
    capturePackets,
)


def testGenerateKey():
    library = "phe"
    keySize = 128

    publicKey, privateKey = generateKey(keySize, library)

    assert type(publicKey) == int
    assert set(privateKey.keys()) == {"p", "q"}


def testEncrypt():
    library = "phe"
    keySize = 128
    publicKey = 240537853022521961474293276399056393697

    value = 16

    encryptedValue = encrypt(value, keySize, library, publicKey)

    assert encryptedValue != value


def testDecrypt():
    library = "phe"
    keySize = 128
    publicKey = 240537853022521961474293276399056393697
    privateKey = {"p": 15077889811522283831, "q": 15953018361939928487}

    encryptedValue = 54460907148015048399650723031319333758655292473353853450480678347318563444904

    decryptedValue = decrypt(
        encryptedValue, keySize, library, publicKey, privateKey
    )

    assert decryptedValue == 16

import pytest
from PETWorks.homomorphic_encryption import Paillier


@pytest.fixture(scope="function")
def paillierObj():
    return Paillier(nLength=128)


def testEncryptionAndDecryption(paillierObj):
    number = 16

    publicKey, privateKey = paillierObj.generateKey()

    encrypted = paillierObj.encrypt(publicKey, number)

    decrypted = paillierObj.decrypt(privateKey, publicKey, encrypted)

    assert decrypted == number

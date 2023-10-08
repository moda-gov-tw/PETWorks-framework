from typing import Dict, Tuple, Union
from phe import paillier
from phe.paillier import (
    PaillierPublicKey,
    PaillierPrivateKey,
    EncryptedNumber,
    DEFAULT_KEYSIZE,
)


class Paillier:
    PrivateKey = Dict[str, int]
    PublicKey = int

    def __init__(self, nLength=DEFAULT_KEYSIZE) -> None:
        self.nLength = nLength

    def generateKey(self) -> Tuple[int, Dict[str, int]]:
        publicKey, privateKey = paillier.generate_paillier_keypair(
            n_length=self.nLength
        )

        return self.__publicKeyToBuiltIn(
            publicKey
        ), self.__privateKeyToBuiltIn(privateKey)

    def encrypt(self, publicKey: PublicKey, value: Union[int, float]) -> int:
        publicKeyObj = self.__publicKeyToLibraryObj(publicKey)

        ciphertext = publicKeyObj.encrypt(value).ciphertext()

        return ciphertext

    def decrypt(
        self, privateKey: PrivateKey, publicKey: PublicKey, encryptedNum: int
    ) -> int:
        publicKeyObj = self.__publicKeyToLibraryObj(publicKey)
        privateKeyObj = self.__privateKeyToLibraryObj(
            privateKey, publicKey=publicKeyObj
        )

        encryptedNumObj = EncryptedNumber(
            public_key=publicKeyObj, ciphertext=encryptedNum
        )

        return privateKeyObj.decrypt(encryptedNumObj)

    @staticmethod
    def __publicKeyToBuiltIn(publicKey: PaillierPublicKey) -> Dict[str, int]:
        return publicKey.n

    @staticmethod
    def __publicKeyToLibraryObj(publicKey: PublicKey) -> PaillierPublicKey:
        return PaillierPublicKey(publicKey)

    @staticmethod
    def __privateKeyToBuiltIn(
        privateKey: PaillierPrivateKey,
    ) -> Dict[str, int]:
        return {"p": privateKey.p, "q": privateKey.q}

    @staticmethod
    def __privateKeyToLibraryObj(
        privateKey: PrivateKey, publicKey: PaillierPublicKey
    ) -> PaillierPrivateKey:
        return PaillierPrivateKey(
            public_key=publicKey, p=privateKey["p"], q=privateKey["q"]
        )

from typing import Any, Tuple, Union
from PETWorks.homomorphic_encryption.Paillier import Paillier
from PETWorks.homomorphic_encryption.Communication import capturePackets
from PETWorks.homomorphic_encryption.Binary import listExternalFunction


def generateKey(keySize: int, library: str) -> Tuple[int, int]:
    if library == "phe":
        return Paillier(keySize).generateKey()
    else:
        raise KeyError("Unsupported Homomorphic Encryption Library")


def encrypt(
    value: int, keySize: int, library: str, publicKey: Any
) -> int:
    if library == "phe":
        return Paillier(keySize).encrypt(publicKey, value)
    else:
        raise KeyError("Unsupported Homomorphic Encryption Library")


def decrypt(
    encryptedValue: int,
    keySize: int,
    library: str,
    publicKey: Any,
    privateKey: Any,
) -> int:
    if library == "phe":
        return Paillier(keySize).decrypt(privateKey, publicKey, encryptedValue)
    else:
        raise KeyError("Unsupported Homomorphic Encryption Library")


def dataProcess(arg0, arg1, method, **keywordArgs):
    library = keywordArgs.pop("library", None)

    if method == "GenerateKey":
        publicKey, privateKey = generateKey(arg0, library, **keywordArgs)
        return {"Public Key": publicKey, "Private Key": privateKey}

    elif method == "Encrypt":
        value, keySize = arg0, arg1
        encryptedValue = encrypt(value, keySize, library, **keywordArgs)
        return {"Encrypted Value": encryptedValue}

    elif method == "Decrypt":
        encryptedValue, keySize = arg0, arg1
        decryptedValue = decrypt(arg0, arg1, library, **keywordArgs)
        return {"Decrypted Value": decryptedValue}

    elif method == "CapturePackets":
        interval, interface = arg0, arg1
        packets = capturePackets(interval, interface)
        return packets

    elif method == "FindExternalFunctions":
        executable = arg0
        externalFunctions = listExternalFunction(executable)
        return {"External Functions": externalFunctions}

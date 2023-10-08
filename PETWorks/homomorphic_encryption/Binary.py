from os import PathLike
import subprocess
from typing import List


def listExternalFunction(executable: PathLike) -> List[str]:
    try:
        result = subprocess.run(
            ["nm", "-D", executable], capture_output=True, check=True
        )

        if "no symbols" in result.stderr.decode():
            return []

        rawList = result.stdout.decode().splitlines()

        externalFunctions = [l.split()[-1] for l in rawList]

        return externalFunctions

    except subprocess.CalledProcessError as e:
        if "no dynamic symbol table" in e.stderr.decode():
            return []
        else:
            raise e

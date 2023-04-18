from collections import namedtuple
from os import PathLike
from typing import Iterator

from py4j.java_collections import JavaClass

Hierarchy = JavaClass

AnonymityConfig = namedtuple(
    "AnonymityConfig", ["suppressionLimit", "k", "level"]
)


def toFile(configs: Iterator[AnonymityConfig], out: PathLike) -> None:
    with open(out, "w") as outFile:
        convertor = (
            f"{suppressionLimit},{k},"
            + ",".join((str(value) for value in level))
            for suppressionLimit, k, level in configs
        )

        for line in convertor:
            outFile.write(line + "\n")
            outFile.flush()
            print(line)

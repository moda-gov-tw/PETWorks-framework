import re
from os import PathLike, listdir
from os.path import join
from typing import List

from py4j.java_gateway import JavaGateway

PATH_TO_ARX_LIBRARY = "arx/lib/libarx-3.9.0.jar"
gateway = JavaGateway.launch_gateway(
        classpath=PATH_TO_ARX_LIBRARY, die_on_exit=True)

Data = gateway.jvm.org.deidentifier.arx.Data
Charset = gateway.jvm.java.nio.charset.Charset
CSVHierarchyInput = gateway.jvm.org.deidentifier.arx.io.CSVHierarchyInput
Hierarchy = gateway.jvm.org.deidentifier.arx.AttributeType.Hierarchy


def loadDataFromCsv(path: PathLike, charset: Charset, delimiter: str) -> Data:
    return Data.create(path, charset, delimiter)


def loadDataHierarchy(
    path: PathLike, charset: Charset, delimiter: str
) -> dict[str, List[List[str]]]:

    hierarchies = {}
    for filename in listdir(path):
        result = re.match(".*hierarchy_(.*?).csv", filename)
        if result is None:
            continue

        attributeName = result.group(1)

        dataHierarchyFile = join(path, filename)
        hierarchy = CSVHierarchyInput(
            dataHierarchyFile, charset, delimiter
        ).getHierarchy()

        hierarchies[attributeName] = Hierarchy.create(hierarchy)

    return hierarchies

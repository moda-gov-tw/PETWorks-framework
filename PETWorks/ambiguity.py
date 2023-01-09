from typing import List

from PETWorks.arx import Data, gateway, loadDataFromCsv, loadDataHierarchy

StandardCharsets = gateway.jvm.java.nio.charset.StandardCharsets
Hierarchy = gateway.jvm.org.deidentifier.arx.AttributeType.Hierarchy


def _setDataHierarchies(
    data: Data, hierarchies: dict[str, List[List[str]]]
) -> None:
    for attributeName, hierarchy in hierarchies.items():
        data.getDefinition().setAttributeType(attributeName, hierarchy)


def _measureAmbiguity(original: Data, anonymized: Data) -> float:
    utility = (
        original.getHandle()
        .getStatistics()
        .getQualityStatistics(anonymized.getHandle())
    )

    ambiguity = utility.getAmbiguity().getValue()
    return ambiguity


def PETValidation(original, anonymized, _, dataHierarchy, **other):
    dataHierarchy = loadDataHierarchy(
        dataHierarchy, StandardCharsets.UTF_8, ";"
    )

    original = loadDataFromCsv(original, StandardCharsets.UTF_8, ";")
    anonymized = loadDataFromCsv(anonymized, StandardCharsets.UTF_8, ";")

    _setDataHierarchies(original, dataHierarchy)
    _setDataHierarchies(anonymized, dataHierarchy)

    ambiguity = _measureAmbiguity(original, anonymized)
    return {"ambiguity": ambiguity}

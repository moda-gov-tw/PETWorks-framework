from typing import List

from PETWorks.arx import Data, gateway, loadDataFromCsv

StandardCharsets = gateway.jvm.java.nio.charset.StandardCharsets
Hierarchy = gateway.jvm.org.deidentifier.arx.AttributeType.Hierarchy


def _setDataHierarchies(data: Data) -> None:
    for column in range(data.getHandle().getNumColumns()):
        data.getDefinition().setAttributeType(
                data.getHandle().getAttributeName(column), Hierarchy.create())


def _measureAECS(original: Data, anonymized: Data) -> float:
    utility = (
        original.getHandle()
        .getStatistics()
        .getQualityStatistics(anonymized.getHandle())
    )

    aecs = utility.getAverageClassSize().getValue()
    return aecs


def PETValidation(original, anonymized, _):

    original = loadDataFromCsv(original, StandardCharsets.UTF_8, ";")
    anonymized = loadDataFromCsv(anonymized, StandardCharsets.UTF_8, ";")

    _setDataHierarchies(original)
    _setDataHierarchies(anonymized)

    aecs = _measureAECS(original, anonymized)
    return {"AECS": aecs}

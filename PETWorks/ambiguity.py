from typing import Dict, List

from PETWorks.arx import (
    Data,
    loadDataFromCsv,
    loadDataHierarchy,
    JavaApi,
    UtilityMetrics,
)


def _setDataHierarchies(
    data: Data, hierarchies: Dict[str, List[List[str]]]
) -> None:
    for attributeName, hierarchy in hierarchies.items():
        data.getDefinition().setAttributeType(attributeName, hierarchy)


def _measureAmbiguity(original: Data, anonymized: Data) -> float:
    return UtilityMetrics.evaluate(original, anonymized).ambiguity


def PETValidation(original, anonymized, _, dataHierarchy, **other):
    javaApi = JavaApi()

    dataHierarchy = loadDataHierarchy(
        dataHierarchy, javaApi.StandardCharsets.UTF_8, ";", javaApi
    )

    original = loadDataFromCsv(
        original, javaApi.StandardCharsets.UTF_8, ";", javaApi
    )
    anonymized = loadDataFromCsv(
        anonymized, javaApi.StandardCharsets.UTF_8, ";", javaApi
    )

    _setDataHierarchies(original, dataHierarchy)
    _setDataHierarchies(anonymized, dataHierarchy)

    ambiguity = _measureAmbiguity(original, anonymized)
    return {"ambiguity": ambiguity}

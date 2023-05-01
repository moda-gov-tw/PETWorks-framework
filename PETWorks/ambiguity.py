from PETWorks.arx import (
    Data,
    loadDataFromCsv,
    loadDataHierarchy,
    setDataHierarchies,
    JavaApi,
    UtilityMetrics,
)


def _measureAmbiguity(original: Data, anonymized: Data) -> float:
    return UtilityMetrics.evaluate(original, anonymized).ambiguity


def PETValidation(original, anonymized, _, dataHierarchy, attributeTypes):
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

    setDataHierarchies(original, dataHierarchy, attributeTypes, javaApi)
    setDataHierarchies(anonymized, dataHierarchy, attributeTypes, javaApi)

    ambiguity = _measureAmbiguity(original, anonymized)
    return {"ambiguity": ambiguity}

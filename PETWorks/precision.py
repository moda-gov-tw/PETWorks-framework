from PETWorks.arx import (
    Data,
    JavaApi,
    UtilityMetrics,
    loadDataFromCsv,
    loadDataHierarchy,
    setDataHierarchies,
)


def _measurePrecision(original: Data, anonymized: Data) -> float:
    return UtilityMetrics.evaluate(original, anonymized).precision


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

    precision = _measurePrecision(original, anonymized)
    return {"precision": precision}

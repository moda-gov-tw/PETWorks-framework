from PETWorks.arx import (
    Data,
    loadDataFromCsv,
    JavaApi,
    UtilityMetrics,
    setDataHierarchies,
)


def _measureAECS(original: Data, anonymized: Data) -> float:
    return UtilityMetrics.evaluate(original, anonymized).aecs


def PETValidation(original, anonymized, _, attributeTypes):
    javaApi = JavaApi()
    original = loadDataFromCsv(
        original, javaApi.StandardCharsets.UTF_8, ";", javaApi
    )
    anonymized = loadDataFromCsv(
        anonymized, javaApi.StandardCharsets.UTF_8, ";", javaApi
    )

    setDataHierarchies(original, None, attributeTypes, javaApi)
    setDataHierarchies(anonymized, None, attributeTypes, javaApi)

    aecs = _measureAECS(original, anonymized)
    return {"AECS": aecs}

from PETWorks.arx import Data, loadDataFromCsv, loadDataHierarchy
from PETWorks.arx import JavaApi, UtilityMetrics, setDataHierarchies
from PETWorks.attributetypes import QUASI_IDENTIFIER


def _measureNonUniformEntropy(original: Data, anonymized: Data) -> float:
    return UtilityMetrics.evaluate(original, anonymized).nonUniformEntropy


def PETValidation(original, anonymized, _, dataHierarchy, **other):
    javaApi = JavaApi()

    dataHierarchy = loadDataHierarchy(
        dataHierarchy, javaApi.StandardCharsets.UTF_8, ";", javaApi
    )

    attributeTypes = {
        attributeName: QUASI_IDENTIFIER for attributeName in dataHierarchy
    }

    original = loadDataFromCsv(
        original, javaApi.StandardCharsets.UTF_8, ";", javaApi
    )
    anonymized = loadDataFromCsv(
        anonymized, javaApi.StandardCharsets.UTF_8, ";", javaApi
    )

    setDataHierarchies(original, dataHierarchy, attributeTypes, javaApi)
    setDataHierarchies(anonymized, dataHierarchy, attributeTypes, javaApi)

    nonUniformEntropy = _measureNonUniformEntropy(original, anonymized)
    return {"Non-Uniform Entropy": nonUniformEntropy}

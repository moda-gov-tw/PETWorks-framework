from typing import Dict

import pandas as pd

from PETWorks.deidentification.arx import (
    JavaApi,
    anonymizeData,
    getDataFrame,
    loadDataFromCsv,
    loadDataHierarchy,
    setDataHierarchies,
)


def measureLDiversity(
    anonymizedData: pd.DataFrame,
    attributeTypes: Dict[str, str],
) -> list[int]:
    qis = []
    sensitiveAttributes = []
    lValues = []

    for attribute, value in attributeTypes.items():
        if value == "quasi_identifier":
            qis.append(attribute)
        if value == "sensitive_attribute":
            sensitiveAttributes.append(attribute)

    for index in range(len(sensitiveAttributes)):
        columns = (
            qis
            + sensitiveAttributes[:index]
            + sensitiveAttributes[index + 1 :]
        )
        groups = anonymizedData.groupby(columns)

        sensitiveAttribute = sensitiveAttributes[index]
        lValues += [group[sensitiveAttribute].nunique() for _, group in groups]

    return lValues


def validateLDiversity(lValues: list[int], lLimit: int) -> bool:
    return all(value >= lLimit for value in lValues)


def PETValidation(
    original, anonymized, _, l, dataHierarchy=None, attributeTypes={}
):
    anonymizedDataFrame = pd.read_csv(anonymized, sep=";")

    lValues = measureLDiversity(anonymizedDataFrame, attributeTypes)
    fulfillLDiversity = validateLDiversity(lValues, l)

    return {"l": l, "fulfill l-diversity": fulfillLDiversity}


def PETAnonymization(
    originalData: str,
    maxSuppressionRate: float,
    l: int,
    dataHierarchy: str = None,
    attributeTypes: Dict[str, str] = {},
) -> pd.DataFrame:
    javaApi = JavaApi()
    originalData = loadDataFromCsv(
        originalData, javaApi.StandardCharsets.UTF_8, ";", javaApi
    )

    dataHierarchy = loadDataHierarchy(
        dataHierarchy, javaApi.StandardCharsets.UTF_8, ";", javaApi
    )

    setDataHierarchies(
        originalData, dataHierarchy, attributeTypes, javaApi, True
    )

    privacyModels = []
    for attributeName, attributeType in attributeTypes.items():
        if attributeType == "sensitive_attribute":
            privacyModels.append(javaApi.DistinctLDiversity(attributeName, l))

    anonymizedResult = anonymizeData(
        originalData,
        privacyModels,
        javaApi,
        None,
        float(maxSuppressionRate),
    )
    anonymizedData = javaApi.Data.create(
        anonymizedResult.getOutput(True).iterator()
    )
    return getDataFrame(anonymizedData)

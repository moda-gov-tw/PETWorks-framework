import pandas as pd

from PETWorks.arx import (
    loadDataHierarchyNatively,
    getAttributeNameByType,
    loadDataFromCsv,
    loadDataHierarchy,
    setDataHierarchies,
    JavaApi,
    getDataFrame,
    anonymizeData,
)
from PETWorks.attributetypes import SENSITIVE_ATTRIBUTE, QUASI_IDENTIFIER
import numpy as np
from math import fabs
from typing import Dict


def _computeHierarchicalDistance(
    dataDistribution: dict[str, float],
    groupDistribution: dict[str, float],
    sensitiveHierarchy: np.chararray,
) -> float:
    hierarchyWidth, hierarchyHeight = sensitiveHierarchy.shape

    extraArray = np.zeros((hierarchyWidth, hierarchyHeight), dtype=np.float32)
    costArray = np.zeros((hierarchyWidth, hierarchyHeight), dtype=np.float32)

    # loop through hierarchy height from 0
    for currentHeight in range(hierarchyHeight):
        for rowIndex in range(hierarchyWidth):
            # if leaf
            if currentHeight == 0:
                costArray[rowIndex, currentHeight] = 0.0

                value = sensitiveHierarchy[rowIndex, 0]
                extra = groupDistribution.get(value, 0) - dataDistribution.get(
                    value, 0
                )
                extraArray[rowIndex, currentHeight] = extra
                continue

            # if not leaf
            uniqueValues = np.unique(sensitiveHierarchy[:, currentHeight])
            for value in uniqueValues:
                rowIndicesWithMatchedValue = np.where(
                    sensitiveHierarchy[:, currentHeight] == value
                )[0]
                extraSubset = extraArray[
                    rowIndicesWithMatchedValue, currentHeight - 1
                ]
                maskForPositiveExtras = extraSubset > 0
                maskForNegativeExtras = extraSubset < 0

                positiveExtrasSum = np.sum(extraSubset[maskForPositiveExtras])
                negativeExtrasSum = -1 * np.sum(
                    extraSubset[maskForNegativeExtras]
                )

                extraArray[rowIndicesWithMatchedValue[0], currentHeight] = (
                    positiveExtrasSum - negativeExtrasSum
                )

                cost = float(currentHeight) * min(
                    positiveExtrasSum, negativeExtrasSum
                )
                cost /= hierarchyHeight - 1
                costArray[rowIndicesWithMatchedValue[0], currentHeight] = cost

    return float(np.sum(costArray))


def _computeEqualDistance(
    dataDistribution: dict[str, float],
    groupDistribution: dict[str, float],
) -> float:
    extraList = [
        float(groupDistribution.get(value, 0) - dataDistribution.get(value, 0))
        for value in dataDistribution.keys()
    ]

    distance = 0.0
    for extra in extraList:
        distance += fabs(extra)
    distance /= 2

    return distance


def _computeNumericalDistance(
    dataDistribution: dict[str, float],
    groupDistribution: dict[str, float],
    sensitiveData: pd.Series,
) -> float:
    sensitiveData = sensitiveData.sort_values(
        ascending=True, key=lambda x: pd.to_numeric(x)
    )

    valueList = sensitiveData.unique().tolist()

    extraList = [
        float(groupDistribution.get(value, 0) - dataDistribution.get(value, 0))
        for value in valueList
    ]

    distance = 0.0
    sum = 0.0
    for extra in extraList:
        sum += extra
        distance += fabs(sum)
    distance /= len(extraList) - 1

    return distance


def measureTCloseness(
    anonymizedData: pd.DataFrame,
    sensitiveAttributeName: str,
    qiNames: list[str],
    sensitiveHierarchy: np.chararray,
) -> float:
    dataDistribution = dict(
        anonymizedData[sensitiveAttributeName].value_counts()
        / len(anonymizedData)
    )
    anonymizedGroups = anonymizedData.groupby(qiNames)

    maxDistance = float("-inf")
    for _, group in anonymizedGroups:
        groupDistribution = dict(
            group[sensitiveAttributeName].value_counts() / len(group)
        )
        isNumeral = False
        try:
            float(anonymizedData[sensitiveAttributeName].iloc[0])
            isNumeral = True
        except ValueError:
            pass

        if isNumeral:
            distance = _computeNumericalDistance(
                dataDistribution,
                groupDistribution,
                anonymizedData[sensitiveAttributeName],
            )
        elif sensitiveHierarchy is not None:
            distance = _computeHierarchicalDistance(
                dataDistribution, groupDistribution, sensitiveHierarchy
            )
        else:
            distance = _computeEqualDistance(
                dataDistribution, groupDistribution
            )

        if distance > maxDistance:
            maxDistance = distance

    return maxDistance


def _validateTCloseness(tFromData: float, tLimit: float) -> bool:
    return tFromData < tLimit


def PETValidation(
    original, anonymized, _, dataHierarchy, attributeTypes, tLimit, **other
):
    tLimit = float(tLimit)

    dataHierarchy = loadDataHierarchyNatively(dataHierarchy, ";")
    anonymizedData = pd.read_csv(anonymized, sep=";", skipinitialspace=True)

    qiNames = getAttributeNameByType(attributeTypes, QUASI_IDENTIFIER)
    sensitiveAttributes = getAttributeNameByType(
        attributeTypes, SENSITIVE_ATTRIBUTE
    )

    tList = [
        measureTCloseness(
            anonymizedData,
            sensitiveAttribute,
            qiNames,
            dataHierarchy.get(sensitiveAttribute, None),
        )
        for sensitiveAttribute in sensitiveAttributes
    ]

    fulfillTCloseness = all(_validateTCloseness(t, tLimit) for t in tList)

    return {"t": tLimit, "fulfill t-closeness": fulfillTCloseness}


def PETAnonymization(
    originalData: str,
    dataHierarchy: str,
    attributeTypes: Dict[str, str],
    maxSuppressionRate: float,
    t: float,
) -> pd.DataFrame:
    javaApi = JavaApi()
    originalDataFrame = pd.read_csv(
        originalData, sep=";", skipinitialspace=True
    )

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
        if attributeType == SENSITIVE_ATTRIBUTE:
            isNumerical = True
            try:
                float(originalDataFrame[attributeName].iloc[0])
            except ValueError:
                isNumerical = False

            if isNumerical:
                tClosenessModel = javaApi.OrderedDistanceTCloseness(
                    attributeName, float(t)
                )
            else:
                tClosenessModel = javaApi.HierarchicalDistanceTCloseness(
                    attributeName, float(t), dataHierarchy.get(attributeName)
                )

            privacyModels.append(tClosenessModel)

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

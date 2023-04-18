import pandas as pd

from PETWorks.arx import (
    loadDataHierarchyNatively,
    getAttributeNameByType,
)
from PETWorks.attributetypes import SENSITIVE_ATTRIBUTE, QUASI_IDENTIFIER
import numpy as np
import pandas as pd
from math import fabs


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


def _computeNumericalDistance(
    dataDistribution: dict[str, float],
    groupDistribution: dict[str, float],
    originalSensitiveData: pd.Series,
) -> float:
    originalSensitiveData = originalSensitiveData.sort_values(
        ascending=True, key=lambda x: pd.to_numeric(x, errors="coerce")
    )
    numRows = len(originalSensitiveData)

    valueList = sorted(
        [originalSensitiveData[index] for index in range(numRows)],
        key=lambda x: pd.to_numeric(x),
    )

    extraList = [
        float(groupDistribution.get(value, 0) - dataDistribution.get(value, 0))
        for value in valueList
    ]

    distance = 0.0
    for index in range(numRows):
        sum = 0
        for subIndex in range(index):
            sum += extraList[subIndex]
        distance += fabs(sum)
    distance /= numRows - 1

    return distance


def _computeTCloseness(
    originalData: pd.DataFrame,
    anonymizedData: pd.DataFrame,
    sensitiveAttributeName: str,
    qiNames: list[str],
    sensitiveHierarchy: np.chararray,
) -> float:
    dataDistribution = dict(
        originalData[sensitiveAttributeName].value_counts() * 0
        + 1 / originalData[sensitiveAttributeName].nunique()
    )
    anonymizedGroups = anonymizedData.groupby(qiNames)

    maxHierarchicalDistance = float("-inf")
    for _, group in anonymizedGroups:
        groupDistribution = dict(
            group[sensitiveAttributeName].value_counts() * 0 + 1 / len(group)
        )
        if sensitiveHierarchy is not None:
            distance = _computeHierarchicalDistance(
                dataDistribution, groupDistribution, sensitiveHierarchy
            )
        else:
            distance = _computeNumericalDistance(
                dataDistribution,
                groupDistribution,
                originalData[sensitiveAttributeName],
            )

        if distance > maxHierarchicalDistance:
            maxHierarchicalDistance = distance

    return maxHierarchicalDistance


def measureTCloseness(
    originalData: pd.DataFrame,
    anonymizedData: pd.DataFrame,
    sensitiveAttributeName: str,
    qiNames: list[str],
    sensitiveHierarchy: np.chararray,
) -> float:
    isNumerical = True
    try:
        float(sensitiveHierarchy[0, 0])
    except ValueError:
        isNumerical = False

    if isNumerical:
        return _computeTCloseness(
            originalData, anonymizedData, sensitiveAttributeName, qiNames, None
        )

    return _computeTCloseness(
        originalData,
        anonymizedData,
        sensitiveAttributeName,
        qiNames,
        sensitiveHierarchy,
    )


def _validateTCloseness(tFromData: float, tLimit: float) -> bool:
    return tFromData < tLimit


def PETValidation(
    original, anonymized, _, dataHierarchy, attributeTypes, tLimit, **other
):
    tLimit = float(tLimit)

    dataHierarchy = loadDataHierarchyNatively(dataHierarchy, ";")
    originalData = pd.read_csv(original, sep=";", skipinitialspace=True)
    anonymizedData = pd.read_csv(anonymized, sep=";", skipinitialspace=True)

    qiNames = getAttributeNameByType(attributeTypes, QUASI_IDENTIFIER)
    sensitiveAttributes = getAttributeNameByType(
        attributeTypes, SENSITIVE_ATTRIBUTE
    )

    tList = [
        measureTCloseness(
            originalData,
            anonymizedData,
            sensitiveAttribute,
            qiNames,
            dataHierarchy,
        )
        for sensitiveAttribute in sensitiveAttributes
    ]

    fullfilTCloseness = all(_validateTCloseness(t, tLimit) for t in tList)

    return {"t": tLimit, "fullfil t-closeness": fullfilTCloseness}

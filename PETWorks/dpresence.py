import pandas as pd
from PETWorks.arx import gateway, loadDataFromCsv, loadDataHierarchy
from PETWorks.arx import setDataHierarchies, getDataFrame
from PETWorks.arx import getAnonymousLevels, applyAnonymousLevels
from PETWorks.attributetypes import QUASI_IDENTIFIER
from typing import Dict

StandardCharsets = gateway.jvm.java.nio.charset.StandardCharsets


def measureDPresence(
    populationTable: pd.DataFrame,
    sampleTable: pd.DataFrame,
    attributeTypes: Dict[str, str],
) -> list[float]:
    qiNames = [
        qi for qi, value in attributeTypes.items() if value == QUASI_IDENTIFIER
    ]
    populationGroups = populationTable.groupby(qiNames).groups
    sampleGroups = sampleTable.groupby(qiNames).groups

    intersectionGroups = set(populationGroups.keys()).intersection(
        set(sampleGroups.keys())
    )

    rawValues = [
        (
            float(len(sampleGroups[intersectGroup])),
            float(len(populationGroups[intersectGroup])),
        )
        for intersectGroup in intersectionGroups
    ]

    deltaValues = [
        count / pCount for count, pCount in rawValues if pCount != 0
    ]

    return deltaValues


def validateDPresence(
    deltaValues: list[float], dMin: float, dMax: float
) -> bool:
    return all(dMax >= value >= dMin for value in deltaValues)


def PETValidation(
    original, sample, _, dataHierarchy, attributeTypes, dMin, dMax
):
    dataHierarchy = loadDataHierarchy(
        dataHierarchy, StandardCharsets.UTF_8, ";"
    )
    originalPopulationData = loadDataFromCsv(
        original, StandardCharsets.UTF_8, ";"
    )

    anonymizedSampleData = loadDataFromCsv(sample, StandardCharsets.UTF_8, ";")

    setDataHierarchies(originalPopulationData, dataHierarchy, attributeTypes)
    setDataHierarchies(anonymizedSampleData, dataHierarchy, attributeTypes)

    anonymousLevels = getAnonymousLevels(anonymizedSampleData, dataHierarchy)
    anonymizedPopulationDataHandle = applyAnonymousLevels(
        originalPopulationData, anonymousLevels
    )

    populationDataFrame = getDataFrame(anonymizedPopulationDataHandle)
    sampleDataFrame = getDataFrame(anonymizedSampleData.getHandle())

    deltaValues = measureDPresence(
        populationDataFrame, sampleDataFrame, attributeTypes
    )
    fulfillDPresence = validateDPresence(
        deltaValues, float(dMin), float(dMax)
    )

    return {"dMin": dMin, "dMax": dMax, "d-presence": fulfillDPresence}

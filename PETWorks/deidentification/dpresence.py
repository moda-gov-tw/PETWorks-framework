from typing import Dict

import pandas as pd

from PETWorks.deidentification.arx import (
    JavaApi,
    applyAnonymousLevels,
    getAnonymousLevels,
    getDataFrame,
    loadDataFromCsv,
    loadDataHierarchy,
    setDataHierarchies,
    anonymizeData,
)


def measureDPresence(
    populationTable: pd.DataFrame,
    sampleTable: pd.DataFrame,
    attributeTypes: Dict[str, str],
) -> list[float]:
    qiNames = [
        qi
        for qi, value in attributeTypes.items()
        if value == "quasi_identifier"
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
    original, sample, _, dMin, dMax, dataHierarchy=None, attributeTypes={}
):
    javaApi = JavaApi()
    dataHierarchy = loadDataHierarchy(
        dataHierarchy, javaApi.StandardCharsets.UTF_8, ";", javaApi
    )
    originalPopulationData = loadDataFromCsv(
        original, javaApi.StandardCharsets.UTF_8, ";", javaApi
    )
    anonymizedSampleData = loadDataFromCsv(
        sample, javaApi.StandardCharsets.UTF_8, ";", javaApi
    )

    setDataHierarchies(
        originalPopulationData, dataHierarchy, attributeTypes, javaApi
    )
    setDataHierarchies(
        anonymizedSampleData, dataHierarchy, attributeTypes, javaApi
    )

    anonymousLevels = getAnonymousLevels(anonymizedSampleData, dataHierarchy)
    anonymizedPopulation = applyAnonymousLevels(
        originalPopulationData,
        anonymousLevels,
        dataHierarchy,
        attributeTypes,
        javaApi,
    )

    populationDataFrame = getDataFrame(anonymizedPopulation)
    sampleDataFrame = getDataFrame(anonymizedSampleData)

    deltaValues = measureDPresence(
        populationDataFrame, sampleDataFrame, attributeTypes
    )
    fulfillDPresence = validateDPresence(deltaValues, float(dMin), float(dMax))

    return {"dMin": dMin, "dMax": dMax, "d-presence": fulfillDPresence}


def PETAnonymization(
    originalData: str,
    maxSuppressionRate: float,
    dMin: float,
    dMax: float,
    subsetData: str,
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

    subsetData = loadDataFromCsv(
        subsetData, javaApi.StandardCharsets.UTF_8, ";", javaApi
    )

    setDataHierarchies(originalData, dataHierarchy, attributeTypes, javaApi)
    dataSubset = javaApi.DataSubset.create(originalData, subsetData)

    anonymizedResult = anonymizeData(
        originalData,
        [javaApi.DPresence(dMin, dMax, dataSubset)],
        javaApi,
        None,
        float(maxSuppressionRate),
    )
    anonymizedData = javaApi.Data.create(
        anonymizedResult.getOutput(True).iterator()
    )
    return getDataFrame(anonymizedData)

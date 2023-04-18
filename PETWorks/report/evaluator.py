import numpy as np
from os import PathLike
from typing import Dict, Generator, Iterator, Tuple
from dataclasses import dataclass
from collections import namedtuple
from PETWorks.report import AnonymityConfig
from PETWorks.arx import (
    Data,
    getDataFrame,
    UtilityMetrics,
    convertJavaListToList,
    setDataHierarchies,
    anonymizeData,
    JavaApi,
    loadDataHierarchy,
    setDataHierarchies,
    getAttributeNameByType,
)
from PETWorks.attributetypes import QUASI_IDENTIFIER, SENSITIVE_ATTRIBUTE


import pandas as pd

from multiprocessing.pool import Pool
from multiprocessing import cpu_count

from PETWorks.tcloseness import (
    measureTCloseness,
)
from PETWorks.profitability import _measureProfitabilityPayoffNoAttack

from py4j.java_gateway import Py4JJavaError


@dataclass
class Metrics:
    ambiguity: float
    precision: float
    nonUniformEntropy: float
    aecs: float
    k: int
    d: float
    t: float
    profitability: int

    @staticmethod
    def __evaluateDPresence(
        originalData: pd.DataFrame,
        anonymizedSubset: pd.DataFrame,
        attributeTypes: Dict[str, str],
    ) -> float:
        qiNames = [
            attributeName
            for attributeName, attributeType in attributeTypes.items()
            if attributeType == QUASI_IDENTIFIER
        ]
        qiIndices = [
            originalData.columns.get_loc(qiName) for qiName in qiNames
        ]

        groupedData = originalData.groupby(qiNames)
        groupedSubset = anonymizedSubset.groupby(qiNames)

        deltaValues = []
        for _, subsetGroup in groupedSubset:
            count = 0
            pcount = 0

            subsetGroupList = subsetGroup.values.tolist()
            count = len(subsetGroupList)

            for _, dataGroup in groupedData:
                dataGroupList = dataGroup.values.tolist()

                pcount = len(dataGroup)
                for index in qiIndices:
                    if subsetGroupList[0][index] != dataGroupList[0][index]:
                        pcount = 0

                if pcount > 0:
                    deltaValues.append(count / pcount)
                else:
                    deltaValues.append(0)

        return 1 - max(deltaValues)

    @staticmethod
    def evaluate(
        originalData: Data,
        anonymizedData: Data,
        k: int,
        attributeTypes: Dict[str, str],
        dataHierarchy: Dict[str, np.chararray],
    ) -> "Metrics":
        utility = UtilityMetrics.evaluate(originalData, anonymizedData)

        originalDataFrame = getDataFrame(originalData)
        anonymizedDataFrame = getDataFrame(anonymizedData)

        sensitiveAttributes = getAttributeNameByType(
            attributeTypes, SENSITIVE_ATTRIBUTE
        )
        qiNames = list(
            getAttributeNameByType(attributeTypes, QUASI_IDENTIFIER)
        )

        d = Metrics.__evaluateDPresence(
            originalDataFrame, anonymizedDataFrame, attributeTypes
        )

        t = 1 - max(
            [
                measureTCloseness(
                    originalDataFrame,
                    anonymizedDataFrame,
                    sensitive,
                    qiNames,
                    dataHierarchy[sensitive],
                )
                for sensitive in sensitiveAttributes
            ],
            default=1,
        )

        profitability = _measureProfitabilityPayoffNoAttack(
            anonymizedDataFrame, qiNames, 4, 200000 / len(anonymizedDataFrame)
        )

        return Metrics(
            ambiguity=utility.ambiguity,
            precision=utility.precision,
            nonUniformEntropy=utility.nonUniformEntropy,
            aecs=utility.aecs,
            k=k,
            d=d,
            t=t,
            profitability=profitability,
        )


__javaApi = None


def __setupJavaGateway():
    global __javaApi
    __javaApi = JavaApi()


def __filterWithKAnonymity(args: Tuple):
    pathToOriginalData, pathToHierarchy, suppressRate, k = args

    originalData = __javaApi.Data.create(
        pathToOriginalData, __javaApi.StandardCharsets.UTF_8, ";"
    )

    hierarchies = loadDataHierarchy(
        pathToHierarchy, __javaApi.StandardCharsets.UTF_8, ";", __javaApi
    )

    attributeTypes = {key: QUASI_IDENTIFIER for key, _ in hierarchies.items()}

    setDataHierarchies(originalData, hierarchies, attributeTypes, __javaApi)

    privacyModels = [__javaApi.KAnonymity(k)]

    try:
        anonymizedResult = anonymizeData(
            originalData, privacyModels, __javaApi, None, suppressRate
        )
    except Py4JJavaError:
        return

    if not anonymizedResult:
        return None

    anonymizedSolutions = anonymizedResult.getLattice().getLevels()

    levels = set()
    for level in anonymizedSolutions:
        for node in level:
            if str(node.getAnonymity()) != "ANONYMOUS":
                continue

            try:
                anonymizingLevel = convertJavaListToList(
                    node.getTransformation()
                )
            except Py4JJavaError:
                pass

            levels.add(anonymizingLevel)

    return (suppressRate, k, levels)


Combination = namedtuple("Combination", "suppressionRate k")


def filterWithKAnonymityParallelly(
    originalData: PathLike,
    dataHierarchy: PathLike,
    configs: Iterator[AnonymityConfig],
    numOfProcess: int = (cpu_count() - 1),
) -> Generator[Tuple, None, None]:
    pool = Pool(numOfProcess, __setupJavaGateway)

    argumentSets = (
        (originalData, dataHierarchy, config.suppressionLimit, config.k)
        for config in configs
    )

    asyncResults = pool.imap(
        __filterWithKAnonymity, argumentSets, chunksize=30
    )

    fullConfigs = (
        AnonymityConfig(suppressionLimit, k, level)
        for suppressionLimit, k, levels in asyncResults
        for level in levels
    )

    yield from fullConfigs

from dataclasses import asdict
import itertools
import json
import math
from multiprocessing import Pool
from os import PathLike
import os
from typing import Callable, Dict, Generator, List, Tuple, TypeVar

import numpy as np
import pandas as pd
from PETWorks.arx import (
    createJavaGateway,
    JavaApi,
    loadDataFromCsv,
    loadDataHierarchy,
    loadDataHierarchyNatively,
    applyAnonymousLevels,
    setDataHierarchies,
    getDataFrame,
)
from PETWorks.report import toFile
from PETWorks.report.iterator import generateConfigs
from PETWorks.report.evaluator import filterWithKAnonymityParallelly, Metrics
from PETWorks.report.validator import isAnalysiable

T = TypeVar("T")


def __sample(
    data: List[T], count: int, dataSize: int = None
) -> Generator[T, None, None]:

    if dataSize is None:
        dataSize = len(data)

    step = (dataSize - 1) // (count - 1)

    steppedData = (
        element for index, element in enumerate(data) if index % step == 0
    )

    yield from itertools.islice(steppedData, count)


__javaApi = None


def __setJavaApi():
    global __javaApi
    gateway = createJavaGateway()
    __javaApi = JavaApi(gateway)


__analysisFunction = None


def __findQualifiedConfigsImplement(argumentSets: List):
    (
        originalData,
        dataHierarchy,
        attributeTypes,
        bias,
        k,
        transformation,
    ) = argumentSets

    utf8 = __javaApi.StandardCharsets.UTF_8
    dataHierarchyFolder = dataHierarchy
    originalDataFile = originalData

    originalData = loadDataFromCsv(originalDataFile, utf8, ";", __javaApi)
    dataHierarchy = loadDataHierarchy(
        dataHierarchyFolder, __javaApi.StandardCharsets.UTF_8, ";", __javaApi
    )

    setDataHierarchies(originalData, dataHierarchy, attributeTypes, __javaApi)

    anonymizedData = applyAnonymousLevels(
        originalData, transformation, dataHierarchy, attributeTypes, __javaApi
    )

    originalDataFrame = getDataFrame(originalData)
    anonymizedDataFrame = getDataFrame(anonymizedData)
    if isAnalysiable(
        originalDataFrame, anonymizedDataFrame, __analysisFunction, bias
    ):
        # Make a copy of the original data for ARX API to evaluate metrics.
        originalData = loadDataFromCsv(
            originalDataFile, utf8, ";", __javaApi
        )
        setDataHierarchies(
            originalData, dataHierarchy, attributeTypes, __javaApi
        )

        nativeDataHierarchy = loadDataHierarchyNatively(
            dataHierarchyFolder, ";"
        )

        metrics = Metrics.evaluate(
            originalData,
            anonymizedData,
            k,
            attributeTypes,
            nativeDataHierarchy,
        )

        return asdict(metrics)

    return {}


def __calculateFiveThresholds(values: List[float]) -> Tuple[float]:
    series = pd.Series(values)

    middleAvg = series.mean()

    firstAvg = series.loc[lambda v: v <= middleAvg].astype(float).mean()
    thirdAvg = series.loc[lambda v: v >= middleAvg].astype(float).mean()

    firstThreshold = series.loc[lambda v: v <= firstAvg].astype(float).mean()
    secondThreshold = series.loc[
        lambda v: np.logical_and(v >= firstAvg, v <= middleAvg)
    ].astype(float).mean()
    thirdThreshold = series.loc[
        lambda v: np.logical_and(v >= middleAvg, v <= thirdAvg)
    ].astype(float).mean()
    fourthThreshold = series.loc[lambda v: v >= thirdAvg].astype(float).mean()

    if math.isnan(secondThreshold):
        secondThreshold = firstThreshold
    if math.isnan(thirdThreshold):
        thirdThreshold = secondThreshold
    if math.isnan(fourthThreshold):
        fourthThreshold = thirdThreshold

    return (firstThreshold, secondThreshold, thirdThreshold, fourthThreshold)


def generateAnonymityConfigs(
    originalData: PathLike,
    dataHierarchy: PathLike,
    output: PathLike,
    firstSampleCount: int,
    secondSampleCount: int,
) -> None:
    # Generate anonymity configs
    total, configs = generateConfigs(originalData)

    # First sampling
    configs = list(__sample(configs, firstSampleCount, dataSize=total))
    print(f"Configs left after first sampling : {len(configs)}")

    # Filter by ARX API
    configs = list(
        filterWithKAnonymityParallelly(originalData, dataHierarchy, configs)
    )

    print(f"Configs left after filtering : {len(configs)}")

    # Second Sampling
    configs = list(__sample(configs, secondSampleCount))

    print(f"Configs left after second sampling : {len(configs)}")

    # Write combination to the file
    toFile(configs, output)


def findQualifiedAnonymityConfigs(
    originalData: PathLike,
    dataHierarchy: PathLike,
    anonymityConfigs: PathLike,
    attributeTypes: Dict[str, str],
    analysisFunction: Callable[[pd.DataFrame], float],
    bias: float,
    output: PathLike,
    numOfProcess=(os.cpu_count() - 1),
) -> None:
    global __analysisFunction
    __analysisFunction = analysisFunction

    with open(anonymityConfigs, "r") as inFile:
        rawParameters = (
            line.strip().split(",") for line in inFile.readlines()
        )

        argumentSets = [
            (
                originalData,
                dataHierarchy,
                attributeTypes,
                bias,
                parameter[1],
                [int(val) for val in parameter[2:]],
            )
            for parameter in rawParameters
        ]

    with open(output, "w") as outFile:
        pool = Pool(numOfProcess, initializer=__setJavaApi)
        asyncResults = pool.imap(
            __findQualifiedConfigsImplement, argumentSets, chunksize=30
        )

        for index, result in enumerate(asyncResults):
            if result:
                representation = json.dumps(result, indent=4)

                print(f"{index} - {representation}")
                outFile.write(representation + "\n")

            else:
                print(
                    f"{index} - No result "
                    "since the analysis target is not analyzable."
                )
                outFile.write(
                    "No result since the analysis target is not analyzable.\n"
                )

            outFile.flush()


def calculateThresholds(
    metricsMeasures: PathLike,
    output: PathLike,
) -> Dict[str, Tuple[float]]:
    effectiveResults = {
        "k": [],
        "d": [],
        "t": [],
        "profitability": [],
        "ambiguity": [],
        "precision": [],
        "nonUniformEntropy": [],
        "aecs": [],
    }

    with open(metricsMeasures, "r") as file:
        totalCount = 0
        while True:
            totalCount += 1
            line = file.readline()

            if line == "":
                break

            if line.startswith("{"):
                buffer = ""

                while not line.startswith("}"):
                    buffer += line
                    line = file.readline()

                buffer += line
                jsonObj = json.loads(buffer)

                for metric, values in effectiveResults.items():
                    values.append(jsonObj[metric])

    effectiveResults["k"] = [int(element) for element in effectiveResults["k"]]

    thresholds = {}
    for metric, values in effectiveResults.items():
        thresholds[metric] = __calculateFiveThresholds(values)

    with open(output, "w") as outFile:
        outFile.write(json.dumps(thresholds, indent=4))

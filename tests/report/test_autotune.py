from collections import namedtuple
import json
import pandas as pd
import pytest

import PETWorks.autoturn as at
from PETWorks.attributetypes import QUASI_IDENTIFIER, SENSITIVE_ATTRIBUTE

TestSet = namedtuple(
    "TestSet", ["originalData", "dataHierarchy", "attributeTypes"]
)


@pytest.fixture(scope="module")
def simpleTestSet():
    return TestSet(
        originalData="data/adult10.csv",
        dataHierarchy="data/adult_hierarchy",
        attributeTypes={
            "sex": QUASI_IDENTIFIER,
            "age": QUASI_IDENTIFIER,
            "race": QUASI_IDENTIFIER,
            "marital-status": QUASI_IDENTIFIER,
            "education": QUASI_IDENTIFIER,
            "native-country": QUASI_IDENTIFIER,
            "workclass": SENSITIVE_ATTRIBUTE,
            "occupation": SENSITIVE_ATTRIBUTE,
            "salary-class": SENSITIVE_ATTRIBUTE,
        },
    )


def testGenerateAnonymityConfigs(tmp_path, simpleTestSet):
    originalData, dataHierarchy, _ = simpleTestSet
    output = tmp_path / "combinations.csv"

    at.generateAnonymityConfigs(originalData, dataHierarchy, output, 5, 3)

    parameterSets = output.read_text().split("\n")[:-1]
    assert len(parameterSets) == 3
    assert len(parameterSets[0].split(",")) == 11


def testFindQualifiedAnonymityConfigs(tmp_path, simpleTestSet):
    originalData, dataHierarchy, attributeTypes = simpleTestSet
    parameterSetFile = "tests/report/combination.csv"
    output = tmp_path / "result.txt"
    bias = 3

    def analysisFunction(data: pd.DataFrame) -> float:
        return data["age"].astype(float).max()

    at.findQualifiedAnonymityConfigs(
        originalData,
        dataHierarchy,
        parameterSetFile,
        attributeTypes,
        analysisFunction,
        bias,
        output,
        numOfProcess=1,
    )

    results = output.read_text().split("\n")[:-1]
    assert len([line for line in results if line.startswith("No result")]) == 2


def testCalculateThresholds(tmp_path):
    resultFile = "tests/report/result.txt"
    output = tmp_path / "thresholds.json"

    at.calculateThresholds(resultFile, output)

    thresholds = json.loads(output.read_text())
    assert len(thresholds) == 8
    assert thresholds["k"] == [0, 50, 50, 100]
    assert thresholds["d"] == [0, 0.5, 0.5, 1]

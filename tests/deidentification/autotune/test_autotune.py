from collections import namedtuple
import json
import pandas as pd
import pytest

import PETWorks.deidentification.autotune.autotune as at

TestSet = namedtuple(
    "TestSet", ["originalData", "dataHierarchy", "attributeTypes"]
)


@pytest.fixture(scope="module")
def simpleTestSet():
    return TestSet(
        originalData="datasets/adult/adult10.csv",
        dataHierarchy="datasets/adult/adult_hierarchy",
        attributeTypes={
            "sex": "quasi_identifier",
            "age": "quasi_identifier",
            "race": "quasi_identifier",
            "marital-status": "quasi_identifier",
            "education": "quasi_identifier",
            "native-country": "quasi_identifier",
            "workclass": "sensitive_attribute",
            "occupation": "sensitive_attribute",
            "salary-class": "sensitive_attribute",
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
    assert len(thresholds) == 9
    assert thresholds["k"] == [0, 50, 50, 100]
    assert thresholds["d"] == [0, 0.5, 0.5, 1]
    assert thresholds["l"] == [1, 25, 50, 100]

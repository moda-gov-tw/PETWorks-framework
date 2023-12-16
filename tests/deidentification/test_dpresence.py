from PETWorks.deidentification.dpresence import (
    measureDPresence,
    validateDPresence,
    PETValidation,
    PETAnonymization,
)

from typing import Dict
import pytest
import pandas as pd

ORIGINAL_POPULATION_DATA_PATH = "data/presence/presence.csv"
ANONYMIZED_POPULATION_DATA_PATH = "data/presence/presence_transformed.csv"
ANONYMIZED_SAMPLE_DATA_PATH = "data/presence/presence_anonymized.csv"
DATA_HIERARCHY_PATH = "data/presence/presence_hierarchy"


@pytest.fixture(scope="module")
def attributeTypesForPresence() -> Dict[str, str]:
    attributeTypes = {
        "identifier": "identifier",
        "name": "identifier",
        "zip": "quasi_identifier",
        "age": "quasi_identifier",
        "nationality": "quasi_identifier",
        "sen": "sensitive_attribute",
    }
    return attributeTypes


def testMeasureDPresence(attributeTypesForPresence):
    populationDataFrameForPresence = pd.read_csv(
        ANONYMIZED_POPULATION_DATA_PATH, skipinitialspace=True, sep=r";"
    )
    sampleDataFrameForPresence = pd.read_csv(
        ANONYMIZED_SAMPLE_DATA_PATH, skipinitialspace=True, sep=r";"
    )
    populationDataFrameForPresence.columns = (
        populationDataFrameForPresence.columns.str.strip()
    )
    sampleDataFrameForPresence.columns = (
        sampleDataFrameForPresence.columns.str.strip()
    )
    deltaValues = measureDPresence(
        populationDataFrameForPresence,
        sampleDataFrameForPresence,
        attributeTypesForPresence,
    )

    assert set(deltaValues) == {1 / 2, 2 / 3}


def testValidateDPresenceFulfilled():
    dMin = 1 / 2
    dMax = 2 / 3
    dValues = [0.51, 0.56666, 0.6666666666666666]
    assert validateDPresence(dValues, dMin, dMax) is True


def testValidateDPresenceNotFulfilled():
    dMin = 1 / 2
    dMax = 2 / 3
    dValues = [0.2, 0.7]
    assert validateDPresence(dValues, dMin, dMax) is False


def testPETValidationFulfilled(attributeTypesForPresence):
    result = PETValidation(
        ORIGINAL_POPULATION_DATA_PATH,
        ANONYMIZED_SAMPLE_DATA_PATH,
        "d-presence",
        dataHierarchy=DATA_HIERARCHY_PATH,
        attributeTypes=attributeTypesForPresence,
        dMin=1 / 2,
        dMax=2 / 3,
    )
    assert result["dMin"] == 1 / 2
    assert result["dMax"] == 2 / 3
    assert result["d-presence"] is True


def testPETValidationNotFulfilled(attributeTypesForPresence):
    result = PETValidation(
        ORIGINAL_POPULATION_DATA_PATH,
        ANONYMIZED_SAMPLE_DATA_PATH,
        "d-presence",
        dataHierarchy=DATA_HIERARCHY_PATH,
        attributeTypes=attributeTypesForPresence,
        dMin=1 / 2,
        dMax=1 / 3,
    )
    assert result["dMin"] == 1 / 2
    assert result["dMax"] == 1 / 3
    assert result["d-presence"] is False


def testPETAnonymization(DATASET_PATH_ADULT, attributeTypesForAdultAllQi):
    result = PETAnonymization(
        DATASET_PATH_ADULT["originalData"],
        maxSuppressionRate=0.05,
        dMin=0.0,
        dMax=0.2,
        subsetData="data/adult/adult10.csv",
        dataHierarchy=DATASET_PATH_ADULT["dataHierarchy"],
        attributeTypes=attributeTypesForAdultAllQi,
    )
    result["age"] = result["age"].astype(float)
    assert result.equals(
        pd.read_csv("data/DAnonymization.csv", sep=";", skipinitialspace=True)
    )

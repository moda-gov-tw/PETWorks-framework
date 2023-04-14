from PETWorks.attributetypes import IDENTIFIER, QUASI_IDENTIFIER
from PETWorks.attributetypes import SENSITIVE_ATTRIBUTE
from PETWorks.dpresence import (
    measureDPresence,
    validateDPresence,
    PETValidation,
)

from typing import Dict
import pytest
import pandas as pd


ORIGINAL_POPULATION_DATA_PATH = "data/presence.csv"
ANONYMIZED_POPULATION_DATA_PATH = "data/presence_transformed.csv"
ANONYMIZED_SAMPLE_DATA_PATH = "data/presence_anonymized.csv"
DATA_HIERARCHY_PATH = "data/presence_hierarchy"


@pytest.fixture(scope="module")
def attributeTypesForPresence() -> Dict[str, str]:
    attributeTypes = {
        "identifier": IDENTIFIER,
        "name": IDENTIFIER,
        "zip": QUASI_IDENTIFIER,
        "age": QUASI_IDENTIFIER,
        "nationality": QUASI_IDENTIFIER,
        "sen": SENSITIVE_ATTRIBUTE,
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

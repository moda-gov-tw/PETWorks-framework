from PETWorks.deidentification.ldiversity import (
    measureLDiversity,
    validateLDiversity,
    PETValidation,
    PETAnonymization,
)
from typing import Dict
import pytest
import pandas as pd

ANONYMIZED_DATA_PATH = "data/inpatient/inpatient_anonymized.csv"


@pytest.fixture(scope="module")
def attributeTypesForInpatient() -> Dict[str, str]:
    attributeTypes = {
        "zipcode": "quasi_identifier",
        "age": "quasi_identifier",
        "nationality": "quasi_identifier",
        "condition": "sensitive_attribute",
    }
    return attributeTypes


def testMeasureLDiversity(attributeTypesForInpatient):
    dataFrame = pd.read_csv(
        ANONYMIZED_DATA_PATH, skipinitialspace=True, sep=r";"
    )

    dataFrame.columns = dataFrame.columns.str.strip()
    lValues = measureLDiversity(
        dataFrame,
        attributeTypesForInpatient,
    )

    assert set(lValues) == {3, 3, 3}


def testValidateLDiversityFulfilled():
    lLimit = 4
    lValues = [4, 6, 7]
    assert validateLDiversity(lValues, lLimit) is True


def testValidateLDiversityNotFulfilled():
    lLimit = 6
    lValues = [3, 4, 6]
    assert validateLDiversity(lValues, lLimit) is False


def testPETValidationFulfilled(attributeTypesForInpatient):
    result = PETValidation(
        None,
        ANONYMIZED_DATA_PATH,
        "l-diversity",
        attributeTypes=attributeTypesForInpatient,
        l=3,
    )
    assert result["l"] == 3
    assert result["fulfill l-diversity"] is True


def testPETValidationNotFulfilled(attributeTypesForInpatient):
    result = PETValidation(
        None,
        ANONYMIZED_DATA_PATH,
        "l-diversity",
        attributeTypes=attributeTypesForInpatient,
        l=5,
    )
    assert result["l"] == 5
    assert result["fulfill l-diversity"] is False


def testPETAnonymization(DATASET_PATH_ADULT):
    attributeTypes = {
        "age": "quasi_identifier",
        "education": "quasi_identifier",
        "marital-status": "quasi_identifier",
        "native-country": "quasi_identifier",
        "occupation": "sensitive_attribute",
        "race": "quasi_identifier",
        "salary-class": "quasi_identifier",
        "sex": "quasi_identifier",
        "workclass": "quasi_identifier",
    }

    result = PETAnonymization(
        DATASET_PATH_ADULT["originalData"],
        maxSuppressionRate=0.04,
        l=5,
        dataHierarchy=DATASET_PATH_ADULT["dataHierarchy"],
        attributeTypes=attributeTypes,
    )

    assert result.equals(
        pd.read_csv("data/LAnonymization.csv", sep=";", skipinitialspace=True)
    )

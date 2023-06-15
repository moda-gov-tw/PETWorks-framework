from PETWorks.attributetypes import QUASI_IDENTIFIER
from PETWorks.attributetypes import SENSITIVE_ATTRIBUTE
from PETWorks.ldiversity import (
    measureLDiversity,
    validateLDiversity,
    PETValidation,
    PETAnonymization,
)
from typing import Dict
import pytest
import pandas as pd

ANONYMIZED_DATA_PATH = "data/inpatient_anonymized.csv"


@pytest.fixture(scope="module")
def attributeTypesForInpatient() -> Dict[str, str]:
    attributeTypes = {
        "zipcode": QUASI_IDENTIFIER,
        "age": QUASI_IDENTIFIER,
        "nationality": QUASI_IDENTIFIER,
        "condition": SENSITIVE_ATTRIBUTE,
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
        "age": QUASI_IDENTIFIER,
        "education": QUASI_IDENTIFIER,
        "marital-status": QUASI_IDENTIFIER,
        "native-country": QUASI_IDENTIFIER,
        "occupation": SENSITIVE_ATTRIBUTE,
        "race": QUASI_IDENTIFIER,
        "salary-class": QUASI_IDENTIFIER,
        "sex": QUASI_IDENTIFIER,
        "workclass": QUASI_IDENTIFIER,
    }

    result = PETAnonymization(
        DATASET_PATH_ADULT["originalData"],
        DATASET_PATH_ADULT["dataHierarchy"],
        attributeTypes,
        maxSuppressionRate=0.04,
        l=5,
    )

    assert result.equals(
        pd.read_csv("data/LAnonymization.csv", sep=";", skipinitialspace=True)
    )

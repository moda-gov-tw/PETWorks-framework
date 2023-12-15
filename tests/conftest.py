from PETWorks.deidentification.attributetypes import (
    IDENTIFIER,
    QUASI_IDENTIFIER,
    INSENSITIVE_ATTRIBUTE,
    SENSITIVE_ATTRIBUTE,
)
from typing import Dict
import pytest

from PETWorks.deidentification.config import Config

DATASET_PATHS = [
    {
        "originalData": "data/adult/adult.csv",
        "anonymizedData": "data/adult/adult_anonymized.csv",
        "dataHierarchy": "data/adult/adult_hierarchy",
    },
    {
        "originalData": "data/delta/delta.csv",
        "anonymizedData": "data/delta/delta_anonymized.csv",
        "dataHierarchy": "data/delta/delta_hierarchy",
    },
]


@pytest.fixture(scope="session")
def DATASET_PATH_ADULT():
    return DATASET_PATHS[0]


@pytest.fixture(scope="session")
def DATASET_PATH_DELTA():
    return DATASET_PATHS[1]


@pytest.fixture(scope="session")
def attributeTypesForAdult() -> Dict[str, str]:
    attributeTypes = {
        "age": IDENTIFIER,
        "education": IDENTIFIER,
        "marital-status": QUASI_IDENTIFIER,
        "native-country": QUASI_IDENTIFIER,
        "occupation": QUASI_IDENTIFIER,
        "race": INSENSITIVE_ATTRIBUTE,
        "salary-class": INSENSITIVE_ATTRIBUTE,
        "sex": SENSITIVE_ATTRIBUTE,
        "workclass": SENSITIVE_ATTRIBUTE,
    }
    return attributeTypes


@pytest.fixture(scope="session")
def attributeTypesForAdultAllQi() -> Dict[str, str]:
    attributeTypes = {
        "age": QUASI_IDENTIFIER,
        "education": QUASI_IDENTIFIER,
        "marital-status": QUASI_IDENTIFIER,
        "native-country": QUASI_IDENTIFIER,
        "occupation": QUASI_IDENTIFIER,
        "race": QUASI_IDENTIFIER,
        "salary-class": QUASI_IDENTIFIER,
        "sex": QUASI_IDENTIFIER,
        "workclass": QUASI_IDENTIFIER,
    }
    return attributeTypes

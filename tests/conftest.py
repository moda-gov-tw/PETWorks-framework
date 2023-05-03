from PETWorks.attributetypes import (
    IDENTIFIER,
    QUASI_IDENTIFIER,
    INSENSITIVE_ATTRIBUTE,
    SENSITIVE_ATTRIBUTE,
)
from typing import Dict
import pytest

DATASET_PATHS = [
    {
        "originalData": "data/adult.csv",
        "anonymizedData": "data/adult_anonymized.csv",
        "dataHierarchy": "data/adult_hierarchy",
    },
    {
        "originalData": "data/delta.csv",
        "anonymizedData": "data/delta_anonymized.csv",
        "dataHierarchy": "data/delta_hierarchy",
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
    
from typing import Dict
import pytest

from PETWorks.deidentification.config import Config

DATASET_PATHS = [
    {
        "originalData": "datasets/adult/adult.csv",
        "anonymizedData": "datasets/adult/adult_anonymized.csv",
        "dataHierarchy": "datasets/adult/adult_hierarchy",
    },
    {
        "originalData": "datasets/delta/delta.csv",
        "anonymizedData": "datasets/delta/delta_anonymized.csv",
        "dataHierarchy": "datasets/delta/delta_hierarchy",
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
        "age": "identifier",
        "education": "identifier",
        "marital-status": "quasi_identifier",
        "native-country": "quasi_identifier",
        "occupation": "quasi_identifier",
        "race": "insensitive_attribute",
        "salary-class": "insensitive_attribute",
        "sex": "sensitive_attribute",
        "workclass": "sensitive_attribute",
    }
    return attributeTypes


@pytest.fixture(scope="session")
def attributeTypesForAdultAllQi() -> Dict[str, str]:
    attributeTypes = {
        "age": "quasi_identifier",
        "education": "quasi_identifier",
        "marital-status": "quasi_identifier",
        "native-country": "quasi_identifier",
        "occupation": "quasi_identifier",
        "race": "quasi_identifier",
        "salary-class": "quasi_identifier",
        "sex": "quasi_identifier",
        "workclass": "quasi_identifier",
    }
    return attributeTypes

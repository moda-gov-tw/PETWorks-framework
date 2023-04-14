import pytest

DATASET_PATHS = [
    {
        "originalData": "data/adult.csv",
        "anonymizedData": "data/adult_anonymized.csv",
        "dataHierarchy": "data/adult_hierarchy",
    }
]


@pytest.fixture(scope="session")
def DATASET_PATH_ADULT():
    return DATASET_PATHS[0]

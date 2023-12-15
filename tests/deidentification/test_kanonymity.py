from PETWorks.deidentification.kanonymity import (
    PETValidation,
    PETAnonymization,
)
import pandas as pd


def testPETValidationFulfilled(DATASET_PATH_ADULT, attributeTypesForAdult):
    result = PETValidation(
        None,
        DATASET_PATH_ADULT["anonymizedData"],
        "k-anonymity",
        attributeTypes=attributeTypesForAdult,
        k=5,
    )
    assert result["k"] == 5
    assert result["fulfill k-anonymity"] is True


def testPETValidationNotFulfilled(DATASET_PATH_ADULT, attributeTypesForAdult):
    result = PETValidation(
        None,
        DATASET_PATH_ADULT["anonymizedData"],
        "k-anonymity",
        attributeTypes=attributeTypesForAdult,
        k=6,
    )
    assert result["k"] == 6
    assert result["fulfill k-anonymity"] is False


def testPETAnonymization(DATASET_PATH_ADULT, attributeTypesForAdultAllQi):
    result = PETAnonymization(
        DATASET_PATH_ADULT["originalData"],
        maxSuppressionRate=0.04,
        k=5,
        dataHierarchy=DATASET_PATH_ADULT["dataHierarchy"],
        attributeTypes=attributeTypesForAdultAllQi,
    )

    assert result.equals(
        pd.read_csv("data/KAnonymization.csv", sep=";", skipinitialspace=True)
    )

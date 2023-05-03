from PETWorks.kanonymity import PETValidation


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

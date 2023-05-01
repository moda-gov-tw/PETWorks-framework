from PETWorks.nonUniformEntropy import PETValidation


def testPETValidation(DATASET_PATH_ADULT, attributeTypesForAdult):
    assert (
        PETValidation(
            DATASET_PATH_ADULT["originalData"],
            DATASET_PATH_ADULT["anonymizedData"],
            "Non-Uniform Entropy",
            dataHierarchy=DATASET_PATH_ADULT["dataHierarchy"],
            attributeTypes=attributeTypesForAdult,
        )["Non-Uniform Entropy"]
        == 0.6385286721819015
    )

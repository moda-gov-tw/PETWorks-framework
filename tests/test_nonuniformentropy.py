from PETWorks.nonUniformEntropy import PETValidation


def testPETValidation(
    DATASET_PATH_ADULT,
):
    assert (
        PETValidation(
            DATASET_PATH_ADULT["originalData"],
            DATASET_PATH_ADULT["anonymizedData"],
            "Non-Uniform Entropy",
            dataHierarchy=DATASET_PATH_ADULT["dataHierarchy"],
        )["Non-Uniform Entropy"]
        == 0.6691909578638351
    )

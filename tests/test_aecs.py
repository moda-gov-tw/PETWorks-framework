from PETWorks.aecs import PETValidation


def testPETValidation(
    DATASET_PATH_ADULT,
):
    assert (
        PETValidation(
            DATASET_PATH_ADULT["originalData"],
            DATASET_PATH_ADULT["anonymizedData"],
            "AECS",
        )["AECS"]
        == 0.9992930131052006
    )

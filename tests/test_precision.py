from PETWorks.precision import PETValidation


def testPETValidation(
    DATASET_PATH_ADULT,
):
    assert (
        PETValidation(
            DATASET_PATH_ADULT["originalData"],
            DATASET_PATH_ADULT["anonymizedData"],
            "Precision",
            dataHierarchy=DATASET_PATH_ADULT["dataHierarchy"],
        )["precision"]
        == 0.7271401100722763
    )

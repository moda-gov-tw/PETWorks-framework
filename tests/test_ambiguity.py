from PETWorks.ambiguity import PETValidation


def testPETValidation(
    DATASET_PATH_ADULT,
):
    assert (
        PETValidation(
            DATASET_PATH_ADULT["originalData"],
            DATASET_PATH_ADULT["anonymizedData"],
            "Ambiguity",
            dataHierarchy=DATASET_PATH_ADULT["dataHierarchy"],
        )["ambiguity"]
        == 0.7271401100722763
    )

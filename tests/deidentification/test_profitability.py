from PETWorks.deidentification.profitability import PETValidation


def testPETValidation(DATASET_PATH_DELTA):
    attributeTypes = {
        "zip": "quasi_identifier",
        "age": "quasi_identifier",
        "nationality": "quasi_identifier",
        "salary-class": "insensitive_attribute",
    }

    result = PETValidation(
        DATASET_PATH_DELTA["originalData"],
        DATASET_PATH_DELTA["anonymizedData"],
        "profitability",
        dataHierarchy=DATASET_PATH_DELTA["dataHierarchy"],
        attributeTypes=attributeTypes,
        allowAttack=True,
        adversaryCost=4,
        adversaryGain=300,
        publisherLost=300,
        publisherBenefit=1200,
    )

    assert result == {
        "allow attack": True,
        "adversary's cost": 4,
        "adversary's gain": 300,
        "publisher's loss": 300,
        "publisher's benefit": 1200,
        "isProfitable": True,
    }

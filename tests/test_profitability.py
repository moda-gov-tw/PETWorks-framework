from PETWorks.attributetypes import QUASI_IDENTIFIER, INSENSITIVE_ATTRIBUTE
from PETWorks.profitability import PETValidation


def testPETValidation(DATASET_PATH_DELTA):
    attributeTypes = {
        "zip": QUASI_IDENTIFIER,
        "age": QUASI_IDENTIFIER,
        "nationality": QUASI_IDENTIFIER,
        "salary-class": INSENSITIVE_ATTRIBUTE,
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

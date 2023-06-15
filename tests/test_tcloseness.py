from PETWorks.attributetypes import QUASI_IDENTIFIER
from PETWorks.attributetypes import SENSITIVE_ATTRIBUTE
from PETWorks.tcloseness import PETAnonymization
import pandas as pd


def testPETAnonymizationOrderedTCloseness(DATASET_PATH_ADULT):
    attributeTypes = {
        "age": SENSITIVE_ATTRIBUTE,
        "education": QUASI_IDENTIFIER,
        "marital-status": QUASI_IDENTIFIER,
        "native-country": QUASI_IDENTIFIER,
        "occupation": QUASI_IDENTIFIER,
        "race": QUASI_IDENTIFIER,
        "salary-class": QUASI_IDENTIFIER,
        "sex": QUASI_IDENTIFIER,
        "workclass": QUASI_IDENTIFIER,
    }

    result = PETAnonymization(
        DATASET_PATH_ADULT["originalData"],
        DATASET_PATH_ADULT["dataHierarchy"],
        attributeTypes,
        maxSuppressionRate=0.04,
        t=0.2,
    )
    result["age"] = result["age"].astype(int)
    assert result.equals(
        pd.read_csv(
            "data/OrderedTAnonymization.csv", sep=";", skipinitialspace=True
        )
    )


def testPETAnonymizationHierarchicalTCloseness(DATASET_PATH_ADULT):
    attributeTypes = {
        "age": QUASI_IDENTIFIER,
        "education": QUASI_IDENTIFIER,
        "marital-status": QUASI_IDENTIFIER,
        "native-country": QUASI_IDENTIFIER,
        "occupation": SENSITIVE_ATTRIBUTE,
        "race": QUASI_IDENTIFIER,
        "salary-class": QUASI_IDENTIFIER,
        "sex": QUASI_IDENTIFIER,
        "workclass": QUASI_IDENTIFIER,
    }

    result = PETAnonymization(
        DATASET_PATH_ADULT["originalData"],
        DATASET_PATH_ADULT["dataHierarchy"],
        attributeTypes,
        maxSuppressionRate=0.04,
        t=0.2,
    )

    assert result.equals(
        pd.read_csv(
            "data/HierarchicalTAnonymization.csv",
            sep=";",
            skipinitialspace=True,
        )
    )

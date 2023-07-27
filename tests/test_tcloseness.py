from PETWorks.attributetypes import (
    QUASI_IDENTIFIER,
    SENSITIVE_ATTRIBUTE,
    INSENSITIVE_ATTRIBUTE,
)
from PETWorks.tcloseness import PETAnonymization, measureTCloseness
from PETWorks.arx import loadDataHierarchyNatively, getAttributeNameByType
import pandas as pd


def testMeasureTClosenessNumeral():
    anonymizedData = pd.read_csv(
        "data/merit.csv", sep=";", skipinitialspace=True
    )
    attributeTypes = {"Name": QUASI_IDENTIFIER, "Merit": SENSITIVE_ATTRIBUTE}
    qiNames = getAttributeNameByType(attributeTypes, QUASI_IDENTIFIER)
    sensitiveAttribute = getAttributeNameByType(
        attributeTypes, SENSITIVE_ATTRIBUTE
    )[0]
    assert (
        measureTCloseness(anonymizedData, sensitiveAttribute, qiNames, None)
        == 0.26666666666666666
    )


def testMeasureTClosenessHierarchical():
    anonymizedData = pd.read_csv(
        "data/disease.csv", sep=";", skipinitialspace=True
    )
    dataHierarchy = loadDataHierarchyNatively("data/disease_hierarchy", ";")
    attributeTypes = {
        "ZIPCode": QUASI_IDENTIFIER,
        "Age": QUASI_IDENTIFIER,
        "Salary": INSENSITIVE_ATTRIBUTE,
        "Disease": SENSITIVE_ATTRIBUTE,
    }
    qiNames = getAttributeNameByType(attributeTypes, QUASI_IDENTIFIER)
    sensitiveAttribute = getAttributeNameByType(
        attributeTypes, SENSITIVE_ATTRIBUTE
    )[0]

    assert (
        measureTCloseness(
            anonymizedData,
            sensitiveAttribute,
            qiNames,
            dataHierarchy.get(sensitiveAttribute, None),
        )
        == 0.29629629850387573
    )


def testMeasureTClosenessEqual():
    anonymizedData = pd.read_csv(
        "data/disease.csv", sep=";", skipinitialspace=True
    )
    attributeTypes = {
        "ZIPCode": QUASI_IDENTIFIER,
        "Age": QUASI_IDENTIFIER,
        "Salary": INSENSITIVE_ATTRIBUTE,
        "Disease": SENSITIVE_ATTRIBUTE,
    }
    qiNames = getAttributeNameByType(attributeTypes, QUASI_IDENTIFIER)
    sensitiveAttribute = getAttributeNameByType(
        attributeTypes, SENSITIVE_ATTRIBUTE
    )[0]

    assert (
        measureTCloseness(anonymizedData, sensitiveAttribute, qiNames, None)
        == 0.5555555555555556
    )


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

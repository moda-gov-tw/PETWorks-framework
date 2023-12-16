from PETWorks.deidentification.tcloseness import (
    PETAnonymization,
    measureTCloseness,
)
from PETWorks.deidentification.arx import (
    loadDataHierarchyNatively,
    getAttributeNameByType,
)
import pandas as pd


def testMeasureTClosenessNumeral():
    anonymizedData = pd.read_csv(
        "data/merit.csv", sep=";", skipinitialspace=True
    )
    attributeTypes = {"Name": "quasi_identifier", "Merit": "sensitive_attribute"}
    qiNames = getAttributeNameByType(attributeTypes, "quasi_identifier")
    sensitiveAttribute = getAttributeNameByType(
        attributeTypes, "sensitive_attribute"
    )[0]
    assert (
        measureTCloseness(anonymizedData, sensitiveAttribute, qiNames, None)
        == 0.26666666666666666
    )


def testMeasureTClosenessHierarchical():
    anonymizedData = pd.read_csv(
        "data/disease/disease.csv", sep=";", skipinitialspace=True
    )
    dataHierarchy = loadDataHierarchyNatively(
        "data/disease/disease_hierarchy", ";"
    )
    attributeTypes = {
        "ZIPCode": "quasi_identifier",
        "Age": "quasi_identifier",
        "Salary": "insensitive_attribute",
        "Disease": "sensitive_attribute",
    }
    qiNames = getAttributeNameByType(attributeTypes, "quasi_identifier")
    sensitiveAttribute = getAttributeNameByType(
        attributeTypes, "sensitive_attribute"
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
        "data/disease/disease.csv", sep=";", skipinitialspace=True
    )
    attributeTypes = {
        "ZIPCode": "quasi_identifier",
        "Age": "quasi_identifier",
        "Salary": "insensitive_attribute",
        "Disease": "sensitive_attribute",
    }
    qiNames = getAttributeNameByType(attributeTypes, "quasi_identifier")
    sensitiveAttribute = getAttributeNameByType(
        attributeTypes, "sensitive_attribute"
    )[0]

    assert (
        measureTCloseness(anonymizedData, sensitiveAttribute, qiNames, None)
        == 0.5555555555555556
    )


def testPETAnonymizationOrderedTCloseness(DATASET_PATH_ADULT):
    attributeTypes = {
        "age": "sensitive_attribute",
        "education": "quasi_identifier",
        "marital-status": "quasi_identifier",
        "native-country": "quasi_identifier",
        "occupation": "quasi_identifier",
        "race": "quasi_identifier",
        "salary-class": "quasi_identifier",
        "sex": "quasi_identifier",
        "workclass": "quasi_identifier",
    }

    result = PETAnonymization(
        DATASET_PATH_ADULT["originalData"],
        maxSuppressionRate=0.04,
        t=0.2,
        dataHierarchy=DATASET_PATH_ADULT["dataHierarchy"],
        attributeTypes=attributeTypes,
    )
    result["age"] = result["age"].astype(int)
    assert result.equals(
        pd.read_csv(
            "data/OrderedTAnonymization.csv", sep=";", skipinitialspace=True
        )
    )


def testPETAnonymizationHierarchicalTCloseness(DATASET_PATH_ADULT):
    attributeTypes = {
        "age": "quasi_identifier",
        "education": "quasi_identifier",
        "marital-status": "quasi_identifier",
        "native-country": "quasi_identifier",
        "occupation": "sensitive_attribute",
        "race": "quasi_identifier",
        "salary-class": "quasi_identifier",
        "sex": "quasi_identifier",
        "workclass": "quasi_identifier",
    }

    result = PETAnonymization(
        DATASET_PATH_ADULT["originalData"],
        maxSuppressionRate=0.04,
        t=0.2,
        dataHierarchy=DATASET_PATH_ADULT["dataHierarchy"],
        attributeTypes=attributeTypes,
    )

    assert result.equals(
        pd.read_csv(
            "data/HierarchicalTAnonymization.csv",
            sep=";",
            skipinitialspace=True,
        )
    )

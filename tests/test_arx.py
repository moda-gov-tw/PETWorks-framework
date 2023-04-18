from typing import Dict

import pytest
from py4j.java_collections import JavaArray

from PETWorks.arx import (
    Data,
    JavaApi,
    loadDataFromCsv,
    loadDataHierarchy,
    setDataHierarchies,
)
from PETWorks.attributetypes import (
    IDENTIFIER,
    INSENSITIVE_ATTRIBUTE,
    QUASI_IDENTIFIER,
    SENSITIVE_ATTRIBUTE,
)


@pytest.fixture(scope="session")
def javaApi() -> JavaApi:
    return JavaApi()


@pytest.fixture(scope="module")
def attributeTypesForAdult() -> Dict[str, str]:
    attributeTypes = {
        "age": IDENTIFIER,
        "education": IDENTIFIER,
        "marital-status": QUASI_IDENTIFIER,
        "native-country": QUASI_IDENTIFIER,
        "occupation": QUASI_IDENTIFIER,
        "race": INSENSITIVE_ATTRIBUTE,
        "salary-class": INSENSITIVE_ATTRIBUTE,
        "sex": INSENSITIVE_ATTRIBUTE,
        "workclass": SENSITIVE_ATTRIBUTE,
    }
    return attributeTypes


@pytest.fixture(scope="module")
def errorAttributeTypesForAdult() -> Dict[str, str]:
    attributeTypes = {
        "age": "wrong attribute",
    }
    return attributeTypes


@pytest.fixture(scope="module")
def arxDataAdult(DATASET_PATH_ADULT, javaApi) -> Data:
    return loadDataFromCsv(
        DATASET_PATH_ADULT["originalData"],
        javaApi.StandardCharsets.UTF_8,
        ";",
        javaApi,
    )


@pytest.fixture(scope="module")
def arxHierarchyAdult(DATASET_PATH_ADULT, javaApi) -> Dict[str, JavaArray]:
    return loadDataHierarchy(
        DATASET_PATH_ADULT["dataHierarchy"],
        javaApi.StandardCharsets.UTF_8,
        ";",
        javaApi,
    )


def testSetDataHierarchiesErrorAttributeTypes(
    arxDataAdult, arxHierarchyAdult, errorAttributeTypesForAdult, javaApi
):
    with pytest.raises(ValueError):
        setDataHierarchies(
            arxDataAdult,
            arxHierarchyAdult,
            errorAttributeTypesForAdult,
            javaApi,
        )


def testSetDataHierarchies(
    arxDataAdult, arxHierarchyAdult, attributeTypesForAdult, javaApi
):
    setDataHierarchies(arxDataAdult, arxHierarchyAdult, attributeTypesForAdult, javaApi)

    dataDefinition = arxDataAdult.getDefinition()
    maritalStatusHierarchy = dataDefinition.getHierarchy("marital-status")
    assert len(maritalStatusHierarchy) == 7
    assert len(maritalStatusHierarchy[0]) == 3

    nativeCountryHierarchy = dataDefinition.getHierarchy("native-country")
    assert len(nativeCountryHierarchy) == 41
    assert len(nativeCountryHierarchy[0]) == 3

    occupationHierarchy = dataDefinition.getHierarchy("occupation")
    assert len(occupationHierarchy) == 14
    assert len(occupationHierarchy[0]) == 3

    assert (
        dataDefinition.getAttributeType("age").toString()
        == "IDENTIFYING_ATTRIBUTE"
    )
    assert (
        dataDefinition.getAttributeType("education").toString()
        == "IDENTIFYING_ATTRIBUTE"
    )
    assert (
        dataDefinition.getAttributeType("race").toString()
        == "INSENSITIVE_ATTRIBUTE"
    )
    assert (
        dataDefinition.getAttributeType("salary-class").toString()
        == "INSENSITIVE_ATTRIBUTE"
    )
    assert (
        dataDefinition.getAttributeType("sex").toString()
        == "INSENSITIVE_ATTRIBUTE"
    )
    assert (
        dataDefinition.getAttributeType("workclass").toString()
        == "INSENSITIVE_ATTRIBUTE"
    )

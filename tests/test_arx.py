from typing import Dict

import pandas as pd
import pytest
from py4j.java_collections import JavaArray

from PETWorks.arx import (
    Data,
    JavaApi,
    loadDataFromCsv,
    loadDataHierarchy,
    setDataHierarchies,
    anonymizeData,
    getDataFrame,
)
from PETWorks.attributetypes import QUASI_IDENTIFIER, SENSITIVE_ATTRIBUTE


@pytest.fixture(scope="session")
def javaApi() -> JavaApi:
    return JavaApi()


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


def testSetDataHierarchiesNoHierarchies(
    arxDataAdult, attributeTypesForAdult, javaApi
):
    setDataHierarchies(arxDataAdult, None, attributeTypesForAdult, javaApi)
    dataDefinition = arxDataAdult.getDefinition()
    maritalStatusHierarchy = dataDefinition.getHierarchy("marital-status")
    assert len(maritalStatusHierarchy) == 0

    nativeCountryHierarchy = dataDefinition.getHierarchy("native-country")
    assert len(nativeCountryHierarchy) == 0

    occupationHierarchy = dataDefinition.getHierarchy("occupation")
    assert len(occupationHierarchy) == 0

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


def testSetDataHierarchiesSensitiveEnabled(
    arxDataAdult, arxHierarchyAdult, javaApi
):
    attributeTypes = {
        "age": SENSITIVE_ATTRIBUTE,
    }
    setDataHierarchies(
        arxDataAdult, arxHierarchyAdult, attributeTypes, javaApi, True
    )

    dataDefinition = arxDataAdult.getDefinition()
    assert (
        dataDefinition.getAttributeType("age").toString()
        == "SENSITIVE_ATTRIBUTE"
    )


def testSetDataHierarchies(
    arxDataAdult, arxHierarchyAdult, attributeTypesForAdult, javaApi
):
    setDataHierarchies(
        arxDataAdult, arxHierarchyAdult, attributeTypesForAdult, javaApi
    )

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


def testGetDataFrameWithNone():
    assert getDataFrame(None).empty is True


def testGetDataFrame(arxDataAdult):
    assert len(getDataFrame(arxDataAdult)) == 30162


def testAnonymizeData(
    arxDataAdult, arxHierarchyAdult, attributeTypesForAdultAllQi, javaApi
):
    setDataHierarchies(
        arxDataAdult, arxHierarchyAdult, attributeTypesForAdultAllQi, javaApi
    )

    assert (
        anonymizeData(
            arxDataAdult,
            [javaApi.KAnonymity(5)],
            javaApi,
            javaApi.createPrecomputedEntropyMetric(0.1, True),
            0.04,
        )
        .getGlobalOptimum()
        .getHighestScore()
        .toString()
        == "255559.85455731067"
    )

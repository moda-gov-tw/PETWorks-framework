from PETWorks.deidentification.arx import (
    getAttributeNameByType,
    JavaApi,
    anonymizeData,
    getDataFrame,
    loadDataFromCsv,
    loadDataHierarchy,
    setDataHierarchies,
)
from PETWorks.deidentification.attributetypes import QUASI_IDENTIFIER
import pandas as pd
from typing import Dict


def _measureKAnonymity(anonymized: pd.DataFrame, qiNames: list[str]) -> int:
    suppressedValues = ["*"] * len(qiNames)
    anonymized = anonymized.loc[
        ~anonymized[qiNames].isin(suppressedValues).all(axis=1)
    ]
    return anonymized.groupby(qiNames).count().min().min()


def _validateKAnonymity(kValue: int, k: int) -> bool:
    return k <= kValue


def PETValidation(
    foo, anonymized, bar, k, dataHierarchy=None, attributeTypes={}
):
    anonymized = pd.read_csv(anonymized, sep=";", skipinitialspace=True)
    qiNames = list(getAttributeNameByType(attributeTypes, QUASI_IDENTIFIER))

    kValue = int(_measureKAnonymity(anonymized, qiNames))
    fulFillKAnonymity = _validateKAnonymity(kValue, k)

    return {"k": k, "fulfill k-anonymity": fulFillKAnonymity}


def PETAnonymization(
    originalData: str,
    maxSuppressionRate: float,
    k: int,
    dataHierarchy: str = None,
    attributeTypes: Dict[str, str] = {},
) -> pd.DataFrame:
    javaApi = JavaApi()
    originalData = loadDataFromCsv(
        originalData, javaApi.StandardCharsets.UTF_8, ";", javaApi
    )

    dataHierarchy = loadDataHierarchy(
        dataHierarchy, javaApi.StandardCharsets.UTF_8, ";", javaApi
    )

    setDataHierarchies(originalData, dataHierarchy, attributeTypes, javaApi)

    anonymizedResult = anonymizeData(
        originalData,
        [javaApi.KAnonymity(k)],
        javaApi,
        None,
        float(maxSuppressionRate),
    )
    anonymizedData = javaApi.Data.create(
        anonymizedResult.getOutput(True).iterator()
    )
    return getDataFrame(anonymizedData)

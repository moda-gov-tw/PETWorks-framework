from PETWorks.arx import getAttributeNameByType
from PETWorks.attributetypes import QUASI_IDENTIFIER
import pandas as pd


def _measureKAnonymity(anonymized: pd.DataFrame, qiNames: list[str]) -> int:
    suppressedValues = ["*"] * len(qiNames)
    anonymized = anonymized.loc[
        ~anonymized[qiNames].isin(suppressedValues).all(axis=1)
    ]
    return anonymized.groupby(qiNames).count().min().min()


def _validateKAnonymity(kValue: int, k: int) -> bool:
    return k <= kValue


def PETValidation(foo, anonymized, bar, attributeTypes, k):
    anonymized = pd.read_csv(anonymized, sep=";", skipinitialspace=True)
    qiNames = list(getAttributeNameByType(attributeTypes, QUASI_IDENTIFIER))

    kValue = int(_measureKAnonymity(anonymized, qiNames))
    fulFillKAnonymity = _validateKAnonymity(kValue, k)

    return {"k": k, "fulfill k-anonymity": fulFillKAnonymity}

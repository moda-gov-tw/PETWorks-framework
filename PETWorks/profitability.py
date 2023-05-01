from typing import List
from PETWorks.arx import (
    getAttributeNameByType,
)
from PETWorks.attributetypes import QUASI_IDENTIFIER

import pandas as pd


def _measureProfitabilityPayoffAcceptingAttack(
    anonymizedData: pd.DataFrame,
    qiNames: List[str],
    publisherLost: float,
    publisherBenefit: float,
):
    probabilityOfSuccess = 1 / (anonymizedData.groupby(qiNames).size())

    publisherTotalGain = publisherBenefit * len(anonymizedData)
    publisherTotalLost = (publisherLost * probabilityOfSuccess).sum()

    return publisherTotalGain - publisherTotalLost


def _measureProfitabilityPayoffNoAttack(
    anonymizedData: pd.DataFrame,
    qiNames: List[str],
    adversaryCost: float,
    adversaryGain: float,
) -> float:
    anonymizedData["probabilityOfSuccess"] = 1 / (
        anonymizedData.groupby(qiNames).transform("size").astype(float)
    )

    adversaryTotalGain = (
        anonymizedData["probabilityOfSuccess"] * adversaryGain
    ).sum()

    adversaryTotalCost = len(anonymizedData) * adversaryCost

    return adversaryTotalGain - adversaryTotalCost


def PETValidation(
    original,
    subset,
    tech,
    dataHierarchy,
    attributeTypes,
    allowAttack,
    adversaryCost,
    adversaryGain,
    publisherLost,
    publisherBenefit,
):
    subset = pd.read_csv(subset, sep=";")
    qiNames = getAttributeNameByType(attributeTypes, QUASI_IDENTIFIER)

    if allowAttack:
        isProfitable = bool(
            _measureProfitabilityPayoffAcceptingAttack(
                subset, qiNames, publisherLost, publisherBenefit
            )
            > 0
        )
    else:
        isProfitable = bool(
            _measureProfitabilityPayoffNoAttack(
                subset, qiNames, adversaryCost, adversaryGain
            )
            <= 0
        )

    return {
        "allow attack": allowAttack,
        "adversary's cost": adversaryCost,
        "adversary's gain": adversaryGain,
        "publisher's loss": publisherLost,
        "publisher's benefit": publisherBenefit,
        "isProfitable": isProfitable,
    }

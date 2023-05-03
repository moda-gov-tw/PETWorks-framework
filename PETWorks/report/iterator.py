from PETWorks.report import *

from itertools import product
from os import PathLike
from typing import Generator, List
import pandas as pd


def __generateSuppressionLimits(step: float) -> List[float]:
    return [(i / step) for i in range(0, step + 1)]


def __generateKValues(maxK: int) -> List[int]:
    return list(range(1, maxK + 1))


def generateConfigs(
    originalData: PathLike,
) -> Generator[AnonymityConfig, None, None]:
    numOfDataRow = len(pd.read_csv(originalData, sep=";"))

    suppressionLimits = __generateSuppressionLimits(numOfDataRow)
    kValues = __generateKValues(numOfDataRow)

    total = len(suppressionLimits) * len(kValues)

    configs = (
        AnonymityConfig(suppressionLimit, k, None)
        for suppressionLimit, k in product(suppressionLimits, kValues)
    )

    return total, configs

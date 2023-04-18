import pandas as pd

from typing import Callable


def isAnalysiable(
    originalData: pd.DataFrame,
    anonymizedData: pd.DataFrame,
    analyzingFunction: Callable,
    error: float,
) -> bool:
    originalValue = analyzingFunction(originalData)
    anonymityValue = analyzingFunction(anonymizedData)

    return abs((originalValue - anonymityValue)) < error

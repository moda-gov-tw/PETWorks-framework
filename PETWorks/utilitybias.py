from typing import Any, Callable


def PETValidation(
    original: Any,
    anonymized: Any,
    processingFunc: Callable[[Any], float],
    maxBias: float,
):
    expectedValue = processingFunc(original)
    trueValue = processingFunc(anonymized)

    utilityBias = abs(trueValue - expectedValue) <= maxBias

    return {"UtilityBias": bool(utilityBias)}

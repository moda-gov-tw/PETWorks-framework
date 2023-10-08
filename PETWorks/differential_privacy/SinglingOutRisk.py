from typing import Dict
import pandas as pd
from PETWorks.differential_privacy.anonymeter import _resultToDict
from anonymeter.evaluators import SinglingOutEvaluator


def PETValidation(
    synthetic, original, control=None, nAttack=100, n_col=3
) -> Dict[str, float]:
    synthetic = pd.read_csv(synthetic)
    original = pd.read_csv(original)
    if control:
        control = pd.read_csv(control)

    evaluator = SinglingOutEvaluator(
        ori=original,
        syn=synthetic,
        control=control,
        n_attacks=nAttack,
        n_cols=n_col,
    )

    try:
        evaluator.evaluate(mode="multivariate")
        result = evaluator.results()
        return _resultToDict(result)
    except RuntimeError as ex:
        pass

    return _resultToDict(None)

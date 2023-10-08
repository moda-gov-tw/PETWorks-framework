from typing import Dict
import pandas as pd
from PETWorks.differential_privacy.anonymeter import resultToDict
from anonymeter.evaluators import LinkabilityEvaluator


def PETValidation(
    synthetic, original, auxiliaryColumns, control, nAttack=2000
) -> Dict[str, float]:
    synthetic = pd.read_csv(synthetic)
    original = pd.read_csv(original)
    if control:
        control = pd.read_csv(control)

    evaluator = LinkabilityEvaluator(
        ori=original,
        syn=synthetic,
        control=control,
        n_attacks=nAttack,
        aux_cols=auxiliaryColumns,
        n_neighbors=10,
    )

    evaluator.evaluate(n_jobs=-2)  # -2 means using all expect one CPUs.
    result = evaluator.results()

    return resultToDict(result)

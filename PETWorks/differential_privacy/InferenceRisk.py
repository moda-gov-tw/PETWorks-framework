from typing import Dict
import pandas as pd
from PETWorks.differential_privacy.anonymeter import resultToDict
from anonymeter.evaluators import InferenceEvaluator


def PETValidation(
    synthetic, original, control, nAttack=1000
) -> Dict[str, Dict[str, float]]:
    synthetic = pd.read_csv(synthetic)
    original = pd.read_csv(original)
    if control:
        control = pd.read_csv(control)

    results = {}

    for secret in original.columns:
        auxCols = [col for col in original.columns if col != secret]

        evaluator = InferenceEvaluator(
            ori=original,
            syn=synthetic,
            control=control,
            aux_cols=auxCols,
            secret=secret,
            n_attacks=nAttack,
        )
        evaluator.evaluate(n_jobs=-2)
        results[secret] = resultToDict(evaluator.results())

    return results

from typing import Dict
from anonymeter.stats.confidence import EvaluationResults


def resultToDict(result: EvaluationResults = None) -> Dict[str, int]:
    if result:
        return {
            "Success rate of main attack": result.attack_rate.value,
            "Success rate of baseline attack": result.baseline_rate.value,
            "Success rate of control attack": result.control_rate.value,
        }
    else:
        return {
            "Success rate of main attack": 0,
            "Success rate of baseline attack": 0,
            "Success rate of control attack": 0,
        }

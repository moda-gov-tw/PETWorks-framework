import PETWorks.synthetic_data.InferenceRisk as InferenceRisk


def testPETValidation():
    synthetic = "datasets/adult/adults_syn_ctgan.csv"
    original = "datasets/adult/adults_train.csv"
    control = "datasets/adult/adults_control.csv"

    result = InferenceRisk.PETValidation(
        synthetic, original, control, nAttack=5
    )

    assert set(result.keys()) == {"age", "type_employer", "fnlwgt"}
    for info in result.values():
        assert set(info.keys()) == {
            "Success rate of main attack",
            "Success rate of baseline attack",
            "Success rate of control attack",
        }

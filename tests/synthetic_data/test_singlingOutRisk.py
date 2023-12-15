import PETWorks.synthetic_data.SinglingOutRisk as SinglingOutRisk


def testPETValidation():
    synthetic = "data/adult/adults_syn_ctgan.csv"
    original = "data/adult/adults_train.csv"
    control = "data/adult/adults_control.csv"

    result = SinglingOutRisk.PETValidation(
        synthetic, original, control, nAttack=5
    )
    assert set(result.keys()) == {
        "Success rate of main attack",
        "Success rate of baseline attack",
        "Success rate of control attack",
    }

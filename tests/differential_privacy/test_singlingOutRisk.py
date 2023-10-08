import PETWorks.differential_privacy.SinglingOutRisk as SinglingOutRisk


def testPETValidation():
    synthetic = "data/adults_syn_ctgan.csv"
    original = "data/adults_train.csv"
    control = "data/adults_control.csv"

    result = SinglingOutRisk.PETValidation(
        synthetic, original, control, nAttack=5
    )
    assert set(result.keys()) == {
        "Success rate of main attack",
        "Success rate of baseline attack",
        "Success rate of control attack",
    }

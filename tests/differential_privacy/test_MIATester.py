import PETWorks.differential_privacy.MIATester as MIATester


def testPETValidation():
    synthetic = "data/synthetic_NHANES.csv"
    original = "data/NHANES.csv"
    epsilon = 10

    result = MIATester.PETValidation(synthetic, original, epsilon)

    assert (
        result["Does the data processed with differential privacy"]
        == "Possibly Yes"
    )

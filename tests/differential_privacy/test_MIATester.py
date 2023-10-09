import pytest
import PETWorks.differential_privacy.MIATester as MIATester

@pytest.mark.skip(reason="Take too much time that GitHub action can tolerate. (Over than 30 mins)")
def testPETValidation():
    synthetic = "data/synthetic_NHANES.csv"
    original = "data/NHANES.csv"
    epsilon = 10

    result = MIATester.PETValidation(synthetic, original, epsilon)

    assert (
        result["Does the data processed with differential privacy"]
        == "Possibly Yes"
    )

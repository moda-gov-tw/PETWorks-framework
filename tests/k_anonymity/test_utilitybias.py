import PETWorks.deidentification.utilitybias as UtilityBias


def testPETValidationSuccess():
    original = [1, 2, 3, 4, 5, 6]
    anonymized = [6, 5, 4, 1, 2, 4]

    result = UtilityBias.PETValidation(
        original=original, anonymized=anonymized, processingFunc=sum, maxBias=1
    )
    assert result["UtilityBias"]


def testPETValidationFail():
    original = [1, 2, 3, 4, 5, 6]
    anonymized = [6, 5, 4, 1, 2, 5]

    result = UtilityBias.PETValidation(
        original=original, anonymized=anonymized, processingFunc=sum, maxBias=1
    )
    assert not result["UtilityBias"]

import PETWorks.homomorphic_encryption.Binary as Binary


def testFindExternalFunctions():
    executable = "tests/homomorphic_encryption/helloWorld"

    externalFunctions = Binary.listExternalFunction(executable)

    assert set(externalFunctions) == {
        "_ITM_deregisterTMCloneTable",
        "_ITM_registerTMCloneTable",
        "__cxa_finalize@GLIBC_2.2.5",
        "__gmon_start__",
        "__libc_start_main@GLIBC_2.34",
        "puts@GLIBC_2.2.5",
    }

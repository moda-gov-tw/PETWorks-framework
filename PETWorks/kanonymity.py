from PETWorks.arx import Data, loadDataFromCsv
from PETWorks.arx import JavaApi, setDataHierarchies


def _measureKAnonymity(anonymized: Data, k: int, javaApi: JavaApi) -> bool:
    if k > anonymized.getHandle().getNumColumns():
        return False

    anonymizer = javaApi.ARXAnonymizer()
    config = javaApi.ARXConfiguration.create()

    config.addPrivacyModel(javaApi.KAnonymity(k))
    result = anonymizer.anonymize(anonymized, config)

    return bool(result.getOutput())


def PETValidation(foo, anonymized, bar, **other):
    k = other["k"]
    attributeType = other.get("attributeTypes", None)

    javaApi = JavaApi()
    anonymized = loadDataFromCsv(
        anonymized, javaApi.StandardCharsets.UTF_8, ";", javaApi
    )

    setDataHierarchies(anonymized, None, attributeType, javaApi)

    kAnonymity = _measureKAnonymity(anonymized, k)
    return {"k": k, "k-anonymity": kAnonymity}

from PETWorks.arx import Data, gateway, loadDataFromCsv
from PETWorks.attributetypes import QUASI_IDENTIFIER
StandardCharsets = gateway.jvm.java.nio.charset.StandardCharsets
ARXAnonymizer = gateway.jvm.org.deidentifier.arx.ARXAnonymizer
ARXConfiguration = gateway.jvm.org.deidentifier.arx.ARXConfiguration
KAnonymity = gateway.jvm.org.deidentifier.arx.criteria.KAnonymity
AttributeType = gateway.jvm.org.deidentifier.arx.AttributeType


def _setDataHierarchies(data: Data, attributeType: dict) -> None:
    for column in range(data.getHandle().getNumColumns()):
        attribute = data.getHandle().getAttributeName(column)
        if not attributeType:
            data.getDefinition().setAttributeType(
                    attribute, AttributeType.QUASI_IDENTIFYING_ATTRIBUTE)
            continue

        if attributeType.get(attribute) == QUASI_IDENTIFIER:
            data.getDefinition().setAttributeType(
                    attribute, AttributeType.QUASI_IDENTIFYING_ATTRIBUTE)


def _measureKAnonymity(anonymized: Data, k: int) -> bool:

    if k > anonymized.getHandle().getNumColumns():
        return False

    anonymizer = ARXAnonymizer()
    config = ARXConfiguration.create()

    config.addPrivacyModel(KAnonymity(k))
    result = anonymizer.anonymize(anonymized, config)

    return bool(result.getOutput())


def PETValidation(foo, anonymized, bar, **other):
    k = other["k"]
    attributeType = other.get("attributeTypes", None)

    anonymized = loadDataFromCsv(anonymized, StandardCharsets.UTF_8, ";")

    _setDataHierarchies(anonymized, attributeType)

    kanonymity = _measureKAnonymity(anonymized, k)
    return {
            "k": k,
            "k-anonymity": kanonymity
            }

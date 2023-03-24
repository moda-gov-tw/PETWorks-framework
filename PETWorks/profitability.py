from PETWorks.arx import Data, gateway, loadDataFromCsv, loadDataHierarchy
from PETWorks.arx import setDataHierarchies, getSubsetIndices
from PETWorks.arx import getAnonymousLevels, applyAnonymousLevels

StandardCharsets = gateway.jvm.java.nio.charset.StandardCharsets
DataSubset = gateway.jvm.org.deidentifier.arx.DataSubset
HashSet = gateway.jvm.java.util.HashSet

ARXConfiguration = gateway.jvm.org.deidentifier.arx.ARXConfiguration
ARXCostBenefitConfiguration = (
    gateway.jvm.org.deidentifier.arx.ARXCostBenefitConfiguration
)

ARXAnonymizer = gateway.jvm.org.deidentifier.arx.ARXAnonymizer
AttributeType = gateway.jvm.org.deidentifier.arx.AttributeType
Metric = gateway.jvm.org.deidentifier.arx.metric.Metric
Int = gateway.jvm.int

ProfitabilityJournalist = (
    gateway.jvm.org.deidentifier.arx.criteria.ProfitabilityJournalist
)
ProfitabilityJournalistNoAttack = (
    gateway.jvm.org.deidentifier.arx.criteria.ProfitabilityJournalistNoAttack
)


def _measureProfitability(
    original: Data,
    subsetIndices: list[int],
    anonymousLevels: list[int],
    allowAttack: bool,
    adversaryCost: float,
    adversaryGain: float,
    publisherLost: float,
    publisherBenefit: float,
) -> bool:
    indices = HashSet()
    for index in subsetIndices:
        indices.add(index)

    subset = DataSubset.create(original, indices)
    original.getHandle().release()

    config = ARXCostBenefitConfiguration.create()
    config.setAdversaryCost(adversaryCost)
    config.setAdversaryGain(adversaryGain)
    config.setPublisherLoss(publisherLost)
    config.setPublisherBenefit(publisherBenefit)

    arxConfig = ARXConfiguration.create()
    arxConfig.setCostBenefitConfiguration(config)
    arxConfig.setQualityModel(Metric.createPublisherPayoutMetric(False))

    if allowAttack:
        profitabilityModel = ProfitabilityJournalist(subset)
    else:
        profitabilityModel = ProfitabilityJournalistNoAttack(subset)

    arxConfig.addPrivacyModel(profitabilityModel)
    arxConfig.setAlgorithm(
        ARXConfiguration.AnonymizationAlgorithm.BEST_EFFORT_TOP_DOWN
    )

    anonymizer = ARXAnonymizer()
    result = anonymizer.anonymize(original, arxConfig)

    levels = gateway.new_array(Int, len(anonymousLevels))
    for i in range(len(anonymousLevels)):
        levels[i] = anonymousLevels[i]

    lattice = result.getLattice()
    node = lattice.getNode(levels)
    anonymity = str(node.getAnonymity())

    return anonymity == "ANONYMOUS"


def PETValidation(
    original,
    subset,
    tech,
    dataHierarchy,
    attributeTypes,
    allowAttack,
    adversaryCost,
    adversaryGain,
    publisherLost,
    publisherBenefit,
):
    dataHierarchy = loadDataHierarchy(
        dataHierarchy, StandardCharsets.UTF_8, ";"
    )
    original = loadDataFromCsv(original, StandardCharsets.UTF_8, ";")
    subset = loadDataFromCsv(subset, StandardCharsets.UTF_8, ";")

    setDataHierarchies(original, dataHierarchy, attributeTypes)
    setDataHierarchies(subset, dataHierarchy, attributeTypes)

    anonymousLevels = getAnonymousLevels(subset, dataHierarchy)
    anonymizedData = applyAnonymousLevels(original, anonymousLevels)

    subsetIndices = getSubsetIndices(anonymizedData, subset.getHandle())

    isProfitable = _measureProfitability(
        original,
        subsetIndices,
        anonymousLevels,
        allowAttack,
        float(adversaryCost),
        float(adversaryGain),
        float(publisherLost),
        float(publisherBenefit),
    )

    return {
        "allow attack": allowAttack,
        "adversary's cost": adversaryCost,
        "adversary's gain": adversaryGain,
        "publisher's loss": publisherLost,
        "publisher's benefit": publisherBenefit,
        "isProfitable": isProfitable,
    }

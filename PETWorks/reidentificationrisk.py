from PETWorks.arx import Data, gateway, loadDataFromCsv

StandardCharsets = gateway.jvm.java.nio.charset.StandardCharsets
AttributeType = gateway.jvm.org.deidentifier.arx.AttributeType
ARXPopulationModel = gateway.jvm.org.deidentifier.arx.ARXPopulationModel
DataHandle = gateway.jvm.org.deidentifier.arx.DataHandle
RiskModelSampleRisks = (
    gateway.jvm.org.deidentifier.arx.risk.RiskModelSampleRisks
)


def _applyDefinition(data: Data):
    dataHandle = data.getHandle()
    dataDefinition = data.getDefinition()

    for column in range(dataHandle.getNumColumns()):
        attributeName = data.getHandle().getAttributeName(column)
        attributeType = AttributeType.QUASI_IDENTIFYING_ATTRIBUTE
        dataDefinition.setAttributeType(attributeName, attributeType)


def _measureReidentificationRisk(
    data: Data,
) -> RiskModelSampleRisks:
    dataHandle = data.getHandle()
    populationModel = ARXPopulationModel.create(dataHandle.getNumRows(), 0.01)
    riskEstimator = dataHandle.getRiskEstimator(populationModel)

    risk = riskEstimator.getSampleBasedReidentificationRisk()
    return risk


def PETValidation(data, *_):
    data = loadDataFromCsv(data, StandardCharsets.UTF_8, ";")

    _applyDefinition(data)

    risk = _measureReidentificationRisk(data)
    return {"Re-identification Risk": risk.getHighestRisk()}

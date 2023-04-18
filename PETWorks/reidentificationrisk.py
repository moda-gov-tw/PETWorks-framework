from PETWorks.arx import Data, loadDataFromCsv, createJavaGateway, JavaApi
from py4j.java_collections import JavaClass

RiskModelSampleRisks = JavaClass


def _applyDefinition(data: Data, javaApi: JavaApi):
    dataHandle = data.getHandle()
    dataDefinition = data.getDefinition()

    for column in range(dataHandle.getNumColumns()):
        attributeName = data.getHandle().getAttributeName(column)
        attributeType = javaApi.AttributeType.QUASI_IDENTIFYING_ATTRIBUTE
        dataDefinition.setAttributeType(attributeName, attributeType)


def _measureReidentificationRisk(
    data: Data, javaApi: JavaApi
) -> RiskModelSampleRisks:
    dataHandle = data.getHandle()
    populationModel = javaApi.ARXPopulationModel.create(
        dataHandle.getNumRows(), 0.01
    )
    riskEstimator = dataHandle.getRiskEstimator(populationModel)

    risk = riskEstimator.getSampleBasedReidentificationRisk()
    return risk


def PETValidation(data, *_):
    javaApi = JavaApi()
    data = loadDataFromCsv(data, javaApi.StandardCharsets.UTF_8, ";", javaApi)

    _applyDefinition(data, javaApi)

    risk = _measureReidentificationRisk(data, javaApi)
    return {"Re-identification Risk": risk.getHighestRisk()}

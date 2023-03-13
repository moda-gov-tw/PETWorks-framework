from PETWorks.arx import Data, gateway, loadDataFromCsv, loadDataHierarchy
from PETWorks.attributetypes import IDENTIFIER, INSENSITIVE_ATTRIBUTE
from py4j.java_gateway import set_field
import pandas as pd

StandardCharsets = gateway.jvm.java.nio.charset.StandardCharsets
DataSubset = gateway.jvm.org.deidentifier.arx.DataSubset
HashSet = gateway.jvm.java.util.HashSet
DPresence = gateway.jvm.org.deidentifier.arx.criteria.DPresence
HashGroupifyEntry = (
    gateway.jvm.org.deidentifier.arx.framework.check.groupify.HashGroupifyEntry
)
ARXConfiguration = gateway.jvm.org.deidentifier.arx.ARXConfiguration
KAnonymity = gateway.jvm.org.deidentifier.arx.criteria.KAnonymity
ARXAnonymizer = gateway.jvm.org.deidentifier.arx.ARXAnonymizer
AttributeType = gateway.jvm.org.deidentifier.arx.AttributeType
Int = gateway.jvm.int


def _setDataHierarchies(
    data: Data, hierarchies: dict[str, list[list[str]]], attributeTypes: dict
) -> None:
    for attributeName, hierarchy in hierarchies.items():
        data.getDefinition().setAttributeType(attributeName, hierarchy)
        attributeType = attributeTypes.get(attributeName)

        if attributeType == IDENTIFIER:
            data.getDefinition().setAttributeType(
                attributeName, AttributeType.IDENTIFYING_ATTRIBUTE
            )

        if attributeType == INSENSITIVE_ATTRIBUTE:
            data.getDefinition().setAttributeType(
                attributeName, AttributeType.INSENSITIVE_ATTRIBUTE
            )


def _getQiIndices(dataHandle: str) -> list[int]:
    qiNames = dataHandle.getDefinition().getQuasiIdentifyingAttributes()
    qiIndices = []
    for qi in qiNames:
        qiIndices.append(dataHandle.getColumnIndexOf(qi))
    return qiIndices


def _isRowSuppressed(table: Data, rowIndex: int) -> bool:
    qiIndices = _getQiIndices(table.getHandle())
    for i in qiIndices:
        if table.getHandle().getValue(rowIndex, i) != "*":
            return False
    return True


def _findAnonymousLevel(hier: list[list[str]], value: str) -> int:
    for i in range(len(hier)):
        for j in range(len(hier[i])):
            if hier[i][j] == value:
                return j
    return -1


def _getAnonymizedData(
    originalData: Data, anonymizedSubset: Data,
    hierarchies: dict[str, list[list[str]]]
) -> str:
    numDataRows = anonymizedSubset.getHandle().getNumRows()

    sampleRowIndex = 1
    allSuppressed = False
    for i in range(numDataRows):
        if not _isRowSuppressed(anonymizedSubset, i):
            sampleRowIndex = i
            break
        allSuppressed = i == numDataRows - 1

    qiIndices = _getQiIndices(originalData.getHandle())

    anonymousLevels = gateway.new_array(Int, len(qiIndices))
    for i in range(len(qiIndices)):
        index = qiIndices[i]
        value = anonymizedSubset.getHandle().getValue(sampleRowIndex, index)
        attributeName = anonymizedSubset.getHandle().getAttributeName(index)
        hierarchy = hierarchies[attributeName].getHierarchy()

        if allSuppressed:
            anonymousLevels[i] = hierarchy[0].length
            continue

        anonymousLevels[i] = _findAnonymousLevel(hierarchy, value)

    arxconfig = ARXConfiguration.create()
    arxconfig.addPrivacyModel(KAnonymity(1))
    anonymizer = ARXAnonymizer()
    result = anonymizer.anonymize(originalData, arxconfig)

    lattice = result.getLattice()
    node = lattice.getNode(anonymousLevels)

    return result.getOutput(node, True)


def _getDataFrame(dataHandle: str):
    qis = dataHandle.getDefinition().getQuasiIdentifyingAttributes()
    numDataRows = dataHandle.getNumRows()

    data = []
    for i in range(numDataRows):
        row = []
        for qi in qis:
            column = dataHandle.getColumnIndexOf(qi)
            row.append(dataHandle.getValue(i, column))
        data.append(row)

    return pd.DataFrame(data, columns=qis)


def _measureDPresence(
    dataHandle: str, subset: Data,
    dMin: float, dMax: float
) -> bool:
    qisObject = dataHandle.getDefinition().getQuasiIdentifyingAttributes()
    qis = []
    for qi in qisObject:
        qis.append(qi)

    groupedData = _getDataFrame(dataHandle).groupby(qis)
    groupedSubset = _getDataFrame(subset.getHandle()).groupby(qis)

    for _, subsetGroup in groupedSubset:
        count = 0
        pcount = 0

        subsetGroupList = subsetGroup.values.tolist()
        count = len(subsetGroupList)

        for _, dataGroup in groupedData:
            dataGroupList = dataGroup.values.tolist()

            if subsetGroupList[0] == dataGroupList[0]:
                pcount = len(dataGroup)

        dummySubset = DataSubset.create(0, HashSet())
        model = DPresence(dMin, dMax, dummySubset)
        entry = HashGroupifyEntry(None, 0, 0)

        set_field(entry, "count", count)
        set_field(entry, "pcount", pcount)

        if not model.isAnonymous(None, entry):
            return False

    return True


def PETValidation(original, subset, _, dataHierarchy, **other):
    dMax = other["dMax"]
    dMin = other["dMin"]
    attributeType = other.get("attributeTypes", None)

    dataHierarchy = loadDataHierarchy(
        dataHierarchy, StandardCharsets.UTF_8, ";"
    )
    original = loadDataFromCsv(original, StandardCharsets.UTF_8, ";")
    subset = loadDataFromCsv(subset, StandardCharsets.UTF_8, ";")

    _setDataHierarchies(original, dataHierarchy, attributeType)
    _setDataHierarchies(subset, dataHierarchy, attributeType)

    anonymizedData = _getAnonymizedData(original, subset, dataHierarchy)
    dPresence = _measureDPresence(anonymizedData, subset, dMin, dMax)

    return {"dMin": dMin,
            "dMax": dMax,
            "d-presence": dPresence}

import json

import pandas as pd

import PETWorks.federatedlearning as FL
import PETWorks.reidentificationrisk as ReidentificationRisk
import PETWorks.ambiguity as Ambiguity
import PETWorks.precision as Precision
import PETWorks.nonUniformEntropy as NonUniformEntropy
import PETWorks.aecs as AECS
import PETWorks.kanonymity as KAnonymity
import PETWorks.dpresence as DPresence
import PETWorks.profitability as Profitability
import PETWorks.tcloseness as TCloseness
import PETWorks.ldiversity as LDiversity
import PETWorks.utilitybias as UtilityBias
import PETWorks.differential_privacy.SinglingOutRisk as SinglingOutRisk
import PETWorks.differential_privacy.LinkabilityRisk as LinkabilityRisk
import PETWorks.differential_privacy.InferenceRisk as InferenceRisk
import PETWorks.differential_privacy.DPMIATester as DPMIATester
import PETWorks.homomorphic_encryption as HomomorphicEncryption
import PETWorks.homomorphic_encryption.Communication as Communication
from web.generate import generateWebView

HISTORY = "images/history.png"


def dataProcess(model, gradient, tech, method, **keywordArgs):
    if tech == "FL":
        return FL.dataProcess(model, gradient, tech, method, **keywordArgs)
    elif tech == "HomomorphicEncryption":
        return HomomorphicEncryption.dataProcess(
            model, gradient, method, **keywordArgs
        )


def PETValidation(recover, origin, tech, **keywordArgs):
    if tech == "FL":
        return FL.PETValidation(recover, origin, tech, **keywordArgs)
    elif tech == "ReidentificationRisk":
        return ReidentificationRisk.PETValidation(
            recover, origin, tech, **keywordArgs
        )
    elif tech == "Ambiguity":
        return Ambiguity.PETValidation(recover, origin, tech, **keywordArgs)
    elif tech == "Precision":
        return Precision.PETValidation(recover, origin, tech, **keywordArgs)
    elif tech == "Non-Uniform Entropy":
        return NonUniformEntropy.PETValidation(
            recover, origin, tech, **keywordArgs
        )
    elif tech == "AECS":
        return AECS.PETValidation(recover, origin, tech, **keywordArgs)
    elif tech == "k-anonymity":
        return KAnonymity.PETValidation(recover, origin, tech, **keywordArgs)
    elif tech == "d-presence":
        return DPresence.PETValidation(recover, origin, tech, **keywordArgs)
    elif tech == "profitability":
        return Profitability.PETValidation(
            recover, origin, tech, **keywordArgs
        )
    elif tech == "t-closeness":
        return TCloseness.PETValidation(recover, origin, tech, **keywordArgs)
    elif tech == "l-diversity":
        return LDiversity.PETValidation(recover, origin, tech, **keywordArgs)
    elif tech == "UtilityBias":
        return UtilityBias.PETValidation(recover, origin, **keywordArgs)
    elif tech == "SinglingOutRisk":
        return SinglingOutRisk.PETValidation(recover, origin, **keywordArgs)
    elif tech == "LinkabilityRisk":
        return LinkabilityRisk.PETValidation(recover, origin, **keywordArgs)
    elif tech == "InferenceRisk":
        return InferenceRisk.PETValidation(recover, origin, **keywordArgs)
    elif tech == "TLSv1.2OrLater":
        return Communication.PETValidation(recover)
    elif tech == "DifferentialPrivacy":
        return DPMIATester.PETValidation(recover, origin)


def report(result, format):
    if format == "json":
        print(json.dumps(result, indent=4))
        return

    if format == "web":
        originPath = "images/original_image.png"
        recoverPath = "images/recovered_image.png"
        result["origin"].save(originPath)
        result["recover"].save(recoverPath)
        html = generateWebView(
            originPath, recoverPath, HISTORY, result["similarity"]
        )
        with open("output.html", "w") as f:
            f.write(html)
    return


def PETAnonymization(
    originalData,
    tech,
    dataHierarchy,
    attributeTypes,
    maxSuppressionRate,
    **keywordArgs
):
    if tech == "k-anonymity":
        anonymization = KAnonymity
    elif tech == "l-diversity":
        anonymization = LDiversity
    elif tech == "d-presence":
        anonymization = DPresence
    elif tech == "t-closeness":
        anonymization = TCloseness

    return anonymization.PETAnonymization(
        originalData,
        dataHierarchy,
        attributeTypes,
        maxSuppressionRate,
        **keywordArgs
    )


def output(data: pd.DataFrame, filePath: str) -> None:
    data.to_csv(filePath, index=False, sep=";")

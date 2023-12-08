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
import PETWorks.synthetic_data.SinglingOutRisk as SinglingOutRisk
import PETWorks.synthetic_data.LinkabilityRisk as LinkabilityRisk
import PETWorks.synthetic_data.InferenceRisk as InferenceRisk
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


def PETValidation(arg0, arg1, metric, **keywordArgs):
    if metric == "ImageSimilarity":
        return FL.PETValidation(arg0, arg1, metric, **keywordArgs)
    elif metric == "ReidentificationRisk":
        return ReidentificationRisk.PETValidation(
            arg0, arg1, metric, **keywordArgs
        )
    elif metric == "Ambiguity":
        return Ambiguity.PETValidation(arg0, arg1, metric, **keywordArgs)
    elif metric == "Precision":
        return Precision.PETValidation(arg0, arg1, metric, **keywordArgs)
    elif metric == "Non-Uniform Entropy":
        return NonUniformEntropy.PETValidation(
            arg0, arg1, metric, **keywordArgs
        )
    elif metric == "AECS":
        return AECS.PETValidation(arg0, arg1, metric, **keywordArgs)
    elif metric == "k-anonymity":
        return KAnonymity.PETValidation(arg0, arg1, metric, **keywordArgs)
    elif metric == "d-presence":
        return DPresence.PETValidation(arg0, arg1, metric, **keywordArgs)
    elif metric == "profitability":
        return Profitability.PETValidation(
            arg0, arg1, metric, **keywordArgs
        )
    elif metric == "t-closeness":
        return TCloseness.PETValidation(arg0, arg1, metric, **keywordArgs)
    elif metric == "l-diversity":
        return LDiversity.PETValidation(arg0, arg1, metric, **keywordArgs)
    elif metric == "UtilityBias":
        return UtilityBias.PETValidation(arg0, arg1, **keywordArgs)
    elif metric == "SinglingOutRisk":
        return SinglingOutRisk.PETValidation(arg0, arg1, **keywordArgs)
    elif metric == "LinkabilityRisk":
        return LinkabilityRisk.PETValidation(arg0, arg1, **keywordArgs)
    elif metric == "InferenceRisk":
        return InferenceRisk.PETValidation(arg0, arg1, **keywordArgs)
    elif metric == "TLSv1.2OrLater":
        return Communication.PETValidation(arg0)
    elif metric == "MIATest":
        return DPMIATester.PETValidation(arg0, arg1)


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

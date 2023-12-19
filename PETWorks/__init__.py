import json

import pandas as pd
from PETWorks.deidentification.config import Config

import PETWorks.federated_learning as FederatedLearning
import PETWorks.deidentification.reidentificationrisk as ReidentificationRisk
import PETWorks.deidentification.ambiguity as Ambiguity
import PETWorks.deidentification.precision as Precision
import PETWorks.deidentification.nonUniformEntropy as NonUniformEntropy
import PETWorks.deidentification.aecs as AECS
import PETWorks.deidentification.kanonymity as KAnonymity
import PETWorks.deidentification.dpresence as DPresence
import PETWorks.deidentification.profitability as Profitability
import PETWorks.deidentification.tcloseness as TCloseness
import PETWorks.deidentification.ldiversity as LDiversity
import PETWorks.deidentification.utilitybias as UtilityBias
import PETWorks.synthetic_data.SinglingOutRisk as SinglingOutRisk
import PETWorks.synthetic_data.LinkabilityRisk as LinkabilityRisk
import PETWorks.synthetic_data.InferenceRisk as InferenceRisk
import PETWorks.differential_privacy.DPMIATester as DPMIATester
import PETWorks.homomorphic_encryption as HomomorphicEncryption
import PETWorks.homomorphic_encryption.Communication as Communication
from PETWorks.federated_learning.web.generate import generateWebView

HISTORY = "images/history.png"


def dataProcess(model, gradient, tech, method, **keywordArgs):
    if tech == "FL":
        return FederatedLearning.dataProcess(
            model, gradient, tech, method, **keywordArgs
        )
    elif tech == "HomomorphicEncryption":
        return HomomorphicEncryption.dataProcess(
            model, gradient, method, **keywordArgs
        )


def loadConfig(pathToData):
    config = Config(Config.getDefaultConfigPath(pathToData))

    keywordArgs = {}
    if config.attributeTypes:
        keywordArgs["attributeTypes"] = config.attributeTypes

    if config.hierarchy is not None:
        keywordArgs["dataHierarchy"] = config.hierarchy

    return keywordArgs


def PETValidation(arg0, arg1, metric, **keywordArgs):
    if metric == "FL":
        return FederatedLearning.PETValidation(
            arg0, arg1, metric, **keywordArgs
        )
    elif metric == "ReidentificationRisk":
        return ReidentificationRisk.PETValidation(
            arg0, arg1, metric, **keywordArgs
        )
    elif metric == "Ambiguity":
        keywordArgs.update(loadConfig(arg1))
        return Ambiguity.PETValidation(arg0, arg1, metric, **keywordArgs)
    elif metric == "Precision":
        keywordArgs.update(loadConfig(arg1))
        return Precision.PETValidation(arg0, arg1, metric, **keywordArgs)
    elif metric == "Non-Uniform Entropy":
        keywordArgs.update(loadConfig(arg1))
        return NonUniformEntropy.PETValidation(
            arg0, arg1, metric, **keywordArgs
        )
    elif metric == "AECS":
        keywordArgs.update(loadConfig(arg1))
        return AECS.PETValidation(arg0, arg1, metric, **keywordArgs)
    elif metric == "k-anonymity":
        keywordArgs.update(loadConfig(arg1))
        return KAnonymity.PETValidation(arg0, arg1, metric, **keywordArgs)
    elif metric == "d-presence":
        keywordArgs.update(loadConfig(arg1))
        return DPresence.PETValidation(arg0, arg1, metric, **keywordArgs)
    elif metric == "profitability":
        keywordArgs.update(loadConfig(arg1))
        return Profitability.PETValidation(arg0, arg1, metric, **keywordArgs)
    elif metric == "t-closeness":
        keywordArgs.update(loadConfig(arg1))
        return TCloseness.PETValidation(arg0, arg1, metric, **keywordArgs)
    elif metric == "l-diversity":
        keywordArgs.update(loadConfig(arg1))
        return LDiversity.PETValidation(arg0, arg1, metric, **keywordArgs)
    elif metric == "UtilityBias":
        keywordArgs.update(loadConfig(arg1))
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
        if result.get("metric", None) == "FL":
            html = generateWebView(
                result["original"],
                result["recovered"],
                result["history"],
                result["similarity"],
            )

            with open("output.html", "w") as f:
                f.write(html)
        else:
            raise ValueError("The result does not support the web format.")
    return


def PETAnonymization(originalData, tech, maxSuppressionRate, **keywordArgs):
    keywordArgs.update(loadConfig(originalData))

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
        maxSuppressionRate,
        **keywordArgs,
    )


def output(data: pd.DataFrame, filePath: str) -> None:
    data.to_csv(filePath, index=False, sep=";")

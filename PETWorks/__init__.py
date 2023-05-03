import json

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
from web.generate import generateWebView

HISTORY = "images/history.png"


def dataProcess(model, gradient, tech, method, **keywordArgs):
    if tech == "FL":
        return FL.dataProcess(model, gradient, tech, method, **keywordArgs)


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

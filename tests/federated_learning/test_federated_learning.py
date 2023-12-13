from PETWorks.federated_learning import dataProcess, PETValidation
import os.path as path
import math


def testDataProcess(tmp_path):
    model = "data/net.pth"
    gradient = "data/grad.pt"

    recoveredData = dataProcess(
        model,
        gradient,
        "FL",
        "recover",
        iteration=3,
        outputFolder=str(tmp_path),
    )

    assert recoveredData == {
        "history": path.abspath(path.join(str(tmp_path), "history.png")),
        "recovered": path.abspath(
            path.join(str(tmp_path), "recovered_image.png")
        ),
    }
    assert path.exists(recoveredData["history"])
    assert path.exists(recoveredData["recovered"])


def testPETValidation():
    recoveredData = {
        "history": "data/history.png",
        "recovered": "data/recovered_image.png",
    }
    originalData = "data/original_image.png"

    result = PETValidation(recoveredData, originalData, "ImageSimilarity")

    result["similarity"] = math.floor(result["similarity"] * 10000) / 10000
    assert result == {
        "metric": "ImageSimilarity",
        "recovered": "data/recovered_image.png",
        "history": "data/history.png",
        "original": "data/original_image.png",
        "similarity": 0.9943,
    }

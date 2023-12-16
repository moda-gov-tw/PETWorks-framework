from PETWorks.federated_learning import dataProcess, PETValidation
import os.path as path
import math


def testDataProcess(tmp_path):
    model = "datasets/net.pth"
    gradient = "datasets/grad.pt"

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
        "history": "datasets/history.png",
        "recovered": "datasets/recovered_image.png",
    }
    originalData = "datasets/original_image.png"

    result = PETValidation(recoveredData, originalData, "FL")

    result["similarity"] = math.floor(result["similarity"] * 10000) / 10000
    assert result == {
        "metric": "FL",
        "recovered": "datasets/recovered_image.png",
        "history": "datasets/history.png",
        "original": "datasets/original_image.png",
        "similarity": 0.9943,
    }

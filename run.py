from PETWorks import dataProcess, PETValidation, report

gradient = "data/grad.pt"
model = "data/net.pth"
originalData = "images/origin.png"

recoveredData = dataProcess(model, gradient, "FL", "recover", iteration=300)
result = PETValidation(recoveredData, originalData, "FL")
report(result, "web")

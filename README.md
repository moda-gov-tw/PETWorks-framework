# PETWorks-framework

A framework for validating PET enhanced data.

Data Privacy is the keystone promoting stronger and deeper analysis of problem in our society. PET (Privacy Enhancing Technology) is a great helper for making all these happened. However, a trust-worthy and easy-to-use validation tool for PET is still rare. 

Here we provide a framework dealing with the validation problem of PET enhanced data.

## How it works?

| Module                    | Description                                                                                                                           |
|---------------------------|---------------------------------------------------------------------------------------------------------------------------------------|
| PET Enhanced Data Process | This module aims to load and process (e.g. recover) PET-enhanced data accordingly to the data and the PET it used.                    |                                                                                                                                       |
| PET Validation            | This module has validation methodologies built in. Returning the result of the validation.                                            |
| Report                    | This module handles the output format of the report.  It could be text-based on the terminal or GUI-based showing on the web browser. |

## How to install

#### System Requirements:
- Python 3.8 or higher
- Java 8 or higher

#### Installation Instructions:
To install, open a terminal in the directory and enter the following command:

```
pip install -r requirement.txt
```

## APIs

- [k-anonymity](docs/source/k-anonymity.rst)
    - Average Equivalence Class Size
    - Ambiguity
    - d-presence
    - k-anonymity
    - l-diversity
    - Non-Uniform Entropy
    - Precision
    - Profitability
    - t-closeness
    - Utility Bias
    - De-identification for d-presence
    - De-identification for k-anonymity
    - De-identification for l-diversity
    - De-identification for t-closeness
- [Differential Privacy](docs/source/differential_privacy.rst)
    - Man-in-the-Middle Attack
- [Federated Learning](docs/source/federated_learning.rst)
    - Federated Learning Validation With Tamarin Prover
- [Homomorphic Encryption](docs/source/homomorphic_encryption.rst)
    - Testing Method for Homomorphic Encryption Technology
- [Synthetic Data](docs/source/syntehtic_data.rst)
    - Singling Out Attack
    - Inference Attack
    - Linkalility Attack



## Showcase

### Federated Learning

#### Validate Data With the Image Similarity

```python
from PETWorks import dataProcess, PETValidation, report

gradient = "datasets/grad.pt"
model = "datasets/net.pth"
originalData = "datasets/original_image.png"

recoveredData = dataProcess(model, gradient, "FL", "recover")
result = PETValidation(recoveredData, originalData, "ImageSimilarity")
report(result, "web")
```                     

#### Web Report

Here is the showcase of the web report.

![](https://i.imgur.com/p9wE8BP.png)

The web report also shows the process of recovery.

![](https://i.imgur.com/tCtVqBu.png)

### Current Status
This project is now maintained by Telecom Technology Center, Taiwan. We're now providing just a really simple showcase demonstrating how we can use this framework to validate PET protection of the data using the technology of federated learning. We still need plenty of implementation for every module. This is a very early stage project. Stay tuned!  

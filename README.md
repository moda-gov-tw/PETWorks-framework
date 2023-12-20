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

## How to install?

#### System Requirements:
- Python 3.8 or later
- Java 8 or later

#### Installation Instructions:
To install, open a terminal in the directory and enter the following command:

```
pip install -r requirement.txt
```

## APIs

- **Traditional De-identification Technologies**
    - [Average Equivalence Class Size](https://petworks-doc.readthedocs.io/en/latest/k-anonymity.html#average-equivalence-class-size)
    - [Ambiguity](https://petworks-doc.readthedocs.io/en/latest/k-anonymity.html#ambiguity)
    - [d-presence](https://petworks-doc.readthedocs.io/en/latest/k-anonymity.html#d-presence)
    - [k-anonymity](https://petworks-doc.readthedocs.io/en/latest/k-anonymity.html#k-anonymity)
    - [l-diversity](https://petworks-doc.readthedocs.io/en/latest/k-anonymity.html#l-diversity)
    - [Non-Uniform Entropy](https://petworks-doc.readthedocs.io/en/latest/k-anonymity.html#non-uniform-entropy)
    - [Precision](https://petworks-doc.readthedocs.io/en/latest/k-anonymity.html#precision)
    - [Profitability](https://petworks-doc.readthedocs.io/en/latest/k-anonymity.html#profitability)
    - [t-closeness](https://petworks-doc.readthedocs.io/en/latest/k-anonymity.html#t-closeness)
    - [Utility Bias](https://petworks-doc.readthedocs.io/en/latest/k-anonymity.html#utility-bias)
    - [De-identification for d-presence](https://petworks-doc.readthedocs.io/en/latest/k-anonymity.html#de-identification-for-d-presence)
    - [De-identification for k-anonymity](https://petworks-doc.readthedocs.io/en/latest/k-anonymity.html#de-identification-for-k-anonymity)
    - [De-identification for l-diversity](https://petworks-doc.readthedocs.io/en/latest/k-anonymity.html#de-identification-for-l-diversity)
    - [De-identification for t-closeness](https://petworks-doc.readthedocs.io/en/latest/k-anonymity.html#de-identification-for-t-closeness)
- **Differential Privacy**
    - [Man-in-the-Middle Attack](https://petworks-doc.readthedocs.io/en/latest/differential_privacy.html#man-in-the-middle-attack)
- **Federated Learning**
    - [Federated Learning Validation With Tamarin Prover](https://petworks-doc.readthedocs.io/en/latest/federated_learning.html#federated-learning-validation-with-tamarin-prover)
    - [Validate Data With the Image Similarity](https://petworks-doc.readthedocs.io/en/latest/federated_learning.html#validate-data-with-the-image-similarity)
- **Homomorphic Encryption**
    - [Testing Method for Homomorphic Encryption Technology](https://petworks-doc.readthedocs.io/en/latest/homomorphic_encryption.html#testing-method-for-homomorphic-encryption-technology)
    - [Generate Key for Homomorphic Encryption](https://petworks-doc.readthedocs.io/en/latest/homomorphic_encryption.html#generate-key-for-homomorphic-encryption)
    - [Encrypt Value Using Homomorphic Encryption](https://petworks-doc.readthedocs.io/en/latest/homomorphic_encryption.html#encrypt-value-using-homomorphic-encryption)
    - [Decrypt Value Using Homomorphic Encryption](https://petworks-doc.readthedocs.io/en/latest/homomorphic_encryption.html#decrypt-value-using-homomorphic-encryption)
    - [Detect the Use of TLS Protocol (v1.2 or later)](https://petworks-doc.readthedocs.io/en/latest/homomorphic_encryption.html#detect-the-use-of-tls-protocol-v1-2-or-later)
    - [Find External Functions](https://petworks-doc.readthedocs.io/en/latest/homomorphic_encryption.html#find-external-functions)
- **Synthetic Data**
    - [Singling Out Attack](https://petworks-doc.readthedocs.io/en/latest/syntehtic_data.html#singling-out-attack)
    - [Inference Attack](https://petworks-doc.readthedocs.io/en/latest/syntehtic_data.html#inference-attack)
    - [Linkalility Attack](https://petworks-doc.readthedocs.io/en/latest/syntehtic_data.html#linkalility-attack)



## Showcase

### Validate the Federated Learning Enhanced Data

```python
from PETWorks import dataProcess, PETValidation, report

gradient = "datasets/grad.pt"
model = "datasets/net.pth"
originalData = "datasets/original_image.png"

recoveredData = dataProcess(model, gradient, "FL", "recover")
result = PETValidation(recoveredData, originalData, "FL")
report(result, "web")
```                     

### Web Report

Here is the showcase of the web report.

![](https://i.imgur.com/p9wE8BP.png)

The web report also shows the process of recovery.

![](https://i.imgur.com/tCtVqBu.png)

### Current Status
This project is now maintained by Telecom Technology Center, Taiwan. We're now providing just a really simple showcase demonstrating how we can use this framework to validate PET protection of the data using the technology of federated learning. We still need plenty of implementation for every module. This is a very early stage project. Stay tuned!  

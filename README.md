# PETWorks-framework

A framework for validating PET enhanced data.

Data Privacy is the keystone promoting stronger and deeper analysis of problem in our society. PET (Privacy Enhancing Technology) is a great helper for making all these happened. However, a trust-worthy and easy-to-use validation tool for PET is still rare. 

Here we provide a framework dealing with the validation problem of PET enhanced data.

## Showcase

### Traditional De-identification Technologies

#### Measurement of the Re-Identification Risk

```python
from PETWorks import PETValidation, report

originalData = "data/deidentifiedData.csv"

result = PETValidation(originalData, None, "ReidentificationRisk")
report(result, "json")
```

Execution Result

```bash
{
    "Re-identification Risk": 1.0
}
```

#### Measurement of the Ambiguity Metric

```python
from PETWorks import PETValidation, report
from PETWorks.attributetypes import QUASI_IDENTIFIER, SENSITIVE_ATTRIBUTE

originalData = "data/adult.csv"
anonymizedData = "data/adult_anonymized.csv"
dataHierarchy = "data/adult_hierarchy"

attributeTypes = {
    "age": QUASI_IDENTIFIER,
    "education": QUASI_IDENTIFIER,
    "marital-status": QUASI_IDENTIFIER,
    "native-country": QUASI_IDENTIFIER,
    "occupation": QUASI_IDENTIFIER,
    "race": QUASI_IDENTIFIER,
    "salary-class": QUASI_IDENTIFIER,
    "sex": QUASI_IDENTIFIER,
    "workclass": SENSITIVE_ATTRIBUTE,
}

result = PETValidation(
    originalData, anonymizedData,
    "Ambiguity",
    dataHierarchy=dataHierarchy,
    attributeTypes=attributeTypes
)
report(result, "json")
```

Execution Result

```bash
$ python3 ambiguity.py
{
    "ambiguity": 0.72714009672634
}
```

#### Measurement of the Precision Metric

```python
from PETWorks import PETValidation, report
from PETWorks.attributetypes import QUASI_IDENTIFIER, SENSITIVE_ATTRIBUTE

originalData = "data/adult.csv"
anonymizedData = "data/adult_anonymized.csv"
dataHierarchy = "data/adult_hierarchy"

attributeTypes = {
    "age": QUASI_IDENTIFIER,
    "education": QUASI_IDENTIFIER,
    "marital-status": QUASI_IDENTIFIER,
    "native-country": QUASI_IDENTIFIER,
    "occupation": QUASI_IDENTIFIER,
    "race": QUASI_IDENTIFIER,
    "salary-class": QUASI_IDENTIFIER,
    "sex": QUASI_IDENTIFIER,
    "workclass": SENSITIVE_ATTRIBUTE,
}

result = PETValidation(
    originalData, anonymizedData,
    "Precision",
    dataHierarchy=dataHierarchy,
    attributeTypes=attributeTypes
)
report(result, "json")
```

Execution Result
```bash
$ python3 precision.py
{
    "precision": 0.7271401100722763
}
```


#### Measurement of the Non-Uniform Entropy Metric

```python
from PETWorks import PETValidation, report
from PETWorks.attributetypes import QUASI_IDENTIFIER, SENSITIVE_ATTRIBUTE

originalData = "data/adult.csv"
anonymizedData = "data/adult_anonymized.csv"
dataHierarchy = "data/adult_hierarchy"

attributeTypes = {
    "age": QUASI_IDENTIFIER,
    "education": QUASI_IDENTIFIER,
    "marital-status": QUASI_IDENTIFIER,
    "native-country": QUASI_IDENTIFIER,
    "occupation": QUASI_IDENTIFIER,
    "race": QUASI_IDENTIFIER,
    "salary-class": QUASI_IDENTIFIER,
    "sex": QUASI_IDENTIFIER,
    "workclass": SENSITIVE_ATTRIBUTE,
}

result = PETValidation(
    originalData, anonymizedData,
    "Non-Uniform Entropy",
    dataHierarchy=dataHierarchy,
    attributeTypes=attributeTypes
)
report(result, "json")
```

Execution Result
```python
$ python nonUniformEntropy.py
{
    "Non-Uniform Entropy": 0.6740002378300514
}
```

#### Measurement of the AECS Metric

```python
from PETWorks import PETValidation, report
from PETWorks.attributetypes import QUASI_IDENTIFIER, SENSITIVE_ATTRIBUTE

originalData = "data/adult.csv"
anonymizedData = "data/adult_anonymized.csv"

attributeTypes = {
    "age": QUASI_IDENTIFIER,
    "education": QUASI_IDENTIFIER,
    "marital-status": QUASI_IDENTIFIER,
    "native-country": QUASI_IDENTIFIER,
    "occupation": QUASI_IDENTIFIER,
    "race": QUASI_IDENTIFIER,
    "salary-class": QUASI_IDENTIFIER,
    "sex": QUASI_IDENTIFIER,
    "workclass": SENSITIVE_ATTRIBUTE,
}

result = PETValidation(
    originalData, anonymizedData,
    "AECS",
    attributeTypes=attributeTypes
)
report(result, "json")
```

Execution Result
```python
$ python aecs.py
{
    "AECS": 0.9992707253704929
}
```

#### Compute the k-anonymity

```python
from PETWorks import PETValidation, report
from PETWorks.attributetypes import QUASI_IDENTIFIER

anonymizedData = "data/adult_anonymized.csv"

attributeTypes = {
    "age": QUASI_IDENTIFIER,
    "sex": QUASI_IDENTIFIER,
}

result = PETValidation(
        None, anonymizedData, "k-anonymity", attributeTypes=attributeTypes, k=6
)
report(result, "json")
```

Execution Result
```python
$ python3 k-anonymity.py
{
    "k": 6,
    "k-anonymity": true
}
```


#### Compute the δ-presence
```python
from PETWorks import PETValidation, report
from PETWorks.attributetypes import SENSITIVE_ATTRIBUTE, QUASI_IDENTIFIER


origin = "data/delta.csv"
anonymized = "data/delta_anonymized.csv"
dataHierarchy = "data/delta_hierarchy"

attributeTypes = {
    "zip": QUASI_IDENTIFIER,
    "age": QUASI_IDENTIFIER,
    "nationality": QUASI_IDENTIFIER,
    "salary-class": SENSITIVE_ATTRIBUTE
}

result = PETValidation(
        origin, anonymized, "d-presence", dataHierarchy=dataHierarchy, attributeTypes=attributeTypes, dMin=1/2, dMax=2/3
    )
report(result, "json")
```

Execution Result
```python
$ python3 d-presence.py
{
    "dMin": 0.5,
    "dMax": 0.6666666666666666,
    "d-presence": true
}
```


#### Compute the Profitability
```python
from PETWorks import PETValidation, report
from PETWorks.attributetypes import QUASI_IDENTIFIER, INSENSITIVE_ATTRIBUTE

origin = "data/delta.csv"
anonymized = "data/delta_anonymized.csv"
dataHierarchy = "data/delta_hierarchy"

attributeTypes = {
    "zip": QUASI_IDENTIFIER,
    "age": QUASI_IDENTIFIER,
    "nationality": QUASI_IDENTIFIER,
    "salary-class": INSENSITIVE_ATTRIBUTE
}

result = PETValidation(
    origin,
    anonymized,
    "profitability",
    dataHierarchy=dataHierarchy,
    attributeTypes=attributeTypes,
    allowAttack=True,
    adversaryCost=4,
    adversaryGain=300,
    publisherLost=300,
    publisherBenefit=1200
)
report(result, "json")
```

Execution Result
```python
$ python3 profitability.py
{
    "allow attack": true,
    "adversary's cost": 4,
    "adversary's gain": 300,
    "publisher's loss": 300,
    "publisher's benefit": 1200,
    "isProfitable": true
}
```


#### Compute the l-diversity
```python
from PETWorks import PETValidation, report
from PETWorks.attributetypes import SENSITIVE_ATTRIBUTE, QUASI_IDENTIFIER

anonymized = "data/inpatient_anonymized.csv"

attributeTypes = {
    "zipcode": QUASI_IDENTIFIER,
    "age": QUASI_IDENTIFIER,
    "nationality": QUASI_IDENTIFIER,
    "condition": SENSITIVE_ATTRIBUTE
}

result = PETValidation(
    None, anonymized, "l-diversity", attributeTypes=attributeTypes, l=3
)
report(result, "json")
```

Execution Result
```
$ python3 l-diversity.py
{
    "l": 3,
    "fulfill l-diversity": true
}
```

#### Compute the t-closeness

```python
from PETWorks import PETValidation, report
from PETWorks.attributetypes import (
    SENSITIVE_ATTRIBUTE,
    QUASI_IDENTIFIER,
)

anonymized = "data/patient_anonymized.csv"
dataHierarchy = "data/patient_hierarchy"

attributeTypes = {
    "ZIPCode": QUASI_IDENTIFIER,
    "Age": QUASI_IDENTIFIER,
    "Disease": SENSITIVE_ATTRIBUTE,
}

result = PETValidation(
    None,
    anonymized,
    "t-closeness",
    dataHierarchy=dataHierarchy,
    attributeTypes=attributeTypes,
    tLimit=0.376,
)
report(result, "json")
```

Execution Result

```  
$ python3 t-closeness.py
{
    "t": 0.376,
    "fulfill t-closeness": true
}
```

#### Compute the utility bias

```python
from PETWorks import PETValidation, report
import pandas as pd

origin = "data/presence.csv"
anonymized = "data/presence_anonymized2.csv"


def averageAge(source):
    data = pd.read_csv(source, sep=";")
    return data["age"].mean()


result = PETValidation(
    origin, anonymized, "UtilityBias", processingFunc=averageAge, maxBias=2
)
report(result, "json")
```

Execution Result

```  
$ python3 utilityBias.py
{
    "UtilityBias": true
}
```

#### Anonymize with the k-anonymity

```python
from PETWorks import PETAnonymization, output
from PETWorks.attributetypes import *

originalData = "data/adult.csv"
dataHierarchy = "data/adult_hierarchy"

attributeTypes = {
    "age": QUASI_IDENTIFIER,
    "sex": QUASI_IDENTIFIER,
}

result = PETAnonymization(
    originalData,
    "k-anonymity",
    dataHierarchy,
    attributeTypes,
    maxSuppressionRate=0.6,
    k=6,
)

output(result, "output.csv")
```

#### Anonymize with the δ-presence

```python
from PETWorks import PETAnonymization, output
from PETWorks.attributetypes import *

originalData = "data/adult.csv"
dataHierarchy = "data/adult_hierarchy"
subsetData = "data/adult10.csv"

attributeTypes = {
    "age": QUASI_IDENTIFIER,
    "race": QUASI_IDENTIFIER,
}

result = PETAnonymization(
    originalData,
    "d-presence",
    dataHierarchy,
    attributeTypes,
    maxSuppressionRate=0.6,
    dMin=0.0,
    dMax=0.8,
    subsetData=subsetData,
)

output(result, "output.csv")
```

#### Anonymize with the l-diversity

```python
from PETWorks import PETAnonymization, output
from PETWorks.attributetypes import *

originalData = "data/adult.csv"
dataHierarchy = "data/adult_hierarchy"

attributeTypes = {
    "age": QUASI_IDENTIFIER,
    "race": QUASI_IDENTIFIER,
    "workclass": SENSITIVE_ATTRIBUTE,
}

result = PETAnonymization(
    originalData,
    "l-diversity",
    dataHierarchy,
    attributeTypes,
    maxSuppressionRate=0.6,
    l=6,
)

output(result, "output.csv")
```

#### Anonymize with the t-closeness

```python
from PETWorks import PETAnonymization, output
from PETWorks.attributetypes import *

originalData = "data/adult.csv"
dataHierarchy = "data/adult_hierarchy"

attributeTypes = {
    "age": QUASI_IDENTIFIER,
    "race": QUASI_IDENTIFIER,
    "workclass": SENSITIVE_ATTRIBUTE,
}

result = PETAnonymization(
    originalData,
    "t-closeness",
    dataHierarchy,
    attributeTypes,
    maxSuppressionRate=0.6,
    t=6,
)

output(result, "output.csv")
```

### Differential Privacy

#### Validate Data With the Man-in-the-Middle Attack Test

```python
from PETWorks import PETValidation, report

synthetic = "data/synthetic_NHANES.csv"
original = "data/NHANES.csv"

result = PETValidation(synthetic, original, "MIATest")
report(result, "json")
```

Execution Result
```bash
$ python3 validateDP.py
{
    "Does the data processed with differential privacy": "Possibly Yes"
}
```

### Synthetic Data

#### Measurement of the Singling Out Risk

```python
from PETWorks import PETValidation, report

synthetic = "data/adults_syn_ctgan.csv"
original = "data/adults_train.csv"
control = "data/adults_control.csv"

result = PETValidation(synthetic, original, "SinglingOutRisk", control=control)
report(result, "json")
```

Execution Result
```bash
$ python3 singlingOutRisk.py
{
    "Success rate of main attack": 0.2110980494620957,
    "Success rate of baseline attack": 0.037756879139353126,
    "Success rate of control attack": 0.06360101455367315
}
```

#### Measurement of the Inference Risk

```python
from PETWorks import PETValidation, report

synthetic = "data/adults_syn_ctgan.csv"
original = "data/adults_train.csv"
control = "data/adults_control.csv"

result = PETValidation(synthetic, original, "InferenceRisk", control=control)
report(result, "json")
```

Execution Result
```bash
$ python3 inferenceRisk.py
{
    "age": {
        "Success rate of main attack": 0.07961489208090426,
        "Success rate of baseline attack": 0.06666463994121648,
        "Success rate of control attack": 0.06865698642424536
    },
    "type_employer": {
        "Success rate of main attack": 0.48107270841122557,
        "Success rate of baseline attack": 0.4561683773733644,
        "Success rate of control attack": 0.48107270841122557
    },
    "fnlwgt": {
        "Success rate of main attack": 0.03877178917881202,
        "Success rate of baseline attack": 0.05570673428455759,
        "Success rate of control attack": 0.05570673428455759
    }
}
```

#### Measurement of the Linkability Risk

```python
from PETWorks import PETValidation, report

synthetic = "data/adults_syn_ctgan.csv"
original = "data/adults_train.csv"
control = "data/adults_control.csv"

auxiliaryColumns = [
    ["type_employer", "fnlwgt"],
    ["age"]
]

result = PETValidation(
    synthetic,
    original,
    "LinkabilityRisk",
    control=control,
    auxiliaryColumns=auxiliaryColumns,
)
report(result, "json")
```

Execution Result
```bash
$ python3 linkabilityRisk.py
{
    "Success rate of main attack": 0.001956606593345214,
    "Success rate of baseline attack": 0.004451813975142082,
    "Success rate of control attack": 0.0029546895460639613
}
```

### Federated Learning

#### Validate the Federated Learning Protocol Design

Please refer [here](https://petworks-doc.readthedocs.io/en/latest/tamarin.html) to validate the protocol design with Tamarin Prover.

#### Validate Data With the Image Similarity

```python
from PETWorks import dataProcess, PETValidation, report

gradient = "/home/Doc/gradient"
model = "/home/Doc/model"
originalData = "/home/Doc/o.png"

recoveredData = dataProcess(model, gradient, "FL", "recover")
result = PETValidation(recoveredData, originalData, "ImageSimilarity")
report(result, "web")
```

### Homomorphic Encryption

#### Generate Key for Homomorphic Encryption

```python
from PETWorks import dataProcess, report

library = "phe"
keySize = 128

keys = dataProcess(
    keySize, None, "HomomorphicEncryption", "GenerateKey", library=library
)
report(keys, "json")
```

Execution Result
```bash
$ python3 generateKey.py
{
    "Public Key": 176498358747162177292711947860102193361,
    "Private Key": {
        "p": 10056745993628924791,
        "q": 17550245264121825271
    }
}
```

#### Encrypt Value Using Homomorphic Encryption

```python
from PETWorks import dataProcess, report

library = "phe"
keySize = 128
publicKey = 240537853022521961474293276399056393697

value = 16

encryptedValue = dataProcess(
    value,
    keySize,
    "HomomorphicEncryption",
    "Encrypt",
    library=library,
    publicKey=publicKey,
)
report(encryptedValue, "json")
```

Execution Result
```bash
$ python3 encryptValue.py
{
    "Encrypted Value": 21895940939293354723904335349274645110736347403968508239398892528574591099866
}
```

#### Decrypt Value Using Homomorphic Encryption

```python
from PETWorks import dataProcess, report

library = "phe"
keySize = 128
publicKey = 240537853022521961474293276399056393697
privateKey = {"p": 15077889811522283831, "q": 15953018361939928487}

encryptedValue = 54460907148015048399650723031319333758655292473353853450480678347318563444904

decryptedValue = dataProcess(
    encryptedValue,
    keySize,
    "HomomorphicEncryption",
    "Decrypt",
    library=library,
    publicKey=publicKey,
    privateKey=privateKey,
)
report(decryptedValue, "json")
```

Execution Result
```bash
$ python3 decryptValue.py
{
    "Decrypted Value": 16
}
```

#### Detect the Use of TLS Protocol (v1.2 or later) 

```python
from PETWorks import dataProcess, PETValidation, report

packets = dataProcess(None, None, "HomomorphicEncryption", "CapturePackets")
result = PETValidation(packets, None, "TLSv1.2OrLater")
report(result, "json")
```

Execution Result
```bash
$ python3 detectTLS.py
{
    "Use TLS v1.2 or later": true
}
```

#### Find External Functions

```python
from PETWorks import dataProcess, report

executable = "/usr/bin/ls"

result = dataProcess(
    executable, None, "HomomorphicEncryption", "FindExternalFunctions"
)
report(result, "json")

```

Execution Result
```bash
$ python3 findExternalFunctions.py
{
    "External Functions": [
        "abort@GLIBC_2.2.5",
        "__assert_fail@GLIBC_2.2.5",
        "bindtextdomain@GLIBC_2.2.5",
        ...
    ]
}
```


### How it works?
| Module                    | Description                                                                                                                           |
|---------------------------|---------------------------------------------------------------------------------------------------------------------------------------|
| PET Enhanced Data Process | This module aims to load and process (e.g. recover) PET-enhanced data accordingly to the data and the PET it used.                    |                                                                                                                                       |
| PET Validation            | This module has validation methodologies built in. Returning the result of the validation.                                            |
| Report                    | This module handles the output format of the report.  It could be text-based on the terminal or GUI-based showing on the web browser. |

#### Web Report

Here is the showcase of the web report.

![](https://i.imgur.com/p9wE8BP.png)

The web report also shows the process of recovery.

![](https://i.imgur.com/tCtVqBu.png)

### Current Status
This project is now maintained by Telecom Technology Center, Taiwan. We're now providing just a really simple showcase demonstrating how we can use this framework to validate PET protection of the data using the technology of federated learning. We still need plenty of implementation for every module. This is a very early stage project. Stay tuned!  

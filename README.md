# PETWorks-framework

A framework for validating PET enhanced data.

Data Privacy is the keystone promoting stronger and deeper analysis of problem in our society. PET (Privacy Enhancing Tool) is a great helper for making all these happened. However, a trust-worthy and easy-to-use validation tool for PET is still rare. 

Here we provide a framework dealing with the validation problem of PET enhanced data.


### Showcase
Validation of data processed with federated learning.

```python
from PETWorks import dataRecover, PETValidation

gradient = "/home/Doc/gradient"
model = "/home/Doc/model"
originalData = "/home/Doc/o.png"

recoveredData = dataRecover(model, gradient, "FL")
report = PETValidation(recoveredData, originalData, "FL")
print(report)
```

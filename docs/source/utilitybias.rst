++++++++++++
Utility Bias
++++++++++++

The following code snippet assesses whether the data satisfies the utility bias.

We use ``data/presence.csv`` as the original data and ``data/presence_anonymized2.csv`` as the anonymized data to demonstrate how to evaluate this metric through PETWorks-framework.

In the following code snippet, we use the API ``PETValidation(origin, anonymized, "UtilityBias", processingFunc, maxBias)`` with the original data, the anonymized data, the string "UtilityBias," the processing function, and the maximal acceptable bias to determine whether the data satisfies the utility bias.

Then, we use the API ``report(result, format)`` with the evaluation result and the string "json" as parameters to print the evaluation result in JSON format.

Example: utilityBias.py
-------------------------

.. code-block:: python

    from PETWorks import PETValidation, report
    import pandas as pd

    origin = "datasets/presence/presence.csv"
    anonymized = "datasets/presence/presence_anonymized2.csv"


    def averageAge(source):
        data = pd.read_csv(source, sep=";")
        return data["age"].mean()


    result = PETValidation(
        origin, anonymized, "UtilityBias", processingFunc=averageAge, maxBias=2
    )
    report(result, "json")

Execution Result
------------------

.. code-block:: text
    
    $ python3 utilityBias.py
    {
        "UtilityBias": true
    }

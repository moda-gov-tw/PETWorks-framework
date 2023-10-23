+++++++++++++++++++++++++++++++++++++++
Precision
+++++++++++++++++++++++++++++++++++++++

The following code snippet evaluate the precision [1]_.

We use ``data/adult.csv`` as the original data, ``data/adult_anonymized.csv`` as the anonymized data, and ``data/adult_hierarchy`` as the data hierarchy to demonstrate how to evaluate this indicator through PETWorks-framework.

In the following code snippet, we use the API ``PETValidation(original, anonymized, tech, dataHierarchy)`` with the data and the string “Precision” as the parameters to evaluate the precision.

Then, we use the API ``report(result, format)`` with the evaluation result and the string "json" as parameters to print the evaluation result in JSON format.

Example: precision.py
------------------------

.. code-block:: python

    from PETWorks import PETValidation, report

    originalData = "data/adult.csv"
    anonymizedData = "data/adult_anonymized.csv"
    dataHierarchy = "data/adult_hierarchy"

    result = PETValidation(
        originalData, anonymizedData, "Precision", dataHierarchy=dataHierarchy
    )
    report(result, "json")

Execution Result
------------------

.. code-block:: bash

    $ python3 precision.py
    {
        "precision": 0.7271401100722763
    }

Reference
-----------

.. [1] L. SWEENEY, “ACHIEVING k-ANONYMITY PRIVACY PROTECTION USING GENERALIZATION AND SUPPRESSION.” International Journal of Uncertainty, Fuzziness and Knowledge-Based Systems, vol. 10, no. 5, pp. 571-588, 2002, doi: 10.1142/s021848850200165x.

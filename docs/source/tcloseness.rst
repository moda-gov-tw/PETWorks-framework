+++++++++++++++++++++++++++++++++++++++
t-closeness
+++++++++++++++++++++++++++++++++++++++

The following code snippet assesses whether the data satisfies t-closeness [1]_。

We use ``data/patient_anonymized.csv`` as the anonymized data, ``data/patient_hierarchy`` as the data hierarchy, and ``attributeTypes`` as the attribute type definitions to demonstrate how to evaluate this indicator through PETWorks-framework.

In the following code snippet, we use the API ``PETValidation(None, anonymized, "t-closeness", dataHierarchy, attributeTypes, tLimit)`` with the data, the string “t-closeness,” and the variables tLimit as parameters to determine whether the data satisfies t-closeness.

Then, we use the API ``report(result, format)`` with the evaluation result and the string "json" as parameters to print the evaluation result in JSON format.

Example: t-closeness.py
--------------------------

.. code-block:: python

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


Execution Result
------------------

.. code-block:: text
    
    $ python3 t-closeness.py
    {
        "t": 0.376,
        "fulfill t-closeness": true
    }

Reference
-----------
.. [1] N. Li, T. Li and S. Venkatasubramanian, “t-Closeness: Privacy Beyond k-Anonymity and l-Diversity,” 2007 IEEE 23rd International Conference on Data Engineering, Istanbul, Turkey, 2007, pp. 106-115, doi: 10.1109/ICDE.2007.367856.

++++++++++++
l-diversity
++++++++++++

The following code snippet assesses whether the data satisfies :math:`l`-diversity [1]_.

We use ``data/inpatient_anonymized.csv`` as the anonymized data and ``attributeTypes`` as the attribute type definitions to demonstrate how to evaluate this indicator through PETWorks-framework.

In the following code snippet, we use the API ``PETValidation(None, anonymized, "l-diversity", attributeTypes, l)`` with the data, the string "l-diversity", and the l value as parameters to determine whether the data satisfies :math:`l`-diversity.

Then, we use the API ``report(result, format)`` with the evaluation result and the string "json" as parameters to print the evaluation result in JSON format.

Example: l-diversity.py
-------------------------

.. code-block:: python

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

Execution Result
------------------

.. code-block:: text
    
    $ python3 l-diversity.py
    {
        "l": 3,
        "fulfill l-diversity": true
    }

Reference
---------
.. [1] A. Machanavajjhala, J. Gehrke, D. Kifer, and M. Venkitasubramaniam, L-diversity: privacy beyond k-anonymity. 2006. doi: 10.1109/icde.2006.1.

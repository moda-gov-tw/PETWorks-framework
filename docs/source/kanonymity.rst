+++++++++++++++++++++++++++++++++++++++
k-anonymity
+++++++++++++++++++++++++++++++++++++++

The following code snippet assesses whether the data satisfies k-anonymity [1]_。

We use ``data/adult_anonymized.csv`` as the anonymized data and ``attributeTypes`` as the attribute type definitions to demonstrate the evaluation of this indicator through PETWorks-Framework.

In the following code snippet, we use the API ``PETValidation(None, anonymized, tech, attributeTypes, k)`` with the data, the string "k-anonymity", and the k value as parameters to determine whether the data satisfies k-anonymity.

Then, we use the API ``report(result, format)`` with the evaluation result and the string "json" as parameters to print the evaluation result in JSON format.


Example: k-anonymity.py
---------------------------

.. code-block:: python

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

Execution Result
------------------

.. code-block:: text

    $ python3 k-anonymity.py
    {
        "k": 6,
        "k-anonymity": true
    }

Reference
-----------

.. [1] L. Sweeney, “K-anonymity: A model for protecting privacy,” International Journal of Uncertainty, Fuzziness and Knowledge-Based Systems, vol. 10, no. 05, pp. 557–570, 2002. 
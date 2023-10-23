+++++++++++++++++++++++++++++++++++++++
Profitability
+++++++++++++++++++++++++++++++++++++++

The following code snippet assesses whether the data satisfies profitability [1]_.

We use ``data/delta.csv`` as the original data, ``data/delta_anonymized.csv`` as the anonymized data, ``data/delta_hierarchy`` as the data hierarchy, and ``attributeTypes`` as the attribute type definitions to demonstrate how to evaluate this indicator through PETWorks-framework.

In the following code snippet, we use the API ``PETValidation(origin, anonymized, "profitability", dataHierarchy, attributeTypes, allowAttack, adversaryCost, adversaryGain, publisherLost, publisherBenefit)`` with the data, the string “profitability", the variables allowAttack, adversaryCost, adversaryGain, publisherLost, and publisherBenefit as the parameters to determine whether the data satisfies profitability.

Then, we use the API ``report(result, format)`` with the evaluation result and the string "json" as parameters to print the evaluation result in JSON format.

Example: profitability.py
-----------------------------

.. code-block:: python

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


Execution Result
------------------

.. code-block:: text
    
    $ python3 profitability.py
    {
        "allow attack": true,
        "adversary's cost": 4,
        "adversary's gain": 300,
        "publisher's loss": 300,
        "publisher's benefit": 1200,
        "profitability": true
    }

Reference
-----------
.. [1] Z. Wan et al., “A Game Theoretic Framework for Analyzing Re-Identification Risk,” PLOS ONE, vol. 10, no. 3, p. e0120592, Mar. 2015, doi: 10.1371/journal.pone.0120592.

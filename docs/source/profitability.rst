+++++++++++++++++++++++++++++++++++++++
Profitability
+++++++++++++++++++++++++++++++++++++++

The following code snippet assesses whether the data satisfies profitability [1]_.

We use ``data/delta/delta.csv`` as the original data, ``data/delta/delta_anonymized.csv`` as the anonymized data, and the data hierarchy, ``data/delta/delta_hierarchy``, and the attribute type definitions in ``data/adult/adult_anonymized.yaml`` to demonstrate how to evaluate this metric through PETWorks-framework.

In the following code snippet, we use the API ``PETValidation(origin, anonymized, "profitability", allowAttack, adversaryCost, adversaryGain, publisherLost, publisherBenefit)`` with the data, the string “profitability", the variables allowAttack, adversaryCost, adversaryGain, publisherLost, and publisherBenefit as the parameters to determine whether the data satisfies profitability.

Then, we use the API ``report(result, format)`` with the evaluation result and the string "json" as parameters to print the evaluation result in JSON format.

Example: profitability.py
-----------------------------

.. code-block:: python

    from PETWorks import PETValidation, report

    origin = "data/delta/delta.csv"
    anonymized = "data/delta/delta_anonymized.csv"

    result = PETValidation(
        origin,
        anonymized,
        "profitability",
        allowAttack=True,
        adversaryCost=4,
        adversaryGain=300,
        publisherLost=300,
        publisherBenefit=1200,
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
        "isProfitable": true
    }

Reference
-----------
.. [1] Z. Wan et al., “A Game Theoretic Framework for Analyzing Re-Identification Risk,” PLOS ONE, vol. 10, no. 3, p. e0120592, Mar. 2015, doi: 10.1371/journal.pone.0120592.

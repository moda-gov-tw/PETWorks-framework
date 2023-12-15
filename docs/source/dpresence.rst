+++++++++++++++++++++++++++++++++++++++
d-presence
+++++++++++++++++++++++++++++++++++++++

The following code snippet assesses whether the data satisfies :math:`\delta`-presence [1]_。

We use ``data/delta/delta.csv`` as the original data, ``data/delta/delta_anonymized.csv`` as the anonymized data, and the data hierarchy, ``data/delta/delta_hierarchy``, and the attribute type definitions in ``data/adult/adult_anonymized.yaml`` to demonstrate how to evaluate this metric through PETWorks-framework.

In the following code snippet, we use the API ``PETValidation(origin, anonymized, "d-presence", dMin, dMax)`` with the data, the string “d-presence,” and the variables dMin and dMax as parameters to determine whether the data satisfies :math:`\delta`-presence.

Then, we use the API ``report(result, format)`` with the evaluation result and the string "json" as parameters to print the evaluation result in JSON format.

Example: d-presence.py
-------------------------

.. code-block:: python

    from PETWorks import PETValidation, report

    origin = "data/delta/delta.csv"
    anonymized = "data/delta/delta_anonymized.csv"

    result = PETValidation(
        origin, anonymized, "d-presence", dMin=1 / 2, dMax=2 / 3
    )
    report(result, "json")


Execution Result
------------------

.. code-block:: text
    
    $ python3 d-presence.py
    {
        "dMin": 0.5,
        "dMax": 0.6666666666666666,
        "d-presence": true
    }


Reference
---------
.. [1] M. E. Nergiz, M. Atzori, and C. Clifton, “Hiding the presence of individuals from shared databases,” Proceedings of the 2007 ACM SIGMOD international conference on Management of data, 2007. 


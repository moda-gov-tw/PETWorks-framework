+++++++++++++++++++++++++++++++++++++++
t-closeness
+++++++++++++++++++++++++++++++++++++++

The following code snippet assesses whether the data satisfies t-closeness [1]_。

We use ``data/patient/patient_anonymized.csv`` as the anonymized data, the data hierarchy, ``data/patient/patient_hierarchy``, and the attribute type definitions in ``data/patient/patient_anonymized.yaml`` to demonstrate how to evaluate this metric through PETWorks-framework.

In the following code snippet, we use the API ``PETValidation(None, anonymized, "t-closeness", tLimit)`` with the data, the string “t-closeness,” and the variables tLimit as parameters to determine whether the data satisfies t-closeness.

Then, we use the API ``report(result, format)`` with the evaluation result and the string "json" as parameters to print the evaluation result in JSON format.

Example: t-closeness.py
--------------------------

.. code-block:: python

    from PETWorks import PETValidation, report

    anonymized = "datasets/patient/patient_anonymized.csv"

    result = PETValidation(
        None,
        anonymized,
        "t-closeness",
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

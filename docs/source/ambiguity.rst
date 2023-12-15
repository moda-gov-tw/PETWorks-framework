+++++++++++++++++++++++++++++++++++++++
Ambiguity
+++++++++++++++++++++++++++++++++++++++

The following code snippet evaluate the ambiguity of the data [1]_ .

We use ``data/adult/adult.csv`` as the original data, ``data/adult/adult_anonymized.csv`` as the anonymized data, and the data hierarchy, ``data/adult/adult_hierarchy``, defined in ``data/adult/adult_anonymized.yaml`` to demonstrate how to evaluate this metric through PETWorks-framework.

In the following code snippet, we use the API ``PETValidation(original, anonymized, "Ambiguity")`` with the data and the string "Ambiguity" as parameters to evaluate the ambiguity.

Then, we use the API ``report(result, format)`` with the evaluation result and the string "json" as parameters to print the evaluation result in JSON format.

Example: ambiguity.py
------------------------

.. code-block:: python

    from PETWorks import PETValidation, report

    originalData = "data/adult/adult.csv"
    anonymizedData = "data/adult/adult_anonymized.csv"

    result = PETValidation(originalData, anonymizedData, "Ambiguity")
    report(result, "json")


Execution Result
------------------

.. code-block:: bash

    $ python3 ambiguity.py
    {
        "ambiguity": 0.72714009672634
    }

Reference
-----------

.. [1] J. Goldberger and T. Tassa, “Efficient Anonymizations with Enhanced Utility,” in 2009 IEEE International Conference on Data Mining Workshops, Miami, FL, USA, Dec. 2009, pp. 106–113. doi: 10.1109/ICDMW.2009.15.

+++++++++++++++++++++++++++++++++++++++
Ambiguity
+++++++++++++++++++++++++++++++++++++++

The following code snippet evaluate the ambiguity of the data [1]_ .

We use ``data/adult.csv`` as the original data, ``data/adult_anonymized.csv`` as the anonymized data, and ``data/adult_hierarchy`` as the data hierarchy to demonstrate how to evaluate this indicator through PETWorks-framework.

In the following code snippet, we use the API ``PETValidation(original, anonymized, tech, dataHierarchy)`` with the data and the string "Ambiguity" as parameters to evaluate the ambiguity.

Then, we use the API ``report(result, format)`` with the evaluation result and the string "json" as parameters to print the evaluation result in JSON format.

Example: ambiguity.py
------------------------

.. code-block:: python

    from PETWorks import PETValidation, report

    originalData = "data/adult.csv"
    anonymizedData = "data/adult_anonymized.csv"
    dataHierarchy = "data/adult_hierarchy"

    result = PETValidation(
        originalData, anonymizedData, "Ambiguity", dataHierarchy=dataHierarchy
    )
    report(result, "json")


Execution Result
------------------

.. code-block:: bash

    $ python3 ambiguity.py
    {
        "ambiguity": 0.7271401100722763
    }

Reference
-----------

.. [1] J. Goldberger and T. Tassa, “Efficient Anonymizations with Enhanced Utility,” in 2009 IEEE International Conference on Data Mining Workshops, Miami, FL, USA, Dec. 2009, pp. 106–113. doi: 10.1109/ICDMW.2009.15.

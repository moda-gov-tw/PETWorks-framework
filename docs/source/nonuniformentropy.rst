+++++++++++++++++++++++++++++++++++++++
Non-Uniform Entropy
+++++++++++++++++++++++++++++++++++++++

The following code snippet evaluate the non-uniform entropy [1]_。

We use ``data/adult/adult.csv`` as the original data, ``data/adult/adult_anonymized.csv`` as the anonymized data, and the data hierarchy, ``data/adult/adult_hierarchy``, defined in ``data/adult/adult_anonymized.yaml`` to demonstrate how to evaluate this metric through PETWorks-framework.

In the following code snippet, we use the API ``PETValidation(original, anonymized, "Non-Uniform Entropy")`` with the data and the string “Non-Uniform Entropy” as the parameters to evaluate the non-uniform entropy.

Then, we use the API ``report(result, format)`` with the evaluation result and the string "json" as parameters to print the evaluation result in JSON format.

Example: nonUniformEntropy.py
----------------------------------

.. code-block:: python

    from PETWorks import PETValidation, report

    originalData = "data/adult/adult.csv"
    anonymizedData = "data/adult/adult_anonymized.csv"

    result = PETValidation(originalData, anonymizedData, "Non-Uniform Entropy")
    report(result, "json")

Execution Result
------------------

.. code-block:: bash

    $ python nonUniformEntropy.py
    {
        "Non-Uniform Entropy": 0.6740002378300514
    }

Reference
-----------

.. [1] A. Gionis and T. Tassa, “k-Anonymization with Minimal Loss of Information.” IEEE Transactions on Knowledge and Data Engineering, vol. 21, no. 2, pp. 206-219, 2009, doi: 10.1109/tkde.2008.129.

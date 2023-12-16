+++++++++++++++++++++++++++++++++++++++
De-identification for k-anonymity
+++++++++++++++++++++++++++++++++++++++

The following code snippet de-identify the data to satisfy k-anonymity [1]_.

We use ``data/adult/adult.csv`` as the original data, the data hierarchy, ``data/adult/adult_hierarchy``, and the attribute type definitions in ``data/adult/adult.yaml`` to demonstrate how to perform de-identification through PETWorks-framework.

In the following code snippet, we use the API ``PETAnonymization(originalData, "k-anonymity", maxSuppressionRate, k)`` with the data, the string “k-anonymity”, the maximal suppression rate, and the target k value as the parameters to perform de-identification for k-anonymity.

Then, we use the API ``report(result, path)`` with the result and the string "path" as parameters to write the result to the path.

Example: k-anonymization.py
------------------------------------

                                                           
.. code-block:: python
                                                           
  from PETWorks import PETAnonymization, output

  originalData = "data/adult/adult.csv"

  result = PETAnonymization(
      originalData,
      "k-anonymity",
      maxSuppressionRate=0.6,
      k=6,
  )

  output(result, "output.csv")

Execution Result
---------------------------

The above code snippet will output a de-identification result satisfying k-anonymity with k = 6 to ``output.csv``. The excerpt of the file content is as follows:

+--------+-----+------+----------------+-----------+----------------+------------------+------------+--------------+
| sex    | age | race | marital-status | education | native-country | workclass        | occupation | salary-class |
+--------+-----+------+----------------+-----------+----------------+------------------+------------+--------------+
| Male   | 37  | \*   | \*             | \*        | \*             | State-gov        | \*         | \*           |
+--------+-----+------+----------------+-----------+----------------+------------------+------------+--------------+
| Male   | 47  | \*   | \*             | \*        | \*             | Self-emp-not-inc | \*         | \*           |
+--------+-----+------+----------------+-----------+----------------+------------------+------------+--------------+
| Male   | 37  | \*   | \*             | \*        | \*             | Private          | \*         | \*           |
+--------+-----+------+----------------+-----------+----------------+------------------+------------+--------------+
| Male   | 52  | \*   | \*             | \*        | \*             | Private          | \*         | \*           |
+--------+-----+------+----------------+-----------+----------------+------------------+------------+--------------+
| Female | 27  | \*   | \*             | \*        | \*             | Private          | \*         | \*           |
+--------+-----+------+----------------+-----------+----------------+------------------+------------+--------------+
| Female | 37  | \*   | \*             | \*        | \*             | Private          | \*         | \*           |
+--------+-----+------+----------------+-----------+----------------+------------------+------------+--------------+
| Female | 47  | \*   | \*             | \*        | \*             | Private          | \*         | \*           |
+--------+-----+------+----------------+-----------+----------------+------------------+------------+--------------+
| Male   | 52  | \*   | \*             | \*        | \*             | Self-emp-not-inc | \*         | \*           |
+--------+-----+------+----------------+-----------+----------------+------------------+------------+--------------+
| Female | 32  | \*   | \*             | \*        | \*             | Private          | \*         | \*           |
+--------+-----+------+----------------+-----------+----------------+------------------+------------+--------------+
| ...    | ... | ...  | ...            | ...       | ...            | ...              | ...        | ...          |
+--------+-----+------+----------------+-----------+----------------+------------------+------------+--------------+

Use `the validation API <https://petworks-doc.readthedocs.io/en/latest/kanonymity.html>`_ to verify the result satisfies k-anonymity with k = 6.

.. code-block:: json

  {
      "k": 6,
      "fulfill k-anonymity": true
  }

Reference
-----------
.. [1] L. Sweeney, “K-anonymity: A model for protecting privacy,” International Journal of Uncertainty, Fuzziness and Knowledge-Based Systems, vol. 10, no. 05, pp. 557–570, 2002. 
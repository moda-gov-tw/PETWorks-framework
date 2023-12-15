+++++++++++++++++++++++++++++++++++++++
De-identification for t-closeness
+++++++++++++++++++++++++++++++++++++++

The following code snippet de-identify the data to satisfy t-closeness [1]_.

We use ``data/adult/adult.csv`` as the original data, the data hierarchy, ``data/adult/adult_hierarchy``, and the attribute type definitions in ``data/adult/adult.yaml`` to demonstrate how to perform de-identification through PETWorks-framework.

In the following code snippet, we use the API ``PETAnonymization(originalData, "t-closeness", maxSuppressionRate, t)`` with the data, the string “t-closeness,” the maximal suppression rate, and the target t value as the parameters to perform de-identification for t-closeness.

Then, we use the API ``report(result, path)`` with the result and the string "path" as parameters to write the result to the path.

Example: t-closeness.py
---------------------------

.. code-block:: python

  from PETWorks import PETAnonymization, output

  originalData = "data/adult/adult.csv"

  result = PETAnonymization(
      originalData,
      "t-closeness",
      maxSuppressionRate=0.6,
      t=0.2,
  )

  output(result, "output.csv")

Execution Result
---------------------------

The above code snippet will output a de-identification result satisfying t-closeness with t = 0.2 to ``output.csv``. The excerpt of the file content is as follows:

+--------+-----+------+----------------+-----------+----------------+------------------+------------+--------------+
| sex    | age | race | marital-status | education | native-country | workclass        | occupation | salary-class |
+--------+-----+------+----------------+-----------+----------------+------------------+------------+--------------+
| Male   | 39  | \*   | \*             | \*        | \*             | State-gov        | \*         | \*           |
+--------+-----+------+----------------+-----------+----------------+------------------+------------+--------------+
| Male   | 50  | \*   | \*             | \*        | \*             | Self-emp-not-inc | \*         | \*           |
+--------+-----+------+----------------+-----------+----------------+------------------+------------+--------------+
| Male   | 38  | \*   | \*             | \*        | \*             | Private          | \*         | \*           |
+--------+-----+------+----------------+-----------+----------------+------------------+------------+--------------+
| Male   | 53  | \*   | \*             | \*        | \*             | Private          | \*         | \*           |
+--------+-----+------+----------------+-----------+----------------+------------------+------------+--------------+
| Female | 28  | \*   | \*             | \*        | \*             | Private          | \*         | \*           |
+--------+-----+------+----------------+-----------+----------------+------------------+------------+--------------+
| Female | 37  | \*   | \*             | \*        | \*             | Private          | \*         | \*           |
+--------+-----+------+----------------+-----------+----------------+------------------+------------+--------------+
| Female | 49  | \*   | \*             | \*        | \*             | Private          | \*         | \*           |
+--------+-----+------+----------------+-----------+----------------+------------------+------------+--------------+
| Male   | 52  | \*   | \*             | \*        | \*             | Self-emp-not-inc | \*         | \*           |
+--------+-----+------+----------------+-----------+----------------+------------------+------------+--------------+
| Female | 31  | \*   | \*             | \*        | \*             | Private          | \*         | \*           |
+--------+-----+------+----------------+-----------+----------------+------------------+------------+--------------+
| Male   | 42  | \*   | \*             | \*        | \*             | Private          | \*         | \*           |
+--------+-----+------+----------------+-----------+----------------+------------------+------------+--------------+
| Male   | 37  | \*   | \*             | \*        | \*             | Private          | \*         | \*           |
+--------+-----+------+----------------+-----------+----------------+------------------+------------+--------------+
| Male   | 30  | \*   | \*             | \*        | \*             | State-gov        | \*         | \*           |
+--------+-----+------+----------------+-----------+----------------+------------------+------------+--------------+
| Female | 23  | \*   | \*             | \*        | \*             | Private          | \*         | \*           |
+--------+-----+------+----------------+-----------+----------------+------------------+------------+--------------+
| ...    | ... | ...  | ...            | ...       | ...            | ...              | ...        | ...          |
+--------+-----+------+----------------+-----------+----------------+------------------+------------+--------------+

Use `the validation API <https://petworks-doc.readthedocs.io/en/latest/tcloseness.html>`_ to verify the result satisfies t-closeness with t = 0.2.

.. code-block:: json

  {
      "t": 0.2,
      "fulfill t-closeness": true
  }

Reference
---------
.. [1] N. Li, T. Li and S. Venkatasubramanian, “t-Closeness: Privacy Beyond k-Anonymity and l-Diversity,” 2007 IEEE 23rd International Conference on Data Engineering, Istanbul, Turkey, 2007, pp. 106-115, doi: 10.1109/ICDE.2007.367856.

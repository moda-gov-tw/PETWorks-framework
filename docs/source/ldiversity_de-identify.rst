+++++++++++++++++++++++++++++++++++++++
De-identification for l-diversity
+++++++++++++++++++++++++++++++++++++++


The following code snippet de-identify the data to satisfy :math:`l`-diversity [1]_。

We use ``data/adult/adult.csv`` as the original data, the data hierarchy, ``data/adult/adult_hierarchy``, and the attribute type definitions in ``data/adult/adult.yaml`` to demonstrate how to perform de-identification through PETWorks-framework.

In the following code snippet, we use the API ``PETAnonymization(originalData, tech, maxSuppressionRate, l)`` with the data, the string “l-diversity”, the attribute type definitions, the maximal suppression rate, and the target l value as the parameters to perform de-identification for l-diversity.

Then, we use the API ``report(result, path)`` with the result and the string "path" as parameters to write the result to the path.

Example: l-diversity.py
---------------------------

.. code-block:: python

  from PETWorks import PETAnonymization, output

  originalData = "datasets/adult/adult.csv"

  result = PETAnonymization(
      originalData,
      "l-diversity",
      maxSuppressionRate=0.6,
      l=6,
  )

  output(result, "output.csv")


Execution Result
---------------------------

The above code snippet will output a de-identification result satisfying :math:`l`-diversity with :math:`l = 6` to ``output.csv``. The excerpt of the file content is as follows:

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
| Male   | 42  | \*   | \*             | \*        | \*             | Private          | \*         | \*           |
+--------+-----+------+----------------+-----------+----------------+------------------+------------+--------------+
| Male   | 37  | \*   | \*             | \*        | \*             | Private          | \*         | \*           |
+--------+-----+------+----------------+-----------+----------------+------------------+------------+--------------+
| Male   | 27  | \*   | \*             | \*        | \*             | State-gov        | \*         | \*           |
+--------+-----+------+----------------+-----------+----------------+------------------+------------+--------------+
| Female | 22  | \*   | \*             | \*        | \*             | Private          | \*         | \*           |
+--------+-----+------+----------------+-----------+----------------+------------------+------------+--------------+
| ...    | ... | ...  | ...            | ...       | ...            | ...              | ...        | ...          |
+--------+-----+------+----------------+-----------+----------------+------------------+------------+--------------+

Use `the validation API <https://petworks-doc.readthedocs.io/en/latest/ldiversity.html>`_ to verify the result satisfies :math:`l`-diversity with :math:`l = 6`.

.. code-block:: json

  {
      "l": 6,
      "fulfill l-diversity": true
  }

Reference
---------
.. [1] A. Machanavajjhala, J. Gehrke, D. Kifer, and M. Venkitasubramaniam, L-diversity: privacy beyond k-anonymity. 2006. doi: 10.1109/icde.2006.1.

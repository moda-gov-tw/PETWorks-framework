+++++++++++++++++++++++++++++++++++++++
De-identification for d-presence
+++++++++++++++++++++++++++++++++++++++

The following code snippet de-identify the data to satisfy :math:`\delta`-presence [1]_.

We use ``data/adult/adult.csv`` as the original data, ``data/adult/adult10.csv`` as the subset, and the data hierarchy, ``data/adult/adult_hierarchy``, and the attribute type definitions in ``data/adult/adult.yaml`` to demonstrate how to perform de-identification through PETWorks-framework.

In the following code snippet, we use the API ``PETAnonymization(originalData, "d-presence", maxSuppressionRate, dMin, dMax, subsetData)`` with the data, the string “d-presence", the maximal suppression rate, the target dMin and dMax, and the subset ``subsetData`` as the parameters to perform de-identification for d-presence.

Then, we use the API ``report(result, path)`` with the result and the string "path" as parameters to write the result to the path.

Example: d-presence.py
---------------------------
                                                                                                  
.. code-block:: python
                                                                                                  
  from PETWorks import PETAnonymization, output

  originalData = "data/adult/adult.csv"
  subsetData = "data/adult/adult10.csv"

  result = PETAnonymization(
      originalData,
      "d-presence",
      maxSuppressionRate=0.6,
      dMin=0.0,
      dMax=0.7,
      subsetData=subsetData,
  )

  output(result, "output.csv")

Execution Result
---------------------------

The above code snippet will output a de-identification result satisfying :math:`\delta`-presence with d in the range of 0.0 and 0.7 to ``output.csv``. The excerpt of the file content is as follows:

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
| \*     | \*  | \*   | \*             | \*        | \*             | Private          | \*         | \*           |
+--------+-----+------+----------------+-----------+----------------+------------------+------------+--------------+
| \*     | \*  | \*   | \*             | \*        | \*             | State-gov        | \*         | \*           |
+--------+-----+------+----------------+-----------+----------------+------------------+------------+--------------+
| \*     | \*  | \*   | \*             | \*        | \*             | Private          | \*         | \*           |
+--------+-----+------+----------------+-----------+----------------+------------------+------------+--------------+
| ...    | ... | ...  | ...            | ...       | ...            | ...              | ...        | ...          |
+--------+-----+------+----------------+-----------+----------------+------------------+------------+--------------+

Use `the validation API <https://petworks-doc.readthedocs.io/en/latest/dpresence.html>`_ to verify the result satisfies :math:`\delta`-presence with d in the range of 0.0 and 0.7.

.. code-block:: json
                                                                                                  
  {
      "dMin": 0.0,
      "dMax": 0.7,
      "d-presence": true
  }

Reference
---------
.. [1] M. E. Nergiz, M. Atzori, and C. Clifton, “Hiding the presence of individuals from shared databases,” Proceedings of the 2007 ACM SIGMOD international conference on Management of data, 2007. 

+++++++++++++++++++++++++++++++++++++++
De-identification for t-closeness
+++++++++++++++++++++++++++++++++++++++

The following code snippet de-identify the data to satisfy t-closeness [1]_.

We use ``data/adult.csv`` as the original data, ``data/adult_hierarchy`` as the data hierarchy, and ``attributeTypes`` as the attribute type definitions to demonstrate how to perform de-identification through PETWorks-framework.

In the following code snippet, we use the API ``PETAnonymization(originalData, tech, dataHierarchy, attributeTypes, maxSuppressionRate, t)`` with the data, the string “t-closeness,” the attribute type definitions, the maximal suppression rate, and the target t value as the parameters to perform de-identification for t-closeness.

Then, we use the API ``report(result, path)`` with the result and the string "path" as parameters to write the result to the path.

Example: t-closeness.py
---------------------------

.. code-block:: python

  from PETWorks import PETAnonymization, output
  from PETWorks.attributetypes import *
  
  originalData = "data/adult.csv"
  dataHierarchy = "data/adult_hierarchy"
  
  attributeTypes = {
      "sex": QUASI_IDENTIFIER,
      "age": QUASI_IDENTIFIER,
      "workclass": SENSITIVE_ATTRIBUTE,
  }
  
  result = PETAnonymization(
      originalData,
      "t-closeness",
      dataHierarchy,
      attributeTypes,
      maxSuppressionRate=0.6,
      t=0.2,
  )
  
  output(result, "output.csv")





Execution Result
---------------------------

上述程式碼將輸出滿足 t = 0.2 之 t-相似性去識別化結果至 `output.csv`。檔案內容節錄如下：

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

以本專案開發之 `t-相似性再識別化工具 <https://petworks-doc.readthedocs.io/en/latest/tcloseness.html>`_ 進行檢測，可確認去識別化結果已滿足 t = 0.2 之 t-相似性。

.. code-block:: json

  {
      "t": 0.2,
      "fulfill t-closeness": true
  }

Reference
---------
.. [1] N. Li, T. Li and S. Venkatasubramanian, “t-Closeness: Privacy Beyond k-Anonymity and l-Diversity,” 2007 IEEE 23rd International Conference on Data Engineering, Istanbul, Turkey, 2007, pp. 106-115, doi: 10.1109/ICDE.2007.367856.

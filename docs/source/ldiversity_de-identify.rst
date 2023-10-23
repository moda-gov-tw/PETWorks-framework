+++++++++++++++++++++++++++++++++++++++
De-identification for l-diversity
+++++++++++++++++++++++++++++++++++++++


The following code snippet de-identify the data to satisfy :math:`l`-diversity [1]_。

We use ``data/adult.csv`` as the original data, ``data/adult_hierarchy`` as the data hierarchy, and ``attributeTypes`` as the attribute type definitions to demonstrate how to perform de-identification through PETWorks-framework.

In the following code snippet, we use the API ``PETAnonymization(originalData, tech, dataHierarchy, attributeTypes, maxSuppressionRate, l)`` with the data, the string “l-diversity”, the attribute type definitions, the maximal suppression rate, and the target l value as the parameters to perform de-identification for l-diversity.

Then, we use the API ``report(result, path)`` with the result and the string "path" as parameters to write the result to the path.

Example: l-diversity.py
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
      "l-diversity",
      dataHierarchy,
      attributeTypes,
      maxSuppressionRate=0.6,
      l=6,
  )

  output(result, "output.csv")


Execution Result
---------------------------

上述程式碼將輸出滿足 :math:`l = 6` 之 :math:`l`-多樣性去識別化結果至 `output.csv`。檔案內容節錄如下：

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


以本專案開發之 `l-多樣性再識別化工具 <https://petworks-doc.readthedocs.io/en/latest/ldiversity.html>`_ 進行檢測，可確認去識別化結果已滿足 :math:`l = 6` 之 :math:`l`-多樣性。

.. code-block:: json

  {
      "l": 6,
      "fulfill l-diversity": true
  }

Reference
---------
.. [1] A. Machanavajjhala, J. Gehrke, D. Kifer, and M. Venkitasubramaniam, L-diversity: privacy beyond k-anonymity. 2006. doi: 10.1109/icde.2006.1.

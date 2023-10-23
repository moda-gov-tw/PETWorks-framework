+++++++++++++++++++++++++++++++++++++++
De-identification for d-presence
+++++++++++++++++++++++++++++++++++++++

The following code snippet de-identify the data to satisfy :math:`\delta`-presence [1]_.

We use ``data/adult.csv`` as the original data, ``data/adult_hierarchy`` as the data hierarchy, and ``attributeTypes`` as the attribute type definitions, and ``data/adult10.csv`` as the subset to demonstrate how to perform de-identification through PETWorks-framework.

In the following code snippet, we use the API ``PETAnonymization(originalData, tech, dataHierarchy, attributeTypes, maxSuppressionRate, dMin, dMax, subsetData)`` with the data, the string “d-presence", the attribute type definitions, the maximal suppression rate, the target dMin and dMax, and the subset ``subsetData`` as the parameters to perform de-identification for d-presence.

Then, we use the API ``report(result, path)`` with the result and the string "path" as parameters to write the result to the path.

Example: d-presence.py
---------------------------
                                                                                                  
.. code-block:: python
                                                                                                  
  from PETWorks import PETAnonymization, output
  from PETWorks.attributetypes import *
  
  originalData = "data/adult.csv"
  dataHierarchy = "data/adult_hierarchy"
  subsetData = "data/adult10.csv"
  
  attributeTypes = {
      "sex": QUASI_IDENTIFIER,
      "age": QUASI_IDENTIFIER,
      "workclass": SENSITIVE_ATTRIBUTE,
  }
  
  result = PETAnonymization(
      originalData,
      "d-presence",
      dataHierarchy,
      attributeTypes,
      maxSuppressionRate=0.6,
      dMin=0.0,
      dMax=0.7,
      subsetData=subsetData,
  )
  
  output(result, "output.csv")

Execution Result
---------------------------


上述程式碼將輸出滿足 dMin = 0.0 與 dMax = 0.7 之 :math:`\delta`-存在性去識別化結果至 `output.csv`。檔案內容節錄如下：

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

以本專案開發之 `δ-匿名性再識別化工具 <https://petworks-doc.readthedocs.io/en/latest/dpresence.html>`_ 進行檢測，可確認去識別化結果已滿足 :math:`\delta_{\min}` = 0.0 與 :math:`\delta_{\max}` = 0.7 之 :math:`\delta`-存在性。

.. code-block:: json
                                                                                                  
  {
      "dMin": 0.0,
      "dMax": 0.7,
      "d-presence": true
  }

Reference
---------
.. [1] M. E. Nergiz, M. Atzori, and C. Clifton, “Hiding the presence of individuals from shared databases,” Proceedings of the 2007 ACM SIGMOD international conference on Management of data, 2007. 

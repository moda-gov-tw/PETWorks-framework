+++++++++++++++++++++++++++++++++++++++
De-identification for k-anonymity
+++++++++++++++++++++++++++++++++++++++

The following code snippet de-identify the data to satisfy k-anonymity [1]_.

We use ``data/adult.csv`` as the original data, ``data/adult_hierarchy`` as the data hierarchy, and ``attributeTypes`` as the attribute type definitions to demonstrate how to perform de-identification through PETWorks-framework.

In the following code snippet, we use the API ``PETAnonymization(originalData, tech, dataHierarchy, attributeTypes, maxSuppressionRate, k)`` with the data, the string “k-anonymity”, the attribute type definitions, the maximal suppression rate, and the target k value as the parameters to perform de-identification for k-anonymity.

Then, we use the API ``report(result, path)`` with the result and the string "path" as parameters to write the result to the path.

Example: k-anonymization.py
------------------------------------

                                                           
.. code-block:: python
                                                           
  from PETWorks import PETAnonymization, output
  from PETWorks.attributetypes import *
  
  originalData = "data/adult.csv"
  dataHierarchy = "data/adult_hierarchy"
  
  attributeTypes = {
      "sex": QUASI_IDENTIFIER,
      "age": QUASI_IDENTIFIER,
      "workclass": QUASI_IDENTIFIER,
  }
  
  result = PETAnonymization(
      originalData,
      "k-anonymity",
      dataHierarchy,
      attributeTypes,
      maxSuppressionRate=0.6,
      k=6,
  )
  
  output(result, "output.csv")




Execution Result
---------------------------

上述程式碼將輸出滿足 k = 6 之 k-匿名性去識別化結果至 `output.csv`。檔案內容節錄如下：


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

以本專案開發之 `k-匿名性再識別化工具 <https://petworks-doc.readthedocs.io/en/latest/kanonymity.html>`_ 進行檢測，可確認去識別化結果已滿足 k = 6 之 k-匿名性。

.. code-block:: json

  {
      "k": 6,
      "fulfill k-anonymity": true
  }

Reference
-----------
.. [1] L. Sweeney, “K-anonymity: A model for protecting privacy,” International Journal of Uncertainty, Fuzziness and Knowledge-Based Systems, vol. 10, no. 05, pp. 557–570, 2002. 
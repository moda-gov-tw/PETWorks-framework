++++++++++++++++++++++++++++++++++++++++++++
Traditional De-identification Technologies
++++++++++++++++++++++++++++++++++++++++++++

Average Equivalence Class Size
==================================

The following code snippet evaluate the average equivalence class size [1]_.

We use ``data/adult.csv`` as the original data and ``data/adult_anonymized.csv`` as the anonymized data to demonstrate how to evaluate this indicator through PETWorks-framework.

In the following code snippet, we use the API ``PETValidation(original, anonymized, tech)`` with the data and the string “AECS” as parameters to evaluate the ambiguity.

Then, we use the API ``report(result, format)`` with the evaluation result and the string "json" as parameters to print the evaluation result in JSON format.

Example: aecs.py
------------------------

.. code-block:: python

    from PETWorks import PETValidation, report

    originalData = "data/adult.csv"
    anonymizedData = "data/adult_anonymized.csv"

    result = PETValidation(
        originalData, anonymizedData, "AECS"
        )
    report(result, "json")


Execution Result
------------------

.. code-block:: text

    $ python aecs.py
    {
        "AECS": 0.9992930131052006
    }


Reference
-----------

.. [1] K. LeFevre, D. J. DeWitt and R. Ramakrishnan, "Mondrian Multidimensional K-Anonymity," 22nd International Conference on Data Engineering (ICDE'06), Atlanta, GA, USA, 2006, pp. 25-25, doi: 10.1109/ICDE.2006.101. 


Ambiguity
==============

The following code snippet evaluate the ambiguity of the data [2]_ .

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

.. [2] J. Goldberger and T. Tassa, “Efficient Anonymizations with Enhanced Utility,” in 2009 IEEE International Conference on Data Mining Workshops, Miami, FL, USA, Dec. 2009, pp. 106–113. doi: 10.1109/ICDMW.2009.15.



d-presence
===============

The following code snippet assesses whether the data satisfies :math:`\delta`-presence [3]_。

We use ``data/delta.csv`` as the original data, ``data/delta_anonymized.csv`` as the anonymized data, ``data/delta_hierarchy`` as the data hierarchy, and ``attributeTypes`` as the attribute type definitions to demonstrate how to evaluate this indicator through PETWorks-framework.

In the following code snippet, we use the API ``PETValidation(origin, anonymized, "d-presence", dataHierarchy, attributeTypes, dMin, dMax)`` with the data, the string “d-presence,” and the variables dMin and dMax as parameters to determine whether the data satisfies :math:`\delta`-presence.

Then, we use the API ``report(result, format)`` with the evaluation result and the string "json" as parameters to print the evaluation result in JSON format.

Example: d-presence.py
-------------------------

.. code-block:: python

    from PETWorks import PETValidation, report
    from PETWorks.attributetypes import SENSITIVE_ATTRIBUTE, QUASI_IDENTIFIER


    origin = "data/delta.csv"
    anonymized = "data/delta_anonymized.csv"
    dataHierarchy = "data/delta_hierarchy"

    attributeTypes = {
        "zip": QUASI_IDENTIFIER,
        "age": QUASI_IDENTIFIER,
        "nationality": QUASI_IDENTIFIER,
        "salary-class": SENSITIVE_ATTRIBUTE
    }

    result = PETValidation(
            origin, anonymized, "d-presence", dataHierarchy=dataHierarchy, attributeTypes=attributeTypes, dMin=1/2, dMax=2/3
        )
    report(result, "json")


Execution Result
------------------

.. code-block:: text
    
    $ python3 d-presence.py
    {
        "dMin": 0.5,
        "dMax": 0.6666666666666666,
        "d-presence": true
    }


Reference
---------
.. [3] M. E. Nergiz, M. Atzori, and C. Clifton, “Hiding the presence of individuals from shared databases,” Proceedings of the 2007 ACM SIGMOD international conference on Management of data, 2007. 


k-anonymity
================

The following code snippet assesses whether the data satisfies k-anonymity [4]_。

We use ``data/adult_anonymized.csv`` as the anonymized data and ``attributeTypes`` as the attribute type definitions to demonstrate the evaluation of this indicator through PETWorks-Framework.

In the following code snippet, we use the API ``PETValidation(None, anonymized, tech, attributeTypes, k)`` with the data, the string "k-anonymity", and the k value as parameters to determine whether the data satisfies k-anonymity.

Then, we use the API ``report(result, format)`` with the evaluation result and the string "json" as parameters to print the evaluation result in JSON format.


Example: k-anonymity.py
---------------------------

.. code-block:: python

    from PETWorks import PETValidation, report
    from PETWorks.attributetypes import QUASI_IDENTIFIER

    anonymizedData = "data/adult_anonymized.csv"

    attributeTypes = {
        "age": QUASI_IDENTIFIER,
        "sex": QUASI_IDENTIFIER,
    }

    result = PETValidation(
            None, anonymizedData, "k-anonymity", attributeTypes=attributeTypes, k=6
    )
    report(result, "json")

Execution Result
------------------

.. code-block:: text

    $ python3 k-anonymity.py
    {
        "k": 6,
        "k-anonymity": true
    }

Reference
-----------

.. [4] L. Sweeney, “K-anonymity: A model for protecting privacy,” International Journal of Uncertainty, Fuzziness and Knowledge-Based Systems, vol. 10, no. 05, pp. 557–570, 2002. 


l-diversity
=============

The following code snippet assesses whether the data satisfies :math:`l`-diversity [5]_.

We use ``data/inpatient_anonymized.csv`` as the anonymized data and ``attributeTypes`` as the attribute type definitions to demonstrate how to evaluate this indicator through PETWorks-framework.

In the following code snippet, we use the API ``PETValidation(None, anonymized, "l-diversity", attributeTypes, l)`` with the data, the string "l-diversity", and the l value as parameters to determine whether the data satisfies :math:`l`-diversity.

Then, we use the API ``report(result, format)`` with the evaluation result and the string "json" as parameters to print the evaluation result in JSON format.

Example: l-diversity.py
-------------------------

.. code-block:: python

    from PETWorks import PETValidation, report
    from PETWorks.attributetypes import SENSITIVE_ATTRIBUTE, QUASI_IDENTIFIER

    anonymized = "data/inpatient_anonymized.csv"

    attributeTypes = {
        "zipcode": QUASI_IDENTIFIER,
        "age": QUASI_IDENTIFIER,
        "nationality": QUASI_IDENTIFIER,
        "condition": SENSITIVE_ATTRIBUTE
    }

    result = PETValidation(
        None, anonymized, "l-diversity", attributeTypes=attributeTypes, l=3
    )
    report(result, "json")

Execution Result
------------------

.. code-block:: text
    
    $ python3 l-diversity.py
    {
        "l": 3,
        "fulfill l-diversity": true
    }

Reference
---------
.. [5] A. Machanavajjhala, J. Gehrke, D. Kifer, and M. Venkitasubramaniam, L-diversity: privacy beyond k-anonymity. 2006. doi: 10.1109/icde.2006.1.


Non-Uniform Entropy
=======================

The following code snippet evaluate the non-uniform entropy [6]_。

We use ``data/adult.csv`` as the original data, ``data/adult_anonymized.csv`` as the anonymized data, and ``data/adult_hierarchy`` as the data hierarchy to demonstrate how to evaluate this indicator through PETWorks-framework.

In the following code snippet, we use the API ``PETValidation(original, anonymized, tech, dataHierarchy)`` with the data and the string “Non-Uniform Entropy” as the parameters to evaluate the non-uniform entropy.

Then, we use the API ``report(result, format)`` with the evaluation result and the string "json" as parameters to print the evaluation result in JSON format.

Example: nonUniformEntropy.py
----------------------------------

.. code-block:: python

    from PETWorks import PETValidation, report

    originalData = "data/adult.csv"
    anonymizedData = "data/adult_anonymized.csv"
    dataHierarchy = "data/adult_hierarchy"

    result = PETValidation(
        originalData, anonymizedData, "Non-Uniform Entropy", dataHierarchy=dataHierarchy
    )
    report(result, "json")

Execution Result
------------------

.. code-block:: bash

    $ python nonUniformEntropy.py
    {
        "Non-Uniform Entropy": 0.6691909578638351
    }


Reference
-----------

.. [6] A. Gionis and T. Tassa, “k-Anonymization with Minimal Loss of Information.” IEEE Transactions on Knowledge and Data Engineering, vol. 21, no. 2, pp. 206-219, 2009, doi: 10.1109/tkde.2008.129.



Precision
=================

The following code snippet evaluate the precision [7]_.

We use ``data/adult.csv`` as the original data, ``data/adult_anonymized.csv`` as the anonymized data, and ``data/adult_hierarchy`` as the data hierarchy to demonstrate how to evaluate this indicator through PETWorks-framework.

In the following code snippet, we use the API ``PETValidation(original, anonymized, tech, dataHierarchy)`` with the data and the string “Precision” as the parameters to evaluate the precision.

Then, we use the API ``report(result, format)`` with the evaluation result and the string "json" as parameters to print the evaluation result in JSON format.

Example: precision.py
------------------------

.. code-block:: python

    from PETWorks import PETValidation, report

    originalData = "data/adult.csv"
    anonymizedData = "data/adult_anonymized.csv"
    dataHierarchy = "data/adult_hierarchy"

    result = PETValidation(
        originalData, anonymizedData, "Precision", dataHierarchy=dataHierarchy
    )
    report(result, "json")

Execution Result
------------------

.. code-block:: bash

    $ python3 precision.py
    {
        "precision": 0.7271401100722763
    }

Reference
-----------

.. [7] L. SWEENEY, “ACHIEVING k-ANONYMITY PRIVACY PROTECTION USING GENERALIZATION AND SUPPRESSION.” International Journal of Uncertainty, Fuzziness and Knowledge-Based Systems, vol. 10, no. 5, pp. 571-588, 2002, doi: 10.1142/s021848850200165x.



Profitability
==================

The following code snippet assesses whether the data satisfies profitability [8]_.

We use ``data/delta.csv`` as the original data, ``data/delta_anonymized.csv`` as the anonymized data, ``data/delta_hierarchy`` as the data hierarchy, and ``attributeTypes`` as the attribute type definitions to demonstrate how to evaluate this indicator through PETWorks-framework.

In the following code snippet, we use the API ``PETValidation(origin, anonymized, "profitability", dataHierarchy, attributeTypes, allowAttack, adversaryCost, adversaryGain, publisherLost, publisherBenefit)`` with the data, the string “profitability", the variables allowAttack, adversaryCost, adversaryGain, publisherLost, and publisherBenefit as the parameters to determine whether the data satisfies profitability.

Then, we use the API ``report(result, format)`` with the evaluation result and the string "json" as parameters to print the evaluation result in JSON format.

Example: profitability.py
-----------------------------

.. code-block:: python

    from PETWorks import PETValidation, report
    from PETWorks.attributetypes import QUASI_IDENTIFIER, INSENSITIVE_ATTRIBUTE

    origin = "data/delta.csv"
    anonymized = "data/delta_anonymized.csv"
    dataHierarchy = "data/delta_hierarchy"

    attributeTypes = {
        "zip": QUASI_IDENTIFIER,
        "age": QUASI_IDENTIFIER,
        "nationality": QUASI_IDENTIFIER,
        "salary-class": INSENSITIVE_ATTRIBUTE
    }

    result = PETValidation(
        origin,
        anonymized,
        "profitability",
        dataHierarchy=dataHierarchy,
        attributeTypes=attributeTypes,
        allowAttack=True,
        adversaryCost=4,
        adversaryGain=300,
        publisherLost=300,
        publisherBenefit=1200
    )
    report(result, "json")


Execution Result
------------------

.. code-block:: text
    
    $ python3 profitability.py
    {
        "allow attack": true,
        "adversary's cost": 4,
        "adversary's gain": 300,
        "publisher's loss": 300,
        "publisher's benefit": 1200,
        "profitability": true
    }

Reference
-----------
.. [8] Z. Wan et al., “A Game Theoretic Framework for Analyzing Re-Identification Risk,” PLOS ONE, vol. 10, no. 3, p. e0120592, Mar. 2015, doi: 10.1371/journal.pone.0120592.



t-closeness
================

The following code snippet assesses whether the data satisfies t-closeness [9]_。

We use ``data/patient_anonymized.csv`` as the anonymized data, ``data/patient_hierarchy`` as the data hierarchy, and ``attributeTypes`` as the attribute type definitions to demonstrate how to evaluate this indicator through PETWorks-framework.

In the following code snippet, we use the API ``PETValidation(None, anonymized, "t-closeness", dataHierarchy, attributeTypes, tLimit)`` with the data, the string “t-closeness,” and the variables tLimit as parameters to determine whether the data satisfies t-closeness.

Then, we use the API ``report(result, format)`` with the evaluation result and the string "json" as parameters to print the evaluation result in JSON format.

Example: t-closeness.py
--------------------------

.. code-block:: python

   from PETWorks import PETValidation, report
    from PETWorks.attributetypes import (
        SENSITIVE_ATTRIBUTE,
        QUASI_IDENTIFIER,
    )

    anonymized = "data/patient_anonymized.csv"
    dataHierarchy = "data/patient_hierarchy"

    attributeTypes = {
        "ZIPCode": QUASI_IDENTIFIER,
        "Age": QUASI_IDENTIFIER,
        "Disease": SENSITIVE_ATTRIBUTE,
    }

    result = PETValidation(
        None,
        anonymized,
        "t-closeness",
        dataHierarchy=dataHierarchy,
        attributeTypes=attributeTypes,
        tLimit=0.376,
    )
    report(result, "json")


Execution Result
------------------

.. code-block:: text
    
    $ python3 t-closeness.py
    {
        "t": 0.376,
        "fulfill t-closeness": true
    }

Reference
-----------
.. [9] N. Li, T. Li and S. Venkatasubramanian, “t-Closeness: Privacy Beyond k-Anonymity and l-Diversity,” 2007 IEEE 23rd International Conference on Data Engineering, Istanbul, Turkey, 2007, pp. 106-115, doi: 10.1109/ICDE.2007.367856.



Utility Bias
================

The following code snippet assesses whether the data satisfies the utility bias.

We use ``data/presence.csv`` as the original data and ``data/presence_anonymized2.csv`` as the anonymized data to demonstrate how to evaluate this indicator through PETWorks-framework.

In the following code snippet, we use the API ``PETValidation(origin, anonymized, "UtilityBias", processingFunc, maxBias)`` with the original data, the anonymized data, the string "UtilityBias," the processing function, and the maximal acceptable bias to determine whether the data satisfies the utility bias.

Then, we use the API ``report(result, format)`` with the evaluation result and the string "json" as parameters to print the evaluation result in JSON format.

Example: utilityBias.py
-------------------------

.. code-block:: python

    from PETWorks import PETValidation, report
    import pandas as pd

    origin = "data/presence.csv"
    anonymized = "data/presence_anonymized2.csv"


    def averageAge(source):
        data = pd.read_csv(source, sep=";")
        return data["age"].mean()


    result = PETValidation(
        origin, anonymized, "UtilityBias", processingFunc=averageAge, maxBias=2
    )
    report(result, "json")

Execution Result
------------------

.. code-block:: text
    
    $ python3 utilityBias.py
    {
        "UtilityBias": true
    }



De-identification for d-presence
====================================

The following code snippet de-identify the data to satisfy :math:`\delta`-presence [10]_.

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
.. [10] M. E. Nergiz, M. Atzori, and C. Clifton, “Hiding the presence of individuals from shared databases,” Proceedings of the 2007 ACM SIGMOD international conference on Management of data, 2007. 



De-identification for k-anonymity
=======================================

The following code snippet de-identify the data to satisfy k-anonymity [11]_.

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
.. [11] L. Sweeney, “K-anonymity: A model for protecting privacy,” International Journal of Uncertainty, Fuzziness and Knowledge-Based Systems, vol. 10, no. 05, pp. 557–570, 2002. 


De-identification for l-diversity
======================================


The following code snippet de-identify the data to satisfy :math:`l`-diversity [12]_。

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
.. [12] A. Machanavajjhala, J. Gehrke, D. Kifer, and M. Venkitasubramaniam, L-diversity: privacy beyond k-anonymity. 2006. doi: 10.1109/icde.2006.1.



De-identification for t-closeness
======================================

The following code snippet de-identify the data to satisfy t-closeness [13]_.

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
.. [13] N. Li, T. Li and S. Venkatasubramanian, “t-Closeness: Privacy Beyond k-Anonymity and l-Diversity,” 2007 IEEE 23rd International Conference on Data Engineering, Istanbul, Turkey, 2007, pp. 106-115, doi: 10.1109/ICDE.2007.367856.

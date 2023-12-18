+++++++++++++++++++++
Linkalility Attack
+++++++++++++++++++++

This code evaluates the risk of linkability attacks on data using the PETWorks-framework.

For the evaluation, three datasets are utilized: ``data/adults_syn_ctgan.csv`` as the synthetic data, ``data/adults_train.csv`` as the original training data, and ``data/adults_control.csv`` as control data. Additionally, specific auxiliary columns are identified, including combinations like ["type_employer", "fnlwgt"] and ["age"], to enhance the accuracy of the linkability risk assessment.

In this code, the PETWorks API ``PETValidation(synthetic, original, "LinkabilityRisk", control=control, auxiliaryColumns=auxiliaryColumns)`` is used. It takes the synthetic data, original training data, control data, and auxiliary columns as parameters. This API is tailored to assess the risk of linkability attacks, considering the specified auxiliary information.

After the linkability risk evaluation, the report(result, "json") function is utilized. This function, taking the evaluation result and the format parameter "json", outputs the assessment findings. The results are presented in JSON format, providing the success rate of the linkability attack.

Example: linkalilityRisk.py
-------------------------

.. code-block:: python

    from PETWorks import PETValidation, report

    synthetic = "datasets/adult/adults_syn_ctgan.csv"
    original = "datasets/adult/adults_train.csv"
    control = "datasets/adult/adults_control.csv"

    auxiliaryColumns = [
        ["type_employer", "fnlwgt"],
        ["age"]
    ]

    result = PETValidation(
        synthetic,
        original,
        "LinkabilityRisk",
        control=control,
        auxiliaryColumns=auxiliaryColumns,
    )
    report(result, "json")

Execution Result
------------------

.. code-block:: text
    
    $ python3 linkabilityRisk.py
    {
        "Success rate of main attack": 0.001956606593345214,
        "Success rate of baseline attack": 0.004451813975142082,
        "Success rate of control attack": 0.0029546895460639613
    }

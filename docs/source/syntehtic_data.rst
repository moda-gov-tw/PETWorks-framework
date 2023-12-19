++++++++++++++++++++++++++++++
Synthetic Data
++++++++++++++++++++++++++++++


Singling Out Attack
======================

We employ three datasets: ``datasets/adult/adults_syn_ctgan.csv`` as the synthetic data, ``datasets/adult/adults_train.csv`` as the original training data, and ``datasets/adult/adults_control.csv`` as control dataset. This setup is intended to demonstrate the assessment of the singling out attack risk.

In this code, we utilize the PETWorks API ``PETValidation(synthetic, original, "SinglingOutRisk", control)`` with the synthetic data, original training data, and control data as parameters.

Following the risk assessment, we apply the ``report(result, "json")`` function, passing the evaluation result and the format parameter "json". This function will output the evaluation result in JSON format, providing the success rate of the singling out attack.

Example: singlingOutRisk.py
-----------------------------

.. code-block:: python

    from PETWorks import PETValidation, report

    synthetic = "datasets/adult/adults_syn_ctgan.csv"
    original = "datasets/adult/adults_train.csv"
    control = "datasets/adult/adults_control.csv"

    result = PETValidation(synthetic, original, "SinglingOutRisk", control=control)
    report(result, "json")

Execution Result
------------------

.. code-block:: text
    
    $ python3 singlingOutRisk.py
    {
        "Success rate of main attack": 0.2110980494620957,
        "Success rate of baseline attack": 0.037756879139353126,
        "Success rate of control attack": 0.06360101455367315
    }





Inference Attack
====================

We employ three datasets: ``datasets/adult/adults_syn_ctgan.csv`` as the synthetic data, ``datasets/adult/adults_train.csv`` as the original training data, and ``datasets/adult/adults_control.csv`` as control dataset. This setup is intended to demonstrate the assessment of the inference attack risk.

In this code, we utilize the PETWorks API ``PETValidation(synthetic, original, "InferenceRisk", control)`` with the synthetic data, original training data, and control data as parameters.

Following the risk assessment, we apply the ``report(result, "json")`` function, passing the evaluation result and the format parameter "json". This function will output the evaluation result in JSON format, providing the success rate of the inference attack.

Example: inferenceRisk.py
-------------------------

.. code-block:: python

    from PETWorks import PETValidation, report

    synthetic = "datasets/adult/adults_syn_ctgan.csv"
    original = "datasets/adult/adults_train.csv"
    control = "datasets/adult/adults_control.csv"

    result = PETValidation(synthetic, original, "InferenceRisk", control=control)
    report(result, "json")

Execution Result
------------------

.. code-block:: text
    
    $ python3 inferenceRisk.py
    {
        "age": {
            "Success rate of main attack": 0.07961489208090426,
            "Success rate of baseline attack": 0.06666463994121648,
            "Success rate of control attack": 0.06865698642424536
        },
        "type_employer": {
            "Success rate of main attack": 0.48107270841122557,
            "Success rate of baseline attack": 0.4561683773733644,
            "Success rate of control attack": 0.48107270841122557
        },
        "fnlwgt": {
            "Success rate of main attack": 0.03877178917881202,
            "Success rate of baseline attack": 0.05570673428455759,
            "Success rate of control attack": 0.05570673428455759
        }
    }




Linkalility Attack
======================

This code evaluates the risk of linkability attacks on data using the PETWorks-framework.

For the evaluation, three datasets are utilized: ``datasets/adult/adults_syn_ctgan.csv`` as the synthetic data, ``datasets/adult/adults_train.csv`` as the original training data, and ``datasets/adult/adults_control.csv`` as control data. Additionally, specific auxiliary columns are identified, including combinations like ["type_employer", "fnlwgt"] and ["age"], to enhance the accuracy of the linkability risk assessment.

In this code, the PETWorks API ``PETValidation(synthetic, original, "LinkabilityRisk", control=control, auxiliaryColumns)`` is used. It takes the synthetic data, original training data, control data, and auxiliary columns as parameters. This API is tailored to assess the risk of linkability attacks, considering the specified auxiliary information.

After the linkability risk evaluation, the report(result, "json") function is utilized. This function, taking the evaluation result and the format parameter "json", outputs the assessment findings. The results are presented in JSON format, providing the success rate of the linkability attack.

Example: linkalilityRisk.py
-----------------------------

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

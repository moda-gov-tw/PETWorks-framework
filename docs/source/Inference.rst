++++++++++++++++++
Inference Attack
++++++++++++++++++

We employ three datasets: ``data/adults_syn_ctgan.csv`` as the synthetic data, ``data/adults_train.csv`` as the original training data, and ``data/adults_control.csv`` as control dataset. This setup is intended to demonstrate the assessment of the inference attack risk.

In this code, we utilize the PETWorks API ``PETValidation(synthetic, original, "InferenceRisk", control=control)`` with the synthetic data, original training data, and control data as parameters.

Following the risk assessment, we apply the ``report(result, "json")`` function, passing the evaluation result and the format parameter "json". This function will output the evaluation result in JSON format, providing the success rate of the inference attack.

Example: inferenceRisk.py
-------------------------

.. code-block:: python

    from PETWorks import PETValidation, report

    synthetic = "data/adults_syn_ctgan.csv"
    original = "data/adults_train.csv"
    control = "data/adults_control.csv"

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

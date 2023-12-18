+++++++++++++++++++++
Singling Out Attack
+++++++++++++++++++++

We employ three datasets: ``data/adults_syn_ctgan.csv`` as the synthetic data, ``data/adults_train.csv`` as the original training data, and ``data/adults_control.csv`` as control dataset. This setup is intended to demonstrate the assessment of the singling out attack risk.

In this code, we utilize the PETWorks API ``PETValidation(synthetic, original, "SinglingOutRisk", control=control)`` with the synthetic data, original training data, and control data as parameters.

Following the risk assessment, we apply the ``report(result, "json")`` function, passing the evaluation result and the format parameter "json". This function will output the evaluation result in JSON format, providing the success rate of the singling out attack.

Example: singlingOutRisk.py
-------------------------

.. code-block:: python

    from PETWorks import PETValidation, report

    synthetic = "data/adults_syn_ctgan.csv"
    original = "data/adults_train.csv"
    control = "data/adults_control.csv"

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

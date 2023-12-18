+++++++++++++++++++++
Man-in-teh-Middle Attack
+++++++++++++++++++++


We use two datasets for this assessment: ``datasets/synthetic_NHANES.csv`` as the synthetic data, and ``datasets/NHANES.csv`` as the original dataset.

In this code, we apply the PETWorks API ``PETValidation(synthetic, original, "MIATest")``, using the synthetic and original datasets as parameters. This function is designed to determine whether the data is processed without differential privacy or might potentially use differential privacy.

After the assessment, we use the ``report(result, "json")`` function to process and display the results. This function takes the evaluation result and the format parameter "json". It outputs the evaluation in JSON format, with the result indicating whether the dataset is processed without differential privacy or might potentially use differential privacy.

Example: validateDP.py
-------------------------

.. code-block:: python

    from PETWorks import PETValidation, report

    synthetic = "datasets/synthetic_NHANES.csv"
    original = "datasets/NHANES.csv"

    result = PETValidation(synthetic, original, "MIATest")
    report(result, "json")

Execution Result
------------------

.. code-block:: text
    
    $ python3 validateDP.py
    {
        "Does the data processed with differential privacy": "Possibly Yes"
    }


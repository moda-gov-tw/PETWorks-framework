++++++++++++++++++++++++++++
Homomorphic Encryption
++++++++++++++++++++++++++++


Testing Method for Homomorphic Encryption Technology
========================================================


The testing criteria for the "Homomorphic Encryption Technology Testing Method" provide the basis for service providers to adhere to. The testing criteria ensure that service providers meet user requirements while simultaneously ensuring the security of data. This includes data protection scope, defining security levels, key protection, and more. When the services provided by a service provider conform to these testing criteria, it signifies that users can trust that their data is protected by homomorphic encryption technology, and the service provider utilizes all necessary functions.

1. The service provider must clearly define the scope of data protection.
2. The service provider should define security levels and disclose the corresponding encryption strength coefficients.
3. Setting security levels by the service provider requires user consent.
4. User-side keys must be protected using encryption functions that comply with FIPS 140-2 Annex A, with a security level of AES-128 or higher.
5. The service provider should provide software upgrade programs and address encryption format conversion issues arising from upgrades.
6. Communication between client-side and server-side programs must be protected using security protocols of TLS1 or higher.
7. The service provider must not embed keys in the source code.
8. The service provider should utilize all necessary functions for encryption.
9. The service provider should accept functional verification by users.

Generate Key for Homomorphic Encryption
================================================

In the provided example, the ``generateKey.py`` script is demonstrated, which showcases the process of generating encryption keys using the PETWorks framework. This script is focused on creating keys for homomorphic encryption.

In the script, the ``dataProcess`` function is called with parameters specifying the key size (128 bits), the type of encryption (HomomorphicEncryption), the operation (GenerateKey), and the library used (in this case, "phe" for partially homomorphic encryption). This function returns the generated keys.

The ``report`` function is then used to print the keys in JSON format. The format parameter is set to "json", which formats the output in a structured and readable JSON format.

Upon executing the script using ``python3 generateKey.py``, the output displays the generated public and private keys. The public key is a long integer, while the private key is an object containing two integers, 'p' and 'q', which are components of the private key used in homomorphic encryption.

generateKey.py
--------------------
.. code-block:: python

    from PETWorks import dataProcess, report

    library = "phe"
    keySize = 128

    keys = dataProcess(
        keySize, None, "HomomorphicEncryption", "GenerateKey", library=library
    )
    report(keys, "json")


Execution Result
------------------

.. code-block:: text

    $ python3 generateKey.py
    {
        "Public Key": 176498358747162177292711947860102193361,
        "Private Key": {
            "p": 10056745993628924791,
            "q": 17550245264121825271
        }
    }


Encrypt Value Using Homomorphic Encryption
===============================================

In the provided example, the ``encryptValue.py`` script demonstrates how to encrypt a value using the PETWorks framework. This script focuses on employing homomorphic encryption techniques for data encryption.

Initially, the script sets the library to "phe" (indicating partial homomorphic encryption), the key size to 128 bits, and defines the public key value. The value to be encrypted, which is 16 in this case, is then specified.

The ``dataProcess`` function is used to perform the encryption operation. The input parameters include the value to be encrypted, the key size, the type of encryption ("HomomorphicEncryption"), the operation ("Encrypt"), the library ("phe"), and the public key.

Subsequently, the ``report`` function outputs the encrypted value in JSON format. The format parameter is set to "json" to structure the result in a readable and organized JSON format.

When executing ``python3 encryptValue.py``, the output displays the encrypted value, a long integer representing the encrypted data.

encryptValue.py
--------------------
.. code-block:: python

    from PETWorks import dataProcess, report

    library = "phe"
    keySize = 128
    publicKey = 240537853022521961474293276399056393697

    value = 16

    encryptedValue = dataProcess(
        value,
        keySize,
        "HomomorphicEncryption",
        "Encrypt",
        library=library,
        publicKey=publicKey,
    )
    report(encryptedValue, "json")


Execution Result
------------------

.. code-block:: text

    $ python3 encryptValue.py
    {
        "Encrypted Value": 21895940939293354723904335349274645110736347403968508239398892528574591099866
    }


Decrypt Value Using Homomorphic Encryption
=============================================

In the provided example, the ``decryptValue.py`` script illustrates the process of decrypting a value using the PETWorks framework, specifically focusing on homomorphic encryption.

The script sets up several key parameters: the library is set to "phe" for partial homomorphic encryption, the key size is defined as 128 bits, and both the public key and the private key are specified. The private key is an object containing two integer components, 'p' and 'q'.

The ``dataProcess`` function is called to decrypt an encrypted value. The function takes several parameters: the encrypted value, the key size, the encryption type ("HomomorphicEncryption"), the operation ("Decrypt"), the library ("phe"), the public key, and the private key.

After decryption, the ``report`` function is used to display the decrypted value in JSON format. This ensures that the output is structured and readable.

Upon executing the script with ``python3 decryptValue.py``, the output reveals the decrypted value, which in this case is 16. This demonstrates the successful decryption of the previously encrypted value.

decryptValue.py
--------------------
.. code-block:: python

    from PETWorks import dataProcess, report

    library = "phe"
    keySize = 128
    publicKey = 240537853022521961474293276399056393697
    privateKey = {"p": 15077889811522283831, "q": 15953018361939928487}

    encryptedValue = 54460907148015048399650723031319333758655292473353853450480678347318563444904

    decryptedValue = dataProcess(
        encryptedValue,
        keySize,
        "HomomorphicEncryption",
        "Decrypt",
        library=library,
        publicKey=publicKey,
        privateKey=privateKey,
    )
    report(decryptedValue, "json")


Execution Result
------------------

.. code-block:: text

    $ python3 decryptValue.py
    {
        "Decrypted Value": 16
    }

Detect the Use of TLS Protocol (v1.2 or later)
================================================

In the provided example, the ``detectTLS.py`` script is shown, which demonstrates the use of the PETWorks framework to detect the usage of TLS version 1.2 or later in network communication. 

The script first captures network packets using the ``dataProcess`` function with parameters set for "HomomorphicEncryption" and "CapturePackets". This function does not require any input data or key size for this operation.

Once the packets are captured, the ``PETValidation`` function is used to check if TLS version 1.2 or later is being used. The function takes the captured packets as input, with "TLSv1.2OrLater" specified as the parameter for the type of validation.

Finally, the result of this validation is reported in a JSON format using the `report` function. This ensures the output is structured and easily readable.

Upon executing the script with ``python3 detectTLS.py``, the output confirms whether TLS version 1.2 or later is used in the network communication, which, in this case, is shown as true. This indicates that the network communication captured and analyzed by the script is indeed using TLS version 1.2 or a later version.


detectTLS.py
--------------------
.. code-block:: python

    from PETWorks import dataProcess, PETValidation, report

    packets = dataProcess(None, None, "HomomorphicEncryption", "CapturePackets")
    result = PETValidation(packets, None, "TLSv1.2OrLater")
    report(result, "json")


Execution Result
------------------

.. code-block:: text

    $ python3 detectTLS.py
    {
        "Use TLS v1.2 or later": true
    }

Find External Functions
==========================

In the provided example, the ``findExternalFunctions.py`` script demonstrates how to identify external functions used by a given executable using the PETWorks framework. 

The script focuses on analyzing the ``/usr/bin/ls`` executable. The ``dataProcess`` function is called with the path to the executable, and the operation specified as "FindExternalFunctions" under the category of "HomomorphicEncryption". This setup is tailored to process the given executable and identify external function calls it makes.

After processing the executable, the script uses the ``report`` function to output the results in JSON format. This choice ensures that the list of external functions is presented in a structured and readable format.

Upon running the script with ``python3 findExternalFunctions.py``, the output displays a list of external functions that the ``/usr/bin/ls`` executable calls. These functions are identified with their names and the version of the GLIBC library they are associated with (e.g., "abort@GLIBC_2.2.5", "__assert_fail@GLIBC_2.2.5", "bindtextdomain@GLIBC_2.2.5", etc.). This output provides insight into the external dependencies of the executable.

findExternalFunctions.py
----------------------------
.. code-block:: python

    from PETWorks import dataProcess, report

    executable = "/usr/bin/ls"

    result = dataProcess(
        executable, None, "HomomorphicEncryption", "FindExternalFunctions"
    )
    report(result, "json")

Execution Result
------------------

.. code-block:: text

    $ python3 findExternalFunctions.py
    {
        "External Functions": [
            "abort@GLIBC_2.2.5",
            "__assert_fail@GLIBC_2.2.5",
            "bindtextdomain@GLIBC_2.2.5",
            ...
        ]
    }
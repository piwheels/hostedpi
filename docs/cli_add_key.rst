================
hostedpi add-key
================

.. program:: hostedpi-add-key

Add an SSH key from a public key file to one or more Pis

.. code-block:: text

    positional arguments:
      ssh_key_path  The path to an SSH public key file to add to the Pi
      names         The name of the Pis to add keys to

    optional arguments:
      -h, --help    show this help message and exit

Usage
=====

Add your SSH key to one Pi:

.. code-block:: console

    $ hostedpi add-key ~/.ssh/id_rsa.pub mypi
    1 key added to raspberry

Add your SSH key to multiple Pis:

.. code-block:: console

    $ hostedpi add-key ~/.ssh/id_rsa.pub mypi mypi2 pypi3
    0 keys added to mypi
    1 key added to mypi2
    1 key added to mypi3

.. note::
    Keys are counted before and after addition, and de-duplicated, so if the key
    is already found on the Pi, it will show as not having been added, as above.

===================
hostedpi count-keys
===================

.. program:: hostedpi-count-keys

Show the number of SSH keys currently on one or more Pis

.. code-block:: text

    positional arguments:
      names       The names of the Pis to get keys for

    optional arguments:
      -h, --help  show this help message and exit

Usage
=====

Show the number of keys on a Pi:

.. code-block:: console

    $ hostedpi count-keys mypi
    mypi: 4 keys

Show the number of keys on multiple Pis:

.. code-block:: console

    $ hostedpi count-keys mypi mypi2
    mypi: 4 keys
    mypi2: 2 keys

.. note::
    If no names of Pis are given, the key count will be shown for all Pis in the
    account

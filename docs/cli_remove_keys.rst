====================
hostedpi remove-keys
====================

.. program:: hostedpi-remove-keys

Remove all SSH keys from one or more Pis

.. code-block:: text

    positional arguments:
      names       The names of the Pis to remove keys from

    optional arguments:
      -h, --help  show this help message and exit

Usage
=====

Remove all SSH keys from a Pi:

.. code-block:: console

    $ hostedpi remove-keys mypi
    2 keys removed from mypi

Remove all SSH keys from multiple Pis:

.. code-block:: console

    $ hostedpi remove-keys mypi mypi2
    2 keys removed from mypi
    0 keys removed from mypi2

.. note::
    Unlike other commands, there is no implicit targeting of all Pis. Pis must
    be listed explicitly to have keys removed.

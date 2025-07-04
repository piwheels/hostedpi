====================
hostedpi remove-keys
====================

Remove all SSH keys from one or more Pis

Synopsis
========

.. code-block:: text

    hostedpi remove-keys [-h] names [names ...]

Description
===========

.. program:: hostedpi-remove-keys

.. option:: names [names ...]

    The name of the Pis to remove keys from

.. option:: --help

    Show this message and exit

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
    
    Unlike other commands, there is no implicit targeting of all Pis. Pis must be listed explicitly
    to have keys removed.

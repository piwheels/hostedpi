===============
hostedpi reboot
===============

Reboot one or more Pis in the account

Synopsis
========

.. code-block:: text

    hostedpi reboot [-h] [names [names ...]]

Description
===========

.. program:: hostedpi-reboot

.. option:: names [names ...]

    The names of the Pis to reboot

.. option:: --help

    Show this message and exit

Usage
=====

Reboot a Pi:

.. code-block:: console

    $ hostedpi reboot mypi
    mypi rebooted

Reboot multiple Pis:

.. code-block:: console

    $ hostedpi reboot mypi mypi2
    mypi rebooted
    mypi2 rebooted

.. note::
    
    If no names of Pis are given, all Pis in the account will be rebooted

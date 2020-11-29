===============
hostedpi reboot
===============

.. program:: hostedpi-reboot

Reboot one or more Pis in the account

.. code-block:: text

    positional arguments:
      names       The name of the Pi to reboot

    optional arguments:
      -h, --help  show this help message and exit

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

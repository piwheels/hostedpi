============
hostedpi off
============

.. program:: hostedpi-off

Power off one or more Pis in the account

.. code-block:: text

    positional arguments:
      names       The name of the Pi to power off

    optional arguments:
      -h, --help  show this help message and exit

Usage
=====

Power off a Pi:

.. code-block:: console

    $ hostedpi off mypi
    mypi powered off

Power off multiple Pis:

.. code-block:: console

    $ hostedpi off mypi mypi2
    mypi powered off
    mypi2 powered off

.. note::
    If no names of Pis are given, all Pis in the account will be powered off

===========
hostedpi on
===========

.. program:: hostedpi-on

Power on one or more Pis in the account

.. code-block:: text

    positional arguments:
      names       The name of the Pi to power on

    optional arguments:
      -h, --help  show this help message and exit

Usage
=====

Power off a Pi:

.. code-block:: console

    $ hostedpi on mypi
    mypi powered on

Power off multiple Pis:

.. code-block:: console

    $ hostedpi on mypi mypi2
    mypi powered on
    mypi2 powered on

.. note::
    If no names of Pis are given, all Pis in the account will be powered on

===========
hostedpi on
===========

Power on one or more Pis in the account

Synopsis
========

.. code-block:: text

    hostedpi on [-h] [names [names ...]]

Description
===========

.. program:: hostedpi-on

.. option:: names [names ...]

    The name of the Pi to power on

.. option:: --help

    Show this message and exit

Usage
=====

Power on a Pi:

.. code-block:: console

    $ hostedpi on mypi
    mypi powered on

Power on multiple Pis:

.. code-block:: console

    $ hostedpi on mypi mypi2
    mypi powered on
    mypi2 powered on

.. note::
    
    If no names of Pis are given, all Pis in the account will be powered on

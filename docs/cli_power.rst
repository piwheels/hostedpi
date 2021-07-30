==============
hostedpi power
==============

Get the power status for one or more Pis

Synopsis
========

.. code-block:: text

    hostedpi power [-h] [names [names ...]]

Description
===========

.. program:: hostedpi-power

.. option:: names [names ...]

    The names of the Pis to get the power status for

.. option:: -h, --help

    Show this help message and exit

Usage
=====

Get the power status for a Pi:

.. code-block:: console

    $ hostedpi power mypi
    mypi: powered off

Show the number of keys on multiple Pis:

.. code-block:: console

    $ hostedpi power mypi mypi2 mypi3
    mypi: powered off
    mypi2: powered on
    mypi3: powered on

.. note::
    
    If no names of Pis are given, the power status will be shown for all Pis in
    the account

============
hostedpi off
============

Power off one or more Pis in the account

Synopsis
========

.. code-block:: text

    hostedpi off [-h] [names [names ...]]

Description
===========

.. program:: hostedpi-off

.. option:: names [names ...]

    The name of the Pi to power off

.. option:: -h, --help

    Show this help message and exit

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

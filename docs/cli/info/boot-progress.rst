===========================
hostedpi info boot-progress
===========================

.. program:: hostedpi-info-boot-progress

Get the boot progress of a Raspberry Pi server

.. code-block:: text

    Usage: hostedpi info boot-progress [OPTIONS] NAME

Arguments
=========

.. option:: name [str]

    Name of the Raspberry Pi server

Options
=======

.. option:: --help

    Show this message and exit

Usage
=====

Get the boot progress of a Pi:

.. code-block:: console

    $ hostedpi info boot-progress mypi
    booting

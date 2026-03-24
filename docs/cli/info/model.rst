===================
hostedpi info model
===================

.. program:: hostedpi-info-model

Get the model of a Raspberry Pi server

.. code-block:: text

    Usage: hostedpi info model [OPTIONS] NAME

Arguments
=========

.. option:: name [str]

    Name of the Raspberry Pi server

Options
=======

.. option:: --full

    Show the full model name of the Raspberry Pi server

.. option:: --help

    Show this message and exit

Usage
=====

Get the model number of a Pi:

.. code-block:: console

    $ hostedpi info model mypi
    3

Get the full model name of a Pi:

.. code-block:: console

    $ hostedpi info model mypi --full
    3B+

=================
hostedpi info nic
=================

.. program:: hostedpi-info-nic

Get the network interface speed of a Raspberry Pi server

.. code-block:: text

    Usage: hostedpi info nic [OPTIONS] NAME

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

Get the NIC speed of a Pi:

.. code-block:: console

    $ hostedpi info nic mypi
    1 Gbps

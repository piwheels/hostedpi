========================
hostedpi info ip-address
========================

.. program:: hostedpi-info-ip-address

Get the IPv6 address of a Raspberry Pi server

.. code-block:: text

    Usage: hostedpi info ip-address [OPTIONS] NAME

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

Get the IPv6 address of a Pi:

.. code-block:: console

    $ hostedpi info ip-address mypi
    2a00:1098:8:14b::1

.. warning::

    You will need IPv6 connectivity to connect using the IPv6 address.

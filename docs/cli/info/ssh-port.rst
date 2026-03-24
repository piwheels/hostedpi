======================
hostedpi info ssh-port
======================

.. program:: hostedpi-info-ssh-port

Get the IPv4 SSH port of a Raspberry Pi server

.. code-block:: text

    Usage: hostedpi info ssh-port [OPTIONS] NAME

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

Get the IPv4 SSH port of a Pi:

.. code-block:: console

    $ hostedpi info ssh-port mypi
    5091

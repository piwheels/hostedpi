===========================
hostedpi info ipv4-ssh-port
===========================

.. program:: hostedpi-info-ipv4-ssh-port

Get the IPv4 SSH port of a Raspberry Pi server

.. code-block:: text

    Usage: hostedpi info ipv4-ssh-port [OPTIONS] NAME

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

    $ hostedpi info ipv4-ssh-port mypi
    5091

==========================
hostedpi info ssh-hostname
==========================

.. program:: hostedpi-info-ssh-hostname

Get the SSH hostname of a Raspberry Pi server

.. code-block:: text

    Usage: hostedpi info ssh-hostname [OPTIONS] NAME

Arguments
=========

.. option:: name [str]

    Name of the Raspberry Pi server

Options
=======

.. option:: --ipv6

    Use the IPv6 connection method

.. option:: --help

    Show this message and exit

Usage
=====

Get the IPv4 SSH hostname of a Pi:

.. code-block:: console

    $ hostedpi info ssh-hostname mypi
    ssh.mypi.hostedpi.com

Get the IPv6 SSH hostname of a Pi:

.. code-block:: console

    $ hostedpi info ssh-hostname mypi --ipv6
    mypi.hostedpi.com

.. warning::

    You will need IPv6 connectivity to connect using the IPv6 hostname.

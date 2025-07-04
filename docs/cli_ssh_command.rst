====================
hostedpi ssh command
====================

.. program:: hostedpi-ssh-command

Get the SSH command to connect to a Raspberry Pi server

.. code-block:: text

    Usage: hostedpi ssh command [OPTIONS] NAME

Arguments
=========

.. option:: name [str]

    Name of the Raspberry Pi server to get the SSH command for

Options
=======

.. option:: --ipv6

    Use the IPv6 connection method

.. option:: --help

    Show this message and exit

Usage
=====

Output the IPv4 SSH command for a Pi:

.. code-block:: console

    $ hostedpi ssh command mypi
    ssh -p 5091 root@ssh.mypi.hostedpi.com

Output the IPv6 SSH command for a Pi:

.. code-block:: console

    $ hostedpi ssh command mypi --ipv6
    ssh root@[2a00:1098:8:5b::1]
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
    ssh root@mypi.hostedpi.com

.. note::

    You will need to have an SSH key on the Pi to be able to connect. This can be done when the Pi
    is provisioned with :doc:`../create` or added later with :doc:`keys/add`.

SSH directly onto a Pi:

.. code-block:: console

    $ $(hostedpi ssh command mypi)

.. warning:: 

    This will not work if ``HOSTEDPI_LOG_LEVEL`` is set to ``DEBUG`` as the logging output will
    obscure the SSH command.
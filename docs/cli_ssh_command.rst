====================
hostedpi ssh-command
====================

.. program:: hostedpi-ssh-command

Output the SSH command for one or more Pis in the account

.. code-block:: text

    positional arguments:
      names       The names of the Pis to get SSH commands for

    optional arguments:
      -h, --help  show this help message and exit
      --ipv6      Show IPv6 command

Usage
=====

Output the IPv4 SSH command for a Pi:

.. code-block:: console

    $ hostedpi ssh-command mypi
    ssh -p 5091 root@ssh.mypi.hostedpi.com

Output the IPv6 SSH command for a Pi:

.. code-block:: console

    $ hostedpi ssh-command mypi --ipv6
    ssh root@[2a00:1098:8:5b::1]

Show the number of keys on multiple Pis:

.. code-block:: console

    $ hostedpi ssh-command mypi mypi2
    ssh -p 5091 root@ssh.mypi.hostedpi.com
    ssh -p 5091 root@ssh.mypi2.hostedpi.com

.. note::
    If no names of Pis are given, the key count will be shown for all Pis in the
    account

Execute the SSH command directly:

.. code-block:: console

    $ $(hostedpi ssh-command mypi)

.. warning::
    Use with caution

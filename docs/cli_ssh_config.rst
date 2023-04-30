===================
hostedpi ssh-config
===================

Output the SSH config for one or more Pis in the account

Synopsis
========

.. code-block:: text

    hostedpi ssh-config [-h] [--ipv6] [names [names ...]]

Description
===========

.. program:: hostedpi-ssh-config

.. option:: names [names ...]

    The name of the Pis to add keys to

.. option:: -h, --help

    Show this help message and exit

.. option:: --ipv6

    Use IPv6 connection details

Usage
=====

Output the IPv4 SSH config for a Pi:

.. code-block:: console

    $ hostedpi ssh-config mypi
    Host mypi
        user root
        port 5224
        hostname ssh.mypi.hostedpi.com

Output the IPv6 SSH config for a Pi:

.. code-block:: console

    $ hostedpi ssh-config mypi --ipv6
    Host mypi
        user root
        hostname 2a00:1098:8:5b::1

Output the IPv4 SSH config for multiple Pis:

.. code-block:: console

    $ hostedpi ssh-config mypi mypi2
    Host mypi
        user root
        port 5224
        hostname ssh.mypi.hostedpi.com
    Host mypi2
        user root
        port 5072
        hostname ssh.mypi2.hostedpi.com

.. note::

    If no names of Pis are given, the SSH commands will be shown for all Pis in the account

Save (append) the IPv4 SSH config for all Pis in the account into your SSH
config file:

.. code-block:: console

    $ hostedpi ssh-config >> ~/.ssh/config

.. note::

    Read more about the SSH config file: https://www.ssh.com/ssh/config/

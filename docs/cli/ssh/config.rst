===================
hostedpi ssh config
===================

.. program:: hostedpi-ssh config

Get the SSH config to connect to one or more Raspberry Pi servers

.. code-block:: text

    Usage: hostedpi ssh config [OPTIONS] [NAMES]...

Arguments
=========

.. option:: names [str ...]

    Names of the Raspberry Pi servers to get SSH config for

Options
=======

.. option:: --filter [str]

    Search pattern for filtering server names

.. option:: --ipv6

    Use the IPv6 connection method

.. option:: --help

    Show this message and exit

Usage
=====

The SSH config file is a convenient way to store SSH connection information for multiple hosts. It
allows you to connect to a host using a simple command like `ssh mypi` instead of typing the full
command every time.

It is generally useful to redirect the output of this command to your SSH config file, which is
usually located at `~/.ssh/config`. Outputting to the terminal is useful for copy-pasting, but
redirecting to the config file allows you to automate the process. You will need to prune this file
as you provision and deprovision Pis.

Output the IPv4 SSH config for a Pi:

.. code-block:: console

    $ hostedpi ssh config mypi
    Host mypi
        user root
        port 5224
        hostname ssh.mypi.hostedpi.com

Output the IPv6 SSH config for a Pi:

.. code-block:: console

    $ hostedpi ssh config mypi --ipv6
    Host mypi
        user root
        hostname mypi.hostedpi.com

Output the IPv4 SSH config for multiple Pis:

.. code-block:: console

    $ hostedpi ssh config mypi mypi2
    Host mypi
        user root
        port 5224
        hostname ssh.mypi.hostedpi.com
    Host mypi2
        user root
        port 5072
        hostname ssh.mypi2.hostedpi.com

Save (append) the IPv4 SSH config for all Pis in the account into your SSH config file:

.. code-block:: console

    $ hostedpi ssh config >> ~/.ssh/config

.. note::

    Read more about the SSH config file: https://www.ssh.com/ssh/config/

=======================
hostedpi ssh keys purge
=======================

.. program:: hostedpi-ssh-keys-purge

Remove all SSH keys from one or more Raspberry Pi servers

.. code-block:: text

    Usage: hostedpi ssh keys purge [OPTIONS] [NAMES]...

Arguments
=========

.. option:: names [str ...]

    Name of the Raspberry Pi servers to purge SSH keys from

Options
=======

.. option:: --filter [str]

    Search pattern for filtering server names

.. option:: --help

    Show this message and exit

Usage
=====

Purge all SSH keys from a Pi:

.. code-block:: console

    $ hostedpi ssh keys purge mypi
    Removed all keys from mypi

Purge all SSH keys from multiple Pis:

.. code-block:: console

    $ hostedpi ssh keys purge mypi mypi2 mypi3
    Removed 2 keys from mypi
    Removed 3 keys from mypi2
    Removed 1 key from mypi3

Purge all SSH keys from all Pis matching a filter:

.. code-block:: console

    $ hostedpi ssh keys purge --filter mypi
    Removed 2 keys from mypi
    Removed 3 keys from mypi2
    Removed 1 key from mypi3
    Removed 2 keys from mypi4

Purge all SSH keys from all Pis:

.. code-block:: console

    $ hostedpi ssh keys purge --filter mypi
    Removed 2 keys from mypi
    Removed 3 keys from mypi2
    Removed 1 key from mypi3
    Removed 2 keys from mypi4

Purge all SSH keys from all Pis:

.. code-block:: console

    $ hostedpi ssh keys purge
    Removed 2 keys from mypi
    Removed 3 keys from mypi2
    Removed 1 key from mypi3
    Removed 2 keys from mypi4
    Removed 1 key from anotherpi
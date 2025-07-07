=============
hostedpi list
=============

.. program:: hostedpi-list

List Raspberry Pi servers

.. code-block:: text

    Usage: hostedpi list [OPTIONS] [NAMES]...

Arguments
=========

.. option:: names

    Names of the Raspberry Pi servers

Options
=======

.. option:: --filter [str]

    Search pattern for filtering server names

.. option:: --help

    Show this message and exit

Usage
=====

List all Pis in the account:

.. code-block:: console

    $ hostedpi list
    mypi
    mypi2
    bob1
    bob2

Filter by a search pattern:

.. code-block:: console

    $ hostedpi list --filter bob
    bob1
    bob2
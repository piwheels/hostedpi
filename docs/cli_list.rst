=============
hostedpi list
=============

List Raspberry Pi servers

Synopsis
========

.. code-block:: text

    hostedpi list [-h]

Description
===========

.. program:: hostedpi-list

.. option:: names

    Names of the Raspberry Pi servers

.. option:: --filter

    Search pattern for filtering results

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
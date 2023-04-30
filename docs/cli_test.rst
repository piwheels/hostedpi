=============
hostedpi test
=============

Test a connection to the Mythic Beasts API using API ID and secret in environment variables

Synopsis
========

.. code-block:: text

    hostedpi test [-h]

Description
===========

.. program:: hostedpi-test

.. option:: -h, --help

    Show this help message and exit

Usage
=====

Successful test:

.. code-block:: console

    $ hostedpi test
    Connected to the Mythic Beasts API

An error will be shown if the connection fails:

.. code-block:: console

    $ hostedpi test
    hostedpi error: Failed to authenticate

.. note::
    
    See the :doc:`getting_started` section for details on how to authenticate

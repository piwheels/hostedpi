=============
hostedpi test
=============

Test a connection to the Mythic Beasts API using API ID and secret, using configuration as described
in the :doc:`getting_started` section.

Synopsis
========

.. code-block:: text

    hostedpi test [-h]

Description
===========

.. program:: hostedpi-test

.. option:: --help

    Show this message and exit

Usage
=====

Successful test:

.. code-block:: console

    $ hostedpi test
    Connected to the Mythic Beasts API

An error will be shown if the connection fails:

.. code-block:: console

    $ hostedpi test
    Failed to authenticate

.. note::
    
    See the :doc:`getting_started` section for details on how to authenticate

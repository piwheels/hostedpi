===============
hostedpi status
===============

.. program:: hostedpi-status

Get the provision status of one or more Pis

.. code-block:: text

    positional arguments:
      names       The names of the Pis to get the provision status for

    optional arguments:
      -h, --help  show this help message and exit

Usage
=====

Get the provision status of a Pi:

.. code-block:: console

    $ hostedpi status mypi
    mypi: live

Get the provision status of multiple Pis:

.. code-block:: console

    $ hostedpi status mypi mypi2
    mypi: live
    mypi2: provisioning

.. note::
    If no names of Pis are given, the provision status will be shown for all Pis
    in the account

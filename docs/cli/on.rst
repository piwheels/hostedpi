===========
hostedpi on
===========

.. program:: hostedpi-on

Power on one or more Raspberry Pi servers

.. code-block:: text

    Usage: hostedpi on [OPTIONS] [NAMES]...

Arguments
=========

.. option:: names [str ...]

    Names of the Raspberry Pi servers to power on

    If no names are given, all Pis in the account will be powered on

Options
=======

.. option:: --filter [str]

    Search pattern for filtering server names

.. option:: --help

    Show this message and exit

Usage
=====

Power on a Pi:

.. code-block:: console

    $ hostedpi on mypi
    ┏━━━━━━━┳━━━━━━━━━━━━━┓
    ┃ Name  ┃ Status      ┃
    ┡━━━━━━━╇━━━━━━━━━━━━━┩
    │ mypi  │ Powering on │
    └───────┴─────────────┘

Power on multiple Pis by name:

.. code-block:: console

    $ hostedpi on mypi mypi2
    ┏━━━━━━━┳━━━━━━━━━━━━━┓
    ┃ Name  ┃ Status      ┃
    ┡━━━━━━━╇━━━━━━━━━━━━━┩
    │ mypi  │ Powering on │
    │ mypi2 │ Powering on │
    └───────┴─────────────┘

Power on multiple Pis with a filter:

.. code-block:: console

    $ hostedpi on --filter mypi
    ┏━━━━━━━┳━━━━━━━━━━━━━┓
    ┃ Name  ┃ Status      ┃
    ┡━━━━━━━╇━━━━━━━━━━━━━┩
    │ mypi  │ Powering on │
    │ mypi2 │ Powering on │
    │ mypi3 │ Powering on │
    │ mypi4 │ Powering on │
    └───────┴─────────────┘

.. note::
    
    If no names of Pis are given, all Pis in the account will be powered on

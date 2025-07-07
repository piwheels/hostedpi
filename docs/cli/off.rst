=============
hostedpi off
=============

.. program:: hostedpi-off

Power off one or more Raspberry Pi servers

.. code-block:: text

    Usage: hostedpi off [OPTIONS] [NAMES]...

Arguments
=========

.. option:: names [str ...]

    Names of the Raspberry Pi servers to power off

    If no names are given, all Pis in the account will be powered off

Options
=======

.. option:: --filter [str]

    Search pattern for filtering server names

.. option:: --help

    Show this message and exit

Usage
=====

Power off a Pi:

.. code-block:: console

    $ hostedpi off mypi
    ┏━━━━━━━┳━━━━━━━━━━━━━━┓
    ┃ Name  ┃ Status       ┃
    ┡━━━━━━━╇━━━━━━━━━━━━━━┩
    │ mypi  │ Powering off │
    └───────┴──────────────┘

Power off multiple Pis by name:

.. code-block:: console

    $ hostedpi off mypi mypi2
    ┏━━━━━━━┳━━━━━━━━━━━━━━┓
    ┃ Name  ┃ Status       ┃
    ┡━━━━━━━╇━━━━━━━━━━━━━━┩
    │ mypi  │ Powering off │
    │ mypi2 │ Powering off │
    └───────┴──────────────┘

Power off multiple Pis with a filter:

.. code-block:: console

    $ hostedpi off --filter mypi
    ┏━━━━━━━┳━━━━━━━━━━━━━━┓
    ┃ Name  ┃ Status       ┃
    ┡━━━━━━━╇━━━━━━━━━━━━━━┩
    │ mypi  │ Powering off │
    │ mypi2 │ Powering off │
    │ mypi3 │ Powering off │
    │ mypi4 │ Powering off │
    └───────┴──────────────┘

.. note::

    If no names of Pis are given, all Pis in the account will be powered off

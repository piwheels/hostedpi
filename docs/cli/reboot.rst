===============
hostedpi reboot
===============

.. program:: hostedpi-on

Reboot one or more Raspberry Pi servers

.. code-block:: text

    Usage: hostedpi reboot [OPTIONS] [NAMES]...

Arguments
=========

.. option:: names [str ...]

    Names of the Raspberry Pi servers to reboot

    If no names are given, all Pis in the account will be rebooted

Options
=======

.. option:: --filter [str]

    Search pattern for filtering server names

.. option:: --help

    Show this message and exit

Usage
=====

Reboot a Pi:

.. code-block:: console

    $ hostedpi reboot mypi
    ┏━━━━━━┳━━━━━━━━━━━┓
    ┃ Name ┃ Status    ┃
    ┡━━━━━━╇━━━━━━━━━━━┩
    │ mypi │ Rebooting │
    └──────┴───────────┘

Reboot multiple Pis by name:

.. code-block:: console

    $ hostedpi reboot mypi mypi2
    ┏━━━━━━┳━━━━━━━━━━━┓
    ┃ Name ┃ Status    ┃
    ┡━━━━━━╇━━━━━━━━━━━┩
    │ mypi │ Rebooting │
    │ mypi2│ Rebooting │
    └──────┴───────────┘

Reboot multiple Pis with a filter:

.. code-block:: console

    $ hostedpi reboot --filter mypi
    ┏━━━━━━┳━━━━━━━━━━━┓
    ┃ Name ┃ Status    ┃
    ┡━━━━━━╇━━━━━━━━━━━┩
    │ mypi │ Rebooting │
    │ mypi2│ Rebooting │
    │ mypi3│ Rebooting │
    │ mypi4│ Rebooting │
    └──────┴───────────┘

.. note::
    
    If no names of Pis are given, all Pis in the account will be rebooted

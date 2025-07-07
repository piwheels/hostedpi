===============
hostedpi status
===============

.. program:: hostedpi-status

Get the current status of one or more Raspberry Pi servers

.. code-block:: text

    Usage: hostedpi status [OPTIONS] [NAMES]...

Arguments
=========

.. option:: names [names ...]

    Names of the Raspberry Pi servers to check the status of

Options
=======

.. option:: --filter [str]

    Search pattern for filtering server names

.. option:: --help

    Show this message and exit

Usage
=====

Get the provision status of a Pi:

.. code-block:: console

    $ hostedpi status mypi2
    ┏━━━━━━━┳━━━━━━━━━━━━┓
    ┃ Name  ┃ Status     ┃
    ┡━━━━━━━╇━━━━━━━━━━━━┩
    │ mypi2 │ Powered on │
    └───────┴────────────┘

Get the provision status of multiple Pis:

.. code-block:: console

    $ hostedpi status mypi2 mypi3
    ┏━━━━━━━┳━━━━━━━━━━━━┓
    ┃ Name  ┃ Status     ┃
    ┡━━━━━━━╇━━━━━━━━━━━━┩
    │ mypi2 │ Powered on │
    │ mypi3 │ Powered on │
    └───────┴────────────┘

Get the provision status of multiple Pis with a filter:

.. code-block:: console

    $ hostedpi status --filter bob
    ┏━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃ Name ┃ Status                   ┃
    ┡━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━┩
    │ bob1 │ Powered on               │
    │ bob2 │ Provisioning: installing │
    └──────┴──────────────────────────┘

Get the provision status of all Pis in the account:

.. code-block:: console

    $ hostedpi status
    ┏━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃ Name            ┃ Status                   ┃
    ┡━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━┩
    │ bob1            │ Provisioning: installing │
    │ bob2            │ Booting: Boot failed     │
    │ mypi            │ Powered on               │
    │ mypi2           │ Powered on               │
    │ mypi3           │ Powered on               │
    │ mypi4           │ Powered on               │
    │ apacheserver123 │ Powered off              │
    └─────────────────┴──────────────────────────┘

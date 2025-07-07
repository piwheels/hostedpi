==============
hostedpi table
==============

.. program:: hostedpi-table

List Raspberry Pi server information in a table

.. code-block:: text

    Usage: hostedpi table [OPTIONS] [NAMES]...

Arguments
=========

.. option:: names

    Names of the Raspberry Pi servers to list

Options
=======

.. option:: --filter [str]

    Search pattern for filtering server names

.. option:: --full

    Show full table of Raspberry Pi server info

    This includes more columns, and requires a separate API request per server

.. option:: --help

    Show this message and exit

Usage
=====

List all Pis in the account in a table:

.. code-block:: console

    $ hostedpi table
    ┏━━━━━━━┳━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━┓
    ┃ Name  ┃ Model ┃ Memory ┃ CPU Speed ┃
    ┡━━━━━━━╇━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━┩
    │ mypi  │ 3     │ 1 GB   │ 1.2 GHz   │
    │ mypi2 │ 4     │ 4 GB   │ 1.5 GHz   │
    │ mypi3 │ 4     │ 4 GB   │ 1.5 GHz   │
    │ mypi4 │ 4     │ 8 GB   │ 2.0 GHz   │
    │ bob1  │ 4     │ 8 GB   │ 2.0 GHz   │
    │ bob2  │ 4     │ 8 GB   │ 2.0 GHz   │
    └───────┴───────┴────────┴───────────┘

List a number of Pis by name:

.. code-block:: console

    $ hostedpi table mypi mypi2
    ┏━━━━━━━┳━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━┓
    ┃ Name  ┃ Model ┃ Memory ┃ CPU Speed ┃
    ┡━━━━━━━╇━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━┩
    │ mypi  │ 3     │ 1 GB   │ 1.2 GHz   │
    │ mypi2 │ 4     │ 4 GB   │ 1.5 GHz   │
    └───────┴───────┴────────┴───────────┘

Filter by a search pattern:

.. code-block:: console

    $ hostedpi table --filter bob
    ┏━━━━━━━┳━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━┓
    ┃ Name  ┃ Model ┃ Memory ┃ CPU Speed ┃
    ┡━━━━━━━╇━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━┩
    │ bob1  │ 4     │ 8 GB   │ 2.0 GHz   │
    │ bob2  │ 4     │ 8 GB   │ 2.0 GHz   │
    └───────┴───────┴────────┴───────────┘

Show the full table of information for each named Pi:

.. code-block:: console

    $ hostedpi table mypi3 mypi4 --full
    ┏━━━━━━━┳━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
    ┃ Name  ┃ Model ┃ Memory ┃ CPU Speed ┃ NIC Speed ┃ Disk size ┃ Status     ┃ Initialised keys ┃ IPv4 SSH port ┃
    ┡━━━━━━━╇━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
    │ mypi3 │ 3B    │ 1 GB   │ 1.2 GHz   │ 100 Mbps  │ 10 GB     │ Powered on │ No               │ 5142          │
    │ mypi4 │ 4B    │ 8 GB   │ 2.0 GHz   │ 1 Gbps    │ 60 GB     │ Powered on │ Yes              │ 5423          │
    └───────┴───────┴────────┴───────────┴───────────┴───────────┴────────────┴──────────────────┴───────────────┘

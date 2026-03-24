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

    Show all available columns in the table

    Equivalent to enabling all column options below

.. option:: --model

    Show model column in table

.. option:: --memory

    Show memory column in table

.. option:: --cpu

    Show CPU speed column in table

.. option:: --disk

    Show disk size column in table

.. option:: --nic

    Show NIC speed column in table

.. option:: --status

    Show status column in table

.. option:: --boot-progress

    Show boot progress column in table

.. option:: --ipv4-ssh-port

    Show IPv4 SSH port column in table

.. option:: --ip-address

    Show IPv6 address column in table

.. option:: --location

    Show location column in table

.. option:: --power

    Show power state column in table

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

Show specific columns:

.. code-block:: console

    $ hostedpi table --status --disk --location
    ┏━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━┓
    ┃ Name  ┃ Status     ┃ Disk size ┃ Location ┃
    ┡━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━┩
    │ mypi  │ Powered on │ 10 GB     │ CLL      │
    │ mypi2 │ Powered on │ 20 GB     │ CLL      │
    └───────┴────────────┴───────────┴──────────┘

Show all available columns:

.. code-block:: console

    $ hostedpi table mypi3 mypi4 --full
    ┏━━━━━━━┳━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━┓
    ┃ Name  ┃ Model ┃ Memory ┃ CPU Speed ┃ NIC Speed ┃ Disk size ┃ Status     ┃ Boot Progress ┃ IPv4 SSH port ┃ IPv6 Address      ┃ Location ┃ Power ┃
    ┡━━━━━━━╇━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━┩
    │ mypi3 │ 4B    │ 1 GB   │ 1.2 GHz   │ 100 Mbps  │ 10 GB     │ Powered on │ booted        │ 5142          │ 2a00:1098:8:68::1 │ CLL      │ True  │
    │ mypi4 │ 4B    │ 8 GB   │ 2.0 GHz   │ 1 Gbps    │ 60 GB     │ Powered on │ booted        │ 5423          │ 2a00:1098:8:68::2 │ CLL      │ True  │
    └───────┴───────┴────────┴───────────┴───────────┴───────────┴────────────┴───────────────┴───────────────┴───────────────────┴──────────┴───────┘


.. note::

    The default view of the table is fast to load, as it does not require fetching all details for
    each server. Requesting additional columns may result in a longer loading time, as more
    information needs to be retrieved from the API for each server.
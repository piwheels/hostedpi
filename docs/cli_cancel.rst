===============
hostedpi cancel
===============

.. program:: hostedpi-cancel

Unprovision one or more Raspberry Pi servers

.. code-block:: text

    Usage: hostedpi cancel [OPTIONS] [NAMES]...

Arguments
=========

.. option:: names [str ...]

    Names of the Raspberry Pi servers to cancel

    If no names are given, all Pis in the account will be cancelled

Options
=======

.. option:: --filter [str]

    Search pattern for filtering server names

.. option:: -y --yes

    Proceed without confirmation

.. option:: --help

    Show this message and exit

Usage
=====

Cancel a Pi:

.. code-block:: console

    $ hostedpi cancel mypi
    Are you sure you want to cancel mypi? [y/N] y
    ┏━━━━━━┳━━━━━━━━━━━┓
    ┃ Name ┃ Status    ┃
    ┡━━━━━━╇━━━━━━━━━━━┩
    │ mypi │ Cancelled │
    └──────┴───────────┘

.. note::
    You can cancel by entering ``n`` or interrupting with ``Ctrl + C``.

Cancel multiple Pis by name:

.. code-block:: console

    $ hostedpi cancel mypi mypi2
    Are you sure you want to cancel mypi, mypi2? [y/N]
    ┏━━━━━━━┳━━━━━━━━━━━┓
    ┃ Name  ┃ Status    ┃
    ┡━━━━━━━╇━━━━━━━━━━━┩
    │ mypi  │ Cancelled │
    │ mypi2 │ Cancelled │
    └───────┴───────────┘

Cancel multiple Pis with a filter:

.. code-block:: console

    $ hostedpi cancel --filter mypi
    Are you sure you want to cancel mypi, mypi2, mypi3, mypi4? [y/N]
    ┏━━━━━━━┳━━━━━━━━━━━┓
    ┃ Name  ┃ Status    ┃
    ┡━━━━━━━╇━━━━━━━━━━━┩
    │ mypi  │ Cancelled │
    │ mypi2 │ Cancelled │
    │ mypi3 │ Cancelled │
    │ mypi4 │ Cancelled │
    └───────┴───────────┘

Cancel a Pi without the confirmation step:

.. code-block:: console

    $ hostedpi cancel mypi -y
    mypi cancelled
    ┏━━━━━━┳━━━━━━━━━━━┓
    ┃ Name ┃ Status    ┃
    ┡━━━━━━╇━━━━━━━━━━━┩
    │ mypi │ Cancelled │
    └──────┴───────────┘

.. warning::
    
    Be careful!

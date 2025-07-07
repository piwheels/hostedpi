=======================
hostedpi ssh keys table
=======================

.. program:: hostedpi-ssh-keys-table

List the SSH keys on a Raspberry Pi server in a table format

.. code-block:: text

    Usage: hostedpi ssh keys table [OPTIONS] NAME

Arguments
=========

.. option:: name [str] [required]

    Name of the Raspberry Pi server to list SSH keys for

Options
=======

.. option:: --filter [str]

    Search pattern for filtering server names

.. option:: --help

    Show this message and exit

Usage
=====

List keys on a Pi:

.. code-block:: console

    $ hostedpi ssh keys table mypi3
    ┏━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃ Type    ┃ Label     ┃ Note                        ┃
    ┡━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
    │ ssh-rsa │ ben@fern  │                             │
    │ ssh-rsa │ dave@home │                             │
    │ ssh-rsa │ ben@jake  │ ssh-import-id gh:bennuttall │
    └─────────┴───────────┴─────────────────────────────┘

.. note::

    The last example includes a comment indicating that the key was imported from GitHub using the
    :doc:`import` command. We refer to the ``ben@jake`` part as the label.

    Keys can be removed by label using the :doc:`remove` command, and imported keys can be removed
    using the :doc:`unimport` command.
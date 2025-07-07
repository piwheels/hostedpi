========================
hostedpi ssh keys remove
========================

.. program:: hostedpi-ssh-keys-remove

Remove an SSH key from one or more Raspberry Pi servers

.. code-block:: text

    Usage: hostedpi ssh keys remove [OPTIONS] LABEL [NAMES]...

Arguments
=========

.. option:: label [str] [required]

    Label for the SSH key, e.g. ``ben@finn``

.. option:: names [str ...]

    Names of the Raspberry Pi servers to remove SSH keys from

Options
=======

.. option:: --filter [str]

    Search pattern for filtering server names

.. option:: --help

    Show this message and exit

Usage
=====

Remove an SSH key from a Pi:

.. code-block:: console

    $ hostedpi ssh keys remove ben@finn mypi
    Removed 'ben@finn' key from mypi3

Remove an SSH key from multiple Pis:

.. code-block:: console

    $ hostedpi ssh keys remove ben@finn mypi mypi2 mypi3
    Removed 'ben@finn' key from mypi
    Removed 'ben@finn' key from mypi2
    Removed 'ben@finn' key from mypi3

Remove an SSH key from all Pis matching a filter:

.. code-block:: console

    $ hostedpi ssh keys remove ben@finn --filter mypi
    Removed 'ben@finn' key from mypi
    Removed 'ben@finn' key from mypi2
    Removed 'ben@finn' key from mypi3
    Removed 'ben@finn' key from mypi4

Remove an SSH key from all Pis:

.. code-block:: console

    $ hostedpi ssh keys remove ben@finn
    Removed 'ben@finn' key from mypi
    Removed 'ben@finn' key from mypi2
    Removed 'ben@finn' key from mypi3
    Removed 'ben@finn' key from mypi4
    Removed 'ben@finn' key from anotherpi
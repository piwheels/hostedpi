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

Remove all SSH keys from a Pi:

.. code-block:: console

    $ hostedpi remove-keys mypi
    2 keys removed from mypi

Remove all SSH keys from multiple Pis:

.. code-block:: console

    $ hostedpi remove-keys mypi mypi2
    2 keys removed from mypi
    0 keys removed from mypi2

.. note::
    
    Unlike other commands, there is no implicit targeting of all Pis. Pis must be listed explicitly
    to have keys removed.

==========================
hostedpi ssh keys unimport
==========================

.. program:: hostedpi-ssh-keys-unimport

Remove imported SSH keys from one or more Raspberry Pi servers

.. code-block:: text

    Usage: hostedpi ssh keys unimport [OPTIONS] [NAMES]...

Arguments
=========

.. option:: names [str ...]

    Names of the Raspberry Pi server to remove SSH keys from

Options
=======

.. option:: --filter [str]

    Search pattern for filtering server names

.. option:: --github [str] [repeatable]

    A GitHub username to source SSH keys from

    Can be provided multiple times

.. option:: --launchpad [str] [repeatable]

    A Launchpad username to source SSH keys from

    Can be provided multiple times

.. option:: --help

    Show this message and exit
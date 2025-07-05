======================
hostedpi ssh keys list
======================

.. program:: hostedpi-ssh-keys-list

List the SSH keys on a Raspberry Pi server, using the key label and note if available

.. code-block:: text

    Usage: hostedpi ssh keys list [OPTIONS] NAME

Arguments
=========

.. option:: name [str] [required]

    Name of the Raspberry Pi server to list SSH keys for

Options
=======

.. option:: --help

    Show this message and exit

Usage
=====

List keys on a Pi:

.. code-block:: console

    $ hostedpi ssh keys list mypi
    ben@fern
    dave@home
    ben@jake # ssh-import-id gh:bennuttall

.. note::

    The last example includes a comment indicating that the key was imported from GitHub using the
    :doc:`import` command. We refer to the ``ben@jake`` part as the label.

    Keys can be removed by label using the :doc:`remove` command, and imported keys can be removed
    using the :doc:`unimport` command.
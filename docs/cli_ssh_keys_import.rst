========================
hostedpi ssh keys import
========================

.. program:: hostedpi-ssh-keys-import

Import SSH keys from GitHub and/or Launchpad to one or more Raspberry Pi servers

.. code-block:: text

    Usage: hostedpi ssh keys import [OPTIONS] [NAMES]...

Arguments
=========

.. option:: names [str ...]

    Names of the Raspberry Pi server to import SSH keys to

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

Usage
=====

Import keys from GitHub onto a Pi:

.. code-block:: console

    $ hostedpi ssh-import-id mypi --gh bennuttall
    4 keys retrieved from GitHub

    4 keys added to mypi

Import keys from GitHub onto multiple Pis:

.. code-block:: console

    $ hostedpi ssh-import-id mypi mypi2 --gh bennuttall
    4 keys retrieved from GitHub

    0 keys added to mypi
    4 keys added to mypi2

.. note::

    If no names of Pis are given, the key count will be shown for all Pis in the account

.. note::

    Keys are counted before and after addition, and de-duplicated, so if a key is already found on
    the Pi, it will show as not having been added, as above.

Import keys from GitHub and Launchpad onto a Pi:

.. code-block:: console

    $ hostedpi ssh-import-id mypi --gh bennuttall --lp bennuttall
    4 keys retrieved from GitHub
    1 key retrieved from Launchpad

    1 key added to mypi

.. note::
    
    Keys are counted before and after addition, and de-duplicated, so if a key is already found on
    the Pi, it will show as not having been added, as above.

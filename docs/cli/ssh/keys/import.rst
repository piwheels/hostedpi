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

.. option:: --github, --gh [str] [repeatable]

    A GitHub username to source SSH keys from

    Can be provided multiple times

.. option:: --launchpad, --lp [str] [repeatable]

    A Launchpad username to source SSH keys from

    Can be provided multiple times

.. option:: --help

    Show this message and exit

Usage
=====

Import keys from GitHub onto a Pi:

.. code-block:: console

    $ hostedpi ssh keys import mypi --gh bennuttall
    Imported 4 keys to mypi

Import keys from GitHub onto multiple Pis:

.. code-block:: console

    $ hostedpi ssh keys import mypi mypi2 --gh bennuttall
    Imported 4 keys to mypi
    No new keys imported to mypi2

Import keys from GitHub and Launchpad onto a Pi:

.. code-block:: console

    $ hostedpi ssh keys import mypi --gh bennuttall --lp bennuttall
    Imported 4 keys to mypi

Import keys from GitHub onto multiple Pis:

.. code-block:: console

    $ hostedpi ssh keys import mypi mypi2 --gh bennuttall
    Imported 4 keys to mypi
    No new keys imported to mypi2

Import keys from GitHub and Launchpad onto multiple Pis matching a filter:

.. code-block:: console

    $ hostedpi ssh keys import --filter mypi --gh bennuttall --lp bennuttall
    Imported 4 keys to mypi
    No new keys imported to mypi2
    No new keys imported to mypi3
    Imported 2 keys to mypi4

.. note::
    
    Keys are counted before and after addition, and de-duplicated, so if a key is already found on
    the Pi, it will show as not having been added, as above.

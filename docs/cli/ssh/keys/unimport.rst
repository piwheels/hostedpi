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

Remove imported keys from GitHub onto a Pi:

.. code-block:: console

    $ hostedpi ssh keys unimport mypi --gh bennuttall
    Removed 4 keys from mypi

Remove imported keys from GitHub onto multiple Pis:

.. code-block:: console

    $ hostedpi ssh keys unimport mypi mypi2 --gh bennuttall
    Removed 4 keys from mypi
    No keys matching import sources specified found on mypi2

Remove imported keys from GitHub and Launchpad onto a Pi:

.. code-block:: console

    $ hostedpi ssh keys unimport mypi --gh bennuttall --lp bennuttall
    Removed 4 keys from mypi

Remove imported keys from GitHub onto multiple Pis:

.. code-block:: console

    $ hostedpi ssh keys unimport mypi mypi2 --gh bennuttall
    Removed 4 keys from mypi
    No keys matching import sources specified found on mypi2

Remove imported keys from GitHub and Launchpad onto multiple Pis matching a filter:

.. code-block:: console

    $ hostedpi ssh keys unimport --filter mypi --gh bennuttall --lp bennuttall
    Removed 4 keys from mypi
    No keys matching import sources specified found on mypi2
    No keys matching import sources specified found on mypi3
    Removed 4 keys from mypi4

.. note::
    
    Keys are counted before and after addition, and de-duplicated, so if a key is already found on
    the Pi, it will show as not having been added, as above.

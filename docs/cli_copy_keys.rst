==================
hostedpi copy-keys
==================

Copy all SSH keys from one Pi to one or more others

Synopsis
========

.. code-block:: text

    hostedpi copy-keys [-h] name_src [names_dest [names_dest ...]]

Description
===========

.. program:: hostedpi-copy-keys

.. option:: name_src

    The name of the Pi to copy keys from

.. option:: names_dest

    The names of the Pis to copy keys to

.. option:: --help

    Show this message and exit

Usage
=====

Copy the keys from one Pi to another:

.. code-block:: console

    $ hostedpi copy-keys mypi mypi2
    2 keys added to mypi2

Copy the keys from one Pi to several others:

.. code-block:: console

    $ hostedpi copy-keys mypi mypi2 mypi3 mypi4
    0 keys added to mypi2
    2 keys added to mypi3
    1 keys added to mypi4

.. note::
    
    Keys are counted before and after addition, and de-duplicated, so if a key is already found on
    the Pi, it will show as not having been added, as above.

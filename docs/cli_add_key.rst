================
hostedpi add-key
================

Add an SSH key from a public key file to one or more Pis

Synopsis
========

.. code-block:: text

    hostedpi add-key [-h] ssh_key_path [names [names ...]]

Description
===========

.. program:: hostedpi-add-key

.. option:: ssh_key_path

    The path to an SSH public key file to add to the Pi

.. option:: names [names ...]

    The name of the Pis to add keys to

.. option:: -h, --help

    Show this help message and exit

Usage
=====

Add your SSH key to one Pi:

.. code-block:: console

    $ hostedpi add-key ~/.ssh/id_rsa.pub mypi
    1 key added to mypi

Add your SSH key to multiple Pis:

.. code-block:: console

    $ hostedpi add-key ~/.ssh/id_rsa.pub mypi mypi2 pypi3
    0 keys added to mypi
    1 key added to mypi2
    1 key added to mypi3

.. note::
    
    Keys are counted before and after addition, and de-duplicated, so if the key
    is already found on the Pi, it will show as not having been added, as above.

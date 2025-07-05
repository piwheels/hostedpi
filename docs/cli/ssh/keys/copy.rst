======================
hostedpi ssh keys copy
======================

.. program:: hostedpi-ssh-keys-copy

Copy the SSH keys from one Raspberry Pi server to others

.. code-block:: text

    Usage: hostedpi ssh keys copy [OPTIONS] SRC DESTS...

Arguments
=========

.. option:: src [str] [required]

    Name of the Raspberry Pi server to copy SSH keys from

.. option:: dests [str ...] [required]

    Names of the Raspberry Pi servers to copy SSH keys to

Options
=======

.. option:: --help

    Show this message and exit

Usage
=====

Copy the keys from one Pi to another:

.. code-block:: console

    $ hostedpi copy-keys mypi mypi2
    Copied 2 keys from mypi to mypi2

Copy the keys from one Pi to several others:

.. code-block:: console

    $ hostedpi copy-keys mypi mypi2 mypi3 mypi4
    Copied 2 keys from mypi to mypi2
    No new keys copied to mypi from mypi3
    Copied 1 key from mypi to mypi4

.. note::
    
    Keys are counted before and after addition, and de-duplicated, so if a key is already found on
    the Pi, it will show as not having been added, as above.

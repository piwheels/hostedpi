=====================
hostedpi ssh keys add
=====================

.. program:: hostedpi-ssh-keys-add

Add an SSH key to one or more Raspberry Pi servers

.. code-block:: text

    Usage: hostedpi ssh keys add [OPTIONS] SSH_KEY_PATH [NAMES]...

Arguments
=========

.. option:: ssh_key_path [path] [required]

    Path to the SSH key to install on the Raspberry Pi servers

.. option:: names [str ...]

    Name of the Raspberry Pi server to add SSH keys to

Options
=======

.. option:: --filter [str]

    Search pattern for filtering server names

.. option:: --help

    Show this message and exit

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
    
    Keys are counted before and after addition, and de-duplicated, so if the key is already found on
    the Pi, it will show as not having been added, as above.

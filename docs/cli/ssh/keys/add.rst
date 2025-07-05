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

Add your SSH key to a Pi:

.. code-block:: console

    $ hostedpi ssh keys add ~/.ssh/id_rsa.pub mypi
    Added key /home/ben/.ssh/id_rsa.pub to mypi

Add your SSH key to multiple Pis:

.. code-block:: console

    $ hostedpi ssh keys add ~/.ssh/id_rsa.pub mypi mypi2 mypi3
    Added key /home/ben/.ssh/id_rsa.pub to mypi
    Key /home/ben/.ssh/id_rsa.pub already exists on mypi2
    Added key /home/ben/.ssh/id_rsa.pub to mypi3

Add your SSH key to all Pis matching a filter:

.. code-block:: console

    $ hostedpi ssh keys add ~/.ssh/id_rsa.pub --filter mypi
    Added key /home/ben/.ssh/id_rsa.pub to mypi
    Key /home/ben/.ssh/id_rsa.pub already exists on mypi2
    Added key /home/ben/.ssh/id_rsa.pub to mypi3
    Added key /home/ben/.ssh/id_rsa.pub to mypi4

Add your SSH key to all Pis:

.. code-block:: console

    $ hostedpi ssh keys add ~/.ssh/id_rsa.pub
    Added key /home/ben/.ssh/id_rsa.pub to mypi
    Key /home/ben/.ssh/id_rsa.pub already exists on mypi2
    Added key /home/ben/.ssh/id_rsa.pub to mypi3
    Added key /home/ben/.ssh/id_rsa.pub to mypi4
    Added key /home/ben/.ssh/id_rsa.pub to anotherpi

.. warning:: 

    Be sure to add your public key, not your private key. The public key is usually found in
    ``~/.ssh/id_rsa.pub`` or similar, while the private key is in ``~/.ssh/id_rsa`` or similar.
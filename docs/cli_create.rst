===============
hostedpi create
===============

Provision a new Pi in the account

Synopsis
========

.. code-block:: text

    hostedpi create [-h] [--model [model]] [--disk [disk]] [--image [image]]
                    [--ssh-key-path [ssh_key_path]]
                    name

Description
===========

.. program:: hostedpi-create

.. option:: name

    The name of the new Pi to provision

.. option:: -h, --help

    Show this help message and exit

.. option:: --model [model]

    The model of the new Pi to provision (3 or 4)

.. option:: --disk [disk]

    The disk size in GB

.. option:: --image [image]

    The operating system image to use

.. option:: --ssh-key-path [ssh key path]

    The path to an SSH public key file to add to the Pi

Usage
=====

Provision a new Pi using the default settings:

.. code-block:: console

    $ hostedpi create mypi
    Pi mypi provisioned successfully

    Name: mypi
    Provision status: provisioning
    Model: Raspberry Pi 3
    Disk size: 10GB
    IPv6 address: 2a00:1098:8:5b::1
    IPv6 network: 2a00:1098:8:5b00::/56
    SSH port: 5091
    Location: MER
    URLs:
      http://www.mypi.hostedpi.com
      https://www.mypi.hostedpi.com
    SSH commands:
      ssh -p 5091 root@ssh.mypi.hostedpi.com  # IPv4
      ssh root@[2a00:1098:8:5b::1]  # IPv6

Provision a new Pi using custom settings:

.. code-block:: console

    $ hostedpi create mypi4 --model 4 --disk 60 --image ubuntu20.04.arm64 --ssh-key-path ~/.ssh/id_rsa.pub
    Pi mypi4 provisioned successfully

    Name: mypi4
    Provision status: provisioning
    Model: Raspberry Pi 4
    Disk size: 60GB
    IPv6 address: 2a00:1098:8:5b::1
    IPv6 network: 2a00:1098:8:5b00::/56
    SSH port: 5091
    Location: MER
    URLs:
      http://www.mypi4.hostedpi.com
      https://www.mypi4.hostedpi.com
    SSH commands:
      ssh -p 5091 root@ssh.mypi4.hostedpi.com  # IPv4
      ssh root@[2a00:1098:8:5b::1]  # IPv6

.. note::
    Use the :doc:`cli_images` command to retrieve the available operating system
    images for each Pi model.

.. note::
    More information about the Pi will be available with the command
    :doc:`cli_show` once it's finished provisioning.

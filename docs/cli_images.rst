===============
hostedpi images
===============

Retrieve the list of operating system images available for the given Pi model

Synopsis
========

.. code-block:: text

    hostedpi images [-h] [model]

Description
===========

.. program:: hostedpi-images

.. option:: model

    The Pi model number (3 or 4) to get operating systems for

.. option:: -h, --help

    Show this help message and exit

Usage
=====

List the available operating system images for Pi 3 and Pi 4:

.. code-block:: console

    Images for Pi 3:
    Ubuntu 18.04 (Bionic) : ubuntu-18.04
    Ubuntu 16.04 (Xenial) : ubuntu-16.04
    Raspbian Buster       : raspbian-buster
    Raspbian Jessie       : raspbian-jessie
    Raspbian Stretch      : stretch

    Images for Pi 4:
    Ubuntu 20.04 64 bit (experimental) : ubuntu20.04.arm64
    Raspbian Buster                    : raspbian-buster4
    Raspberry Pi OS 64 bit             : pios64b

List the available operating system images for Pi 3:

.. code-block:: console

    $ hostedpi images 3
    Ubuntu 16.04 (Xenial) : ubuntu-16.04
    Ubuntu 18.04 (Bionic) : ubuntu-18.04
    Raspbian Jessie       : raspbian-jessie
    Raspbian Stretch      : stretch
    Raspbian Buster       : raspbian-buster

List the available operating system images for Pi 4:

.. code-block:: console

    $ hostedpi images 4
    Ubuntu 20.04 64 bit (experimental) : ubuntu20.04.arm64
    Raspbian Buster                    : raspbian-buster4
    Raspberry Pi OS 64 bit             : pios64b
    Ubuntu 18.04 (Bionic)              : ubuntu-18.04-rpi4

.. note::
    The right hand column represents the image label which can be used when
    provisioning a new Pi with :doc:`cli_create` and
    :meth:`~hostedpi.picloud.PiCloud.create_pi`.

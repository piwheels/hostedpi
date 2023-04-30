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

    $ hostedpi images
    Images for Pi 3:
    Ubuntu 20.04 (Focal Fossa) (32 bit)                  : rpi-focal-armhf
    Ubuntu 18.04 (Bionic Beaver) (64 bit)                : rpi-bionic-arm64
    Ubuntu 20.04 (Focal Fossa) (64 bit)                  : rpi-focal-arm64
    Ubuntu 22.04 (Jammy Jellyfish) (64 bit)              : rpi-jammy-arm64
    Raspberry Pi OS Bullseye (32 bit)                    : rpi-bullseye-armhf
    Raspberry Pi OS Buster (32 bit)                      : rpi-buster-armhf
    Raspberry Pi OS Buster (64 bit)                      : rpi-buster-arm64
    Raspberry Pi OS Bullseye (64 bit)                    : rpi-bullseye-arm64
    Raspberry Pi OS Bullseye Desktop (64 bit, 1920x1080) : rpi-bullseye-arm64-vnc.2022-03-25T17:23:56+00:00

    Images for Pi 4:
    Ubuntu 20.04 (Focal Fossa) (32 bit)                  : rpi-focal-armhf
    Raspberry Pi OS Bullseye Desktop (64 bit, 1920x1080) : rpi-bullseye-arm64-vnc.2022-03-25T17:23:56+00:00
    Raspberry Pi OS Bullseye (32 bit)                    : rpi-bullseye-armhf
    Raspberry Pi OS Buster (32 bit)                      : rpi-buster-armhf
    Ubuntu 20.04 (Focal Fossa) (64 bit)                  : rpi-focal-arm64
    Ubuntu 18.04 (Bionic Beaver) (64 bit)                : rpi-bionic-arm64
    Raspberry Pi OS Bullseye (64 bit)                    : rpi-bullseye-arm64
    Raspberry Pi OS Buster (64 bit)                      : rpi-buster-arm64
    Ubuntu 22.04 (Jammy Jellyfish) (64 bit)              : rpi-jammy-arm64

List the available operating system images for Pi 3:

.. code-block:: console

    $ hostedpi images 3
    Images for Pi 3:
    Ubuntu 20.04 (Focal Fossa) (32 bit)                  : rpi-focal-armhf
    Ubuntu 18.04 (Bionic Beaver) (64 bit)                : rpi-bionic-arm64
    Ubuntu 20.04 (Focal Fossa) (64 bit)                  : rpi-focal-arm64
    Ubuntu 22.04 (Jammy Jellyfish) (64 bit)              : rpi-jammy-arm64
    Raspberry Pi OS Bullseye (32 bit)                    : rpi-bullseye-armhf
    Raspberry Pi OS Buster (32 bit)                      : rpi-buster-armhf
    Raspberry Pi OS Buster (64 bit)                      : rpi-buster-arm64
    Raspberry Pi OS Bullseye (64 bit)                    : rpi-bullseye-arm64
    Raspberry Pi OS Bullseye Desktop (64 bit, 1920x1080) : rpi-bullseye-arm64-vnc.2022-03-25T17:23:56+00:00

List the available operating system images for Pi 4:

.. code-block:: console

    $ hostedpi images 4
    Images for Pi 4:
    Ubuntu 20.04 (Focal Fossa) (32 bit)                  : rpi-focal-armhf
    Raspberry Pi OS Bullseye Desktop (64 bit, 1920x1080) : rpi-bullseye-arm64-vnc.2022-03-25T17:23:56+00:00
    Raspberry Pi OS Bullseye (32 bit)                    : rpi-bullseye-armhf
    Raspberry Pi OS Buster (32 bit)                      : rpi-buster-armhf
    Ubuntu 20.04 (Focal Fossa) (64 bit)                  : rpi-focal-arm64
    Ubuntu 18.04 (Bionic Beaver) (64 bit)                : rpi-bionic-arm64
    Raspberry Pi OS Bullseye (64 bit)                    : rpi-bullseye-arm64
    Raspberry Pi OS Buster (64 bit)                      : rpi-buster-arm64
    Ubuntu 22.04 (Jammy Jellyfish) (64 bit)              : rpi-jammy-arm64

.. note::
    The right hand column represents the image label which can be used when provisioning a new Pi
    with :doc:`cli_create` and :meth:`~hostedpi.picloud.PiCloud.create_pi`.

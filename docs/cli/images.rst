===============
hostedpi images
===============

.. program:: hostedpi-images

List operating system images available for Raspberry Pi servers

.. code-block:: text

    Usage: hostedpi images [OPTIONS] MODEL

Arguments
=========

.. option:: model [int] [required]

    Raspberry Pi model number to list images for (3 or 4)

Options
=======

.. option:: --filter [str]

    Search pattern for filtering image names

.. option:: --help

    Show this message and exit

Usage
=====

List the available operating system images for Pi 3 and Pi 4:

.. code-block:: console

    $ hostedpi images 3
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃ ID                                         ┃ Name                                        ┃
    ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
    │ rpi-bionic-arm64                           │ Ubuntu 18.04 (Bionic Beaver) (64 bit)       │
    │ rpi-bookworm-arm64                         │ Raspberry Pi OS Bookworm (12) (64 bit)      │
    │ rpi-bookworm-armhf                         │ Raspberry Pi OS Bookworm (12) (32 bit)      │
    │ rpi-bullseye-arm64                         │ Raspberry Pi OS Bullseye (64 bit)           │
    │ rpi-bullseye-arm64-vnc.2022-03-25T17:23:5… │ Raspberry Pi OS Bullseye Desktop (64 bit,   │
    │                                            │ 1920x1080)                                  │
    │ rpi-bullseye-armhf                         │ Raspberry Pi OS Bullseye (32 bit)           │
    │ rpi-buster-arm64                           │ Raspberry Pi OS Buster (64 bit)             │
    │ rpi-buster-armhf                           │ Raspberry Pi OS Buster (32 bit)             │
    │ rpi-focal-arm64                            │ Ubuntu 20.04 (Focal Fossa) (64 bit)         │
    │ rpi-focal-armhf                            │ Ubuntu 20.04 (Focal Fossa) (32 bit)         │
    │ rpi-jammy-arm64                            │ Ubuntu 22.04 (Jammy Jellyfish) (64 bit)     │
    └────────────────────────────────────────────┴─────────────────────────────────────────────┘
    $ hostedpi images 4
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃ ID                                         ┃ Name                                        ┃
    ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
    │ rpi-bionic-arm64                           │ Ubuntu 18.04 (Bionic Beaver) (64 bit)       │
    │ rpi-bookworm-arm64                         │ Raspberry Pi OS Bookworm (12) (64 bit)      │
    │ rpi-bookworm-armhf                         │ Raspberry Pi OS Bookworm (12) (32 bit)      │
    │ rpi-bullseye-arm64                         │ Raspberry Pi OS Bullseye (64 bit)           │
    │ rpi-bullseye-arm64-vnc.2022-03-25T17:23:5… │ Raspberry Pi OS Bullseye Desktop (64 bit,   │
    │                                            │ 1920x1080)                                  │
    │ rpi-bullseye-armhf                         │ Raspberry Pi OS Bullseye (32 bit)           │
    │ rpi-buster-arm64                           │ Raspberry Pi OS Buster (64 bit)             │
    │ rpi-buster-armhf                           │ Raspberry Pi OS Buster (32 bit)             │
    │ rpi-focal-arm64                            │ Ubuntu 20.04 (Focal Fossa) (64 bit)         │
    │ rpi-focal-armhf                            │ Ubuntu 20.04 (Focal Fossa) (32 bit)         │
    │ rpi-jammy-arm64                            │ Ubuntu 22.04 (Jammy Jellyfish) (64 bit)     │
    └────────────────────────────────────────────┴─────────────────────────────────────────────┘

.. note::
    
    The left hand column represents the image label which can be used when provisioning a new Pi
    with :doc:`create` and :meth:`~hostedpi.picloud.PiCloud.create_pi`.

========
hostedpi
========

.. image:: https://badge.fury.io/py/hostedpi.svg
    :target: https://badge.fury.io/py/hostedpi
    :alt: Latest Version

Python interface to the `Mythic Beasts Hosted Pi`_ API, developed by the `piwheels`_ team
(`Ben Nuttall`_ and `Dave Jones`_).

.. _Mythic Beasts Hosted Pi: https://www.mythic-beasts.com/order/rpi
.. _piwheels: https://www.piwheels.org/
.. _Ben Nuttall: https://github.com/bennuttall
.. _Dave Jones: https://github.com/waveform80

This module provides a Pythonic interface to the API, as well as a command line interface.

The authors of this library are not affiliated with Mythic Beasts, but we use their Pi cloud to
power the piwheels project.

Documentation of the API itself can be found at
https://www.mythic-beasts.com/support/api/raspberry-pi

.. note::
    Note that the library is currently in beta. The API and CLI are not yet stable and may change.
    Once the library reaches v1.0, it will be considered stable.

Usage
=====

View the information about Pis in your account from the command line:

.. code-block:: console

    $ hostedpi list          
    c8046p3gu
    c8046p55a
    c8046p6vv
    c8046p6wt
    $ hostedpi table
    ┏━━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━┓
    ┃ Name            ┃ Model ┃ Memory ┃ CPU Speed ┃
    ┡━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━┩
    │ c8046p3gu       │ 3     │ 1 GB   │ 1.2 GHz   │
    │ c8046p55a       │ 3     │ 1 GB   │ 1.2 GHz   │
    │ c8046p6vv       │ 3     │ 1 GB   │ 1.2 GHz   │
    │ c8046p6wt       │ 3     │ 1 GB   │ 1.2 GHz   │
    │ c8046p6ha       │ 4     │ 8 GB   │ 2.0 GHz   │
    │ c8046p6lj       │ 4     │ 4 GB   │ 1.5 GHz   │
    └─────────────────┴───────┴────────┴───────────┘
    $ hostedpi table c8046p6ha
    ┏━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━┓
    ┃ Name      ┃ Model ┃ Memory ┃ CPU Speed ┃
    ┡━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━┩
    │ c8046p6ha │ 3     │ 1 GB   │ 1.2 GHz   │
    └───────────┴───────┴────────┴───────────┘

    $ hostedpi table c8046p6ha --full
    ┏━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
    ┃ Name      ┃ Model ┃ Memory ┃ CPU Speed ┃ NIC Speed ┃ Disk size ┃ Status     ┃ Initialised keys ┃ IPv4 SSH port ┃
    ┡━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
    │ c8046p6ha │ 4B    │ 8 GB   │ 2.0 GHz   │ 1 Gbps    │ 50 GB     │ Powered on │ Yes              │ 5387          │
    └───────────┴───────┴────────┴───────────┴───────────┴───────────┴────────────┴──────────────────┴───────────────┘


Provision a new Pi and view its SSH command:

.. code-block:: console

    $ hostedpi create mypi --spec pi4-server
    Creating Pi mypi with spec pi4-server...
    Pi mypi created successfully.
    SSH command: ssh -p 5123

.. code-block:: pycon

    >>> from hostedpi import PiCloud, Pi4ServerSpec
    >>> cloud = PiCloud()
    >>> pi = cloud.create_pi('mypi', spec=Pi4ServerSpec)
    >>> print(pi.ssh_command)
    ssh -p 5123 root@ssh.mypi.hostedpi.com

See the :doc:`getting_started` page for information on how to authenticate, and
see the :doc:`cli` page for information on using the command line interface.

Table of Contents
=================

.. toctree::
    :maxdepth: 1

    getting_started
    cli
    recipes
    api
    development

Contributing
============

* Source code can be found on GitHub at https://github.com/piwheels/hostedpi
* Code and documentation contributions welcome
* The issue tracker can be found at https://github.com/piwheels/hostedpi/issues
* For issues with the API or the service itself, please contact Mythic Beasts support
  https://www.mythic-beasts.com/support

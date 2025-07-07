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
    pi123
    pi234
    pi345
    pi456
    $ hostedpi table
    ┏━━━━━━━┳━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━┓
    ┃ Name  ┃ Model ┃ Memory ┃ CPU Speed ┃
    ┡━━━━━━━╇━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━┩
    │ pi123 │ 3     │ 1 GB   │ 1.2 GHz   │
    │ pi234 │ 3     │ 1 GB   │ 1.2 GHz   │
    │ pi345 │ 4     │ 8 GB   │ 2.0 GHz   │
    │ pi456 │ 4     │ 4 GB   │ 1.5 GHz   │
    └───────┴───────┴────────┴───────────┘
    $ hostedpi table pi123
    ┏━━━━━━━┳━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━┓
    ┃ Name  ┃ Model ┃ Memory ┃ CPU Speed ┃
    ┡━━━━━━━╇━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━┩
    │ pi123 │ 3     │ 1 GB   │ 1.2 GHz   │
    └───────┴───────┴────────┴───────────┘

    $ hostedpi table pi345 --full
    ┏━━━━━━━┳━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
    ┃ Name  ┃ Model ┃ Memory ┃ CPU Speed ┃ NIC Speed ┃ Disk size ┃ Status     ┃ Initialised keys ┃ IPv4 SSH port ┃
    ┡━━━━━━━╇━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
    │ pi345 │ 4B    │ 8 GB   │ 2.0 GHz   │ 1 Gbps    │ 50 GB     │ Powered on │ Yes              │ 5387          │
    └───────┴───────┴────────┴───────────┴───────────┴───────────┴────────────┴──────────────────┴───────────────┘

Provision a new Pi with your public key and SSH into it:

.. code-block:: console

    $ hostedpi create mypi --model 3 --ssh-key-path ~/.ssh/id_rsa.pub --wait
    Server provisioned
    ┏━━━━━━┳━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━┓
    ┃ Name ┃ Model ┃ Memory ┃ CPU Speed ┃
    ┡━━━━━━╇━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━┩
    │ mypi | 3     │ 1 GB   │ 1.2 GHz   │
    └──────┴───────┴────────┴───────────┘
    $ hostedpi ssh command mypi
    ssh -p 5063 root@ssh.mypi.hostedpi.com
    $ ssh -p 5063 root@ssh.mypi.hostedpi.com
    root@mypi:~#

Write a Python script to provision a new Pi and output its SSH command:

.. code-block:: python

    from hostedpi import PiCloud, Pi4ServerSpec

    cloud = PiCloud()
    
    pi = cloud.create_pi(name="mypi", spec=Pi4ServerSpec())
    print(pi.ipv4_ssh_command)

* See the `getting_started`_ page for information on how to get API keys and authenticate
* See the `cli/index`_ page for information on using the command line interface
* See the `api/index`_ page for the module's API reference

.. _getting_started: https://hostedpi.readthedocs.io/en/latest/getting_started.html
.. _cli/index: https://hostedpi.readthedocs.io/en/latest/cli/index.html
.. _api/index: https://hostedpi.readthedocs.io/en/latest/api/index.html

Documentation
=============

Documentation for this module can be found at https://hostedpi.readthedocs.io/

Documentation of the API itself can be found at
https://www.mythic-beasts.com/support/api/raspberry-pi

Contributing
============

* Source code can be found on GitHub at https://github.com/piwheels/hostedpi
* Code and documentation contributions welcome
* The issue tracker can be found at https://github.com/piwheels/hostedpi/issues
* For issues with the API itself, please contact Mythic Beasts support
  https://www.mythic-beasts.com/support

========
hostedpi
========

.. image:: https://badge.fury.io/py/hostedpi.svg
    :target: https://badge.fury.io/py/hostedpi
    :alt: Latest Version

Python interface to the `Mythic Beasts Hosted Pi`_ API, developed by the
`piwheels`_ team (`Ben Nuttall`_ and `Dave Jones`_).

.. _Mythic Beasts Hosted Pi: https://www.mythic-beasts.com/order/rpi
.. _piwheels: https://www.piwheels.org/
.. _Ben Nuttall: https://twitter.com/ben_nuttall
.. _Dave Jones: https://twitter.com/waveform80

This module provides a Pythonic interface to the API, as well as a command line
interface.

The authors of this library are not affiliated with Mythic Beasts, but we use
their Pi cloud to power the piwheels project.

Documentation of the API itself can be found at
https://www.mythic-beasts.com/support/api/raspberry-pi

Usage
=====

View the information about a Pi from the command line:

.. code-block:: console

    $ hostedpi show mypi
    Name: mypi
    Provision status: live
    Model: Raspberry Pi 3B
    Disk size: 10GB
    Power: on
    IPv6 address: 2a00:1098:8:5b::1
    IPv6 network: 2a00:1098:8:5b00::/56
    Initialised keys: yes
    SSH keys: 4
    IPv4 SSH port: 5091
    Location: MER
    URLs:
      http://www.mypi.hostedpi.com
      https://www.mypi.hostedpi.com
    SSH commands:
      ssh -p 5091 root@ssh.mypi.hostedpi.com  #IPv4
      ssh root@[2a00:1098:8:5b::1]  #IPv6

Provision a new Pi and view its SSH command (using Python):

.. code-block:: pycon

    >>> from hostedpi import PiCloud
    >>> api_id = '8t29hvcux5g9vud8'
    >>> secret = 'QNwsvxZY8SxT3OiLt:Vmz-D1mWQuoZ'
    >>> cloud = PiCloud(api_id, secret, ssh_key_path='/home/ben/.ssh/id_rsa.pub')
    >>> pi = cloud.create_pi('mypi')
    >>> print(pi.ssh_command)
    ssh -p 5123 root@ssh.mypi.hostedpi.com

See the `getting started`_ page for information on how to authenticate, and
see the `command line interface`_ page for information on using the command line
interface.

.. _getting started: https://hostedpi.readthedocs.io/en/latest/getting_started.html
.. _command line interface: https://hostedpi.readthedocs.io/en/latest/cli.html

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

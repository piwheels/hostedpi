========
hostedpi
========

Python interface to the `Mythic Beasts Hosted Pi`_ API, developed by the
`piwheels`_ team (`Ben Nuttall`_ and `Dave Jones`_).

.. _Mythic Beasts Hosted Pi: https://www.mythic-beasts.com/order/rpi
.. _piwheels: https://www.piwheels.org/
.. _Ben Nuttall: https://twitter.com/ben_nuttall
.. _Dave Jones: https://twitter.com/waveform80

This module provides a Pythonic interface to the API, as well as some command
line utilities.

The authors of this library are not affiliated with Mythic Beasts, but we use
their Pi cloud to power the piwheels project.

Documentation of the API itself can be found at
https://www.mythic-beasts.com/support/api/raspberry-pi

Usage
=====

Provision a new Pi and view its SSH command (using Python):

.. code-block:: pycon

    >>> from hostedpi import PiCloud
    >>> api_id = '8t29hvcux5g9vud8'
    >>> secret = 'QNwsvxZY8SxT3OiLt:Vmz-D1mWQuoZ'
    >>> cloud = PiCloud(api_id, secret, ssh_key_path='/home/ben/.ssh/id_rsa.pub')
    >>> pi = cloud.create_pi('mypi')
    >>> print(pi.ssh_command)
    ssh -p 5123 root@ssh.somepi.hostedpi.com

View the information about a Pi from the command line:

.. code-block:: console

    $ hostedpi show mypi
    Name: mypi
    Status: live
    Model: Raspberry Pi 3
    Disk size: 30 GB
    Power: No
    Initialised keys: No
    IPv6 address: 2a00:1098:0008:0088:0000:0000:0000:0001
    IPv6 address (routed): 2a00:1098:0008:8800:0000:0000:0000:0000/56
    Location: MER
    SSH keys: 1
    SSH port: 5123
    URLs:
      http://www.mypi.hostedpi.com
      https://www.mypi.hostedpi.com
    SSH command: ssh -p 5123 root@ssh.mypi.hostedpi.com

See the :doc:`getting_started` page for information on how to authenticate, and
see the :doc:`cli` page for information on using the command line interface.

Table of Contents
=================

.. toctree::
    :maxdepth: 1
    :numbered:

    getting_started
    recipes
    api
    cli
    development

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Contributing
============

* Source code can be found on GitHub at https://github.com/piwheels/hostedpi
* Code and documentation contributions welcome
* The issue tracker can be found at https://github.com/piwheels/hostedpi/issues
* For issues with the API itself, please contact Mythic Beasts support
  https://www.mythic-beasts.com/support

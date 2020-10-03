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

Provision a new Pi and view its SSH command::

    >>> from hostedpi import PiCloud
    >>> api_id = '8t29hvcux5g9vud8'
    >>> secret = 'QNwsvxZY8SxT3OiLt:Vmz-D1mWQuoZ'
    >>> cloud = PiCloud(api_id, secret, ssh_key_path='/home/ben/.ssh/id_rsa.pub')
    >>> pi = cloud.create_pi('somepi')
    >>> print(pi.ssh_command)
    ssh -p 5123 root@ssh.somepi.hostedpi.com

See the :doc:`getting_started` page for information on how to authenticate.

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

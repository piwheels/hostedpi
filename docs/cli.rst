=====================
Command line programs
=====================

hostedpi
========

The ``hostedpi`` command is a multi-purpose utility for common actions
interacting with the API.

This program requires API keys to be provided using environment variables
``HOSTEDPI_ID`` and ``HOSTEDPI_SECRET``.

hostedpi test
-------------

Test a connection to the API:

.. code-block:: console

    $ hostedpi test
    Connected to Mythic Beasts API

hostedpi list
-------------

List all the Pis in the account

.. code-block:: console

    $ hostedpi list
    mypi
    mypi2

hostedpi show
-------------

Show all information for a Pi:

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

Show all information for all Pis in the account:

.. code-block:: console

    $ hostedpi show all
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

    Name: mypi2
    Status: live
    Model: Raspberry Pi 4
    Disk size: 30 GB
    Power: No
    Initialised keys: No
    IPv6 address: 2a00:1098:0088:0088:0000:0000:0000:0001
    IPv6 address (routed): 2a00:1098:0088:8800:0000:0000:0000:0000/56
    Location: MER
    SSH keys: 1
    SSH port: 5124
    URLs:
      http://www.mypi2.hostedpi.com
      https://www.mypi2.hostedpi.com
    SSH command: ssh -p 5124 root@ssh.mypi2.hostedpi.com

hostedpi create
---------------

Provision a new Pi:

.. code-block:: console

    $ hostedpi create mypi3
    Name: mypi3
    Status: provisioning
    Model: Raspberry Pi 3
    Disk size: 10 GB
    Power: No
    IPv6 address: 2a00:1098:0008:0088:0000:0000:0000:0001
    IPv6 address (routed): 2a00:1098:0008:8800:0000:0000:0000:0000/56
    Location: MER
    SSH port: 5136
    URLs:
      http://www.piwheels.hostedpi.com
      https://www.piwheels.hostedpi.com
    SSH command: ssh -p 5136 root@ssh.piwheels.hostedpi.com

Positional arguments:

1. NAME
2. MODEL (optional)
3. SSH_KEY_PATH (optional)

.. code-block:: console

    $ hostedpi create mypi 3 .ssh/id_rsa.pub

hostedpi reboot
---------------

Reboot a Pi:

.. code-block:: console

    $ hostedpi reboot mypi

Reboot all the Pis in the account:

.. code-block:: console

    $ hostedpi reboot all

hostedpi keys
-------------

???

hostedpi cancel
---------------

Cancel a Pi service:

.. code-block:: console

    $ hostedpi cancel mypi
    Pi service mypi cancelled

Cancel all the Pi services in the account:

.. code-block:: console

    $ hostedpi cancel all
    Pi service mypi cancelled
    Pi service mypi2 cancelled

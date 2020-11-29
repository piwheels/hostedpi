=============
hostedpi show
=============

.. program:: hostedpi-show

Show the information about one or more Pis in the account

.. code-block:: text

    positional arguments:
      names       The names of the Pis to show information for

    optional arguments:
      -h, --help  show this help message and exit

Usage
=====

Show the information about a Pi:

.. code-block:: console

    $ hostedpi show mypi
    Name: mypi
    Provision status: live
    Model: Raspberry Pi 3B
    Disk size: 10GB
    Power: off
    IPv6 address: 2a00:1098:8:5b::1
    IPv6 network: 2a00:1098:8:5b00::/56
    Initialised keys: yes
    SSH keys: 0
    IPv4 SSH port: 5091
    Location: MER
    URLs:
      http://www.mypi.hostedpi.com
      https://www.mypi.hostedpi.com
    SSH commands:
      IPv4: ssh -p 5091 root@ssh.mypi.hostedpi.com
      IPv6: ssh root@[2a00:1098:8:5b::1]

Show the number of keys on multiple Pis:

.. code-block:: console

    $ hostedpi show mypi mypi2
    Name: mypi
    Provision status: live
    Model: Raspberry Pi 3B
    Disk size: 10GB
    Power: on
    IPv6 address: 2a00:1098:8:5b::1
    IPv6 network: 2a00:1098:8:5b00::/56
    Initialised keys: yes
    SSH keys: 0
    IPv4 SSH port: 5091
    Location: MER
    URLs:
      http://www.mypi.hostedpi.com
      https://www.mypi.hostedpi.com
    SSH commands:
      IPv4: ssh -p 5091 root@ssh.mypi.hostedpi.com
      IPv6: ssh root@[2a00:1098:8:5b::1]

    Name: mypi2
    Provision status: live
    Model: Raspberry Pi 4B
    Disk size: 40GB
    Power: on
    IPv6 address: 2a00:1098:8:68::1
    IPv6 network: 2a00:1098:8:6800::/56
    Initialised keys: yes
    SSH keys: 0
    IPv4 SSH port: 5072
    Location: MER
    URLs:
      http://www.mypi2.hostedpi.com
      https://www.mypi2.hostedpi.com
    SSH commands:
      IPv4: ssh -p 5072 root@ssh.mypi2.hostedpi.com
      IPv6: ssh root@[2a00:1098:8:68::1]

.. note::
    If no names of Pis are given, information about all Pis will be shown.

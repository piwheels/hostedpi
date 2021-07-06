===============
Getting started
===============

This page contains a simple tutorial to help you get started by creating a
Mythic Beasts account, create an API key, use the command line interface and the
Python module.

Create a Mythic Beasts account
==============================

Sign up: https://www.mythic-beasts.com/user/login

Create an API key
=================

1. Log in to your Mythic Beasts account: https://www.mythic-beasts.com/user/login

2. Open the API Keys page: https://www.mythic-beasts.com/customer/api-users

3. Enter a descriptive name for your API key, for your own reference

4. Check the *Raspberry Pi Provisioning* box

5. Click the *Create API key* button

6. Make a note of the API ID and Secret. You'll need them to use this Python
   module, and you can't retrieve them after this screen is gone.

.. note::
    If you lose your keys, you can simply reset them or create a new API key.

Install the hostedpi module
===========================

For a system-wide installation:

.. code-block:: console

    $ sudo pip3 install hostedpi

for a user-level installation:

.. code-block:: console

    $ pip3 install hostedpi --user

or in a virtual environment:

.. code-block:: console

    $ pip install hostedpi

Test your API keys
==================

To test your API connection, try running the following commands in a terminal
window, with your API ID and secret:

.. code-block:: console

    $ HOSTEDPI_ID='YOUR ID' HOSTEDPI_SECRET='YOUR SECRET' hostedpi test
    Connected to the Mythic Beasts API

This message means your API credentials were found and a successful connection
was made.

Start using the Python module
=============================

The following Python program will connect to the Mythic Beasts API using your
credentials, and print out a list of Pi services in your account::

    from hostedpi import PiCloud

    cloud = PiCloud(api_id='YOUR API ID', secret='YOUR SECRET')

    for name in cloud.pis:
        print(name)

.. note::
    You can either construct :class:`~hostedpi.picloud.PiCloud` with your API
    ID and secret, or set them in environment variables like above.

You can provision a new Pi with the :meth:`~hostedpi.picloud.PiCloud.create_pi`
method::

    from hostedpi import PiCloud

    cloud = PiCloud(api_id='YOUR API ID', secret='YOUR SECRET')

    pi = cloud.create_pi('mypi3')

The default values are for a Pi 3 with a 10GB disk, but you can request either
a Pi 3 or Pi 4 and specify the disk size (which must be a multiple of 10)::

    from hostedpi import PiCloud

    cloud = PiCloud(api_id='YOUR API ID', secret='YOUR SECRET')

    pi = cloud.create_pi('mypi4', model=4, disk_size=20)

.. note::
    When requesting a Pi 3, you will either get a model 3B or 3B+. It is not
    possible to request a particular model beyond 3 or 4. The Pi 4 is the 4GB
    RAM model.

The return value of this method is a :class:`~hostedpi.pi.Pi` object which you
can use to retrieve information about the service, and to manage it. The repr of
a :class:`~hostedpi.pi.Pi` object includes the name and model:

.. code-block:: pycon

    >>> pi
    <Pi model 4 mypi4>

For example, you can retrieve the SSH command needed to connect to it::

    print(pi.ssh_command)

which should print something like::

    ssh -p 5123 root@ssh.mypi4.hostedpi.com

Other properties you can read are include:

* :attr:`~hostedpi.pi.Pi.boot_progress`
* :attr:`~hostedpi.pi.Pi.disk_size`
* :attr:`~hostedpi.pi.Pi.ipv4_ssh_command`
* :attr:`~hostedpi.pi.Pi.ipv4_ssh_config`
* :attr:`~hostedpi.pi.Pi.ipv4_ssh_port`
* :attr:`~hostedpi.pi.Pi.ssh_keys`
* :attr:`~hostedpi.pi.Pi.url`

There are also methods such as :meth:`~hostedpi.pi.Pi.reboot`::

    pi.reboot()

Other methods include:

* :meth:`~hostedpi.pi.Pi.cancel`
* :meth:`~hostedpi.pi.Pi.ssh_import_id`

More
====

* See the :doc:`cli` page for details of the possibilities provided by
  ready-made scripts
* See the API documentation for :class:`~hostedpi.pi.Pi` for more information
  on available properties and methods.
* See the :doc:`recipes` page for more ideas showing what you can do with this
  module.

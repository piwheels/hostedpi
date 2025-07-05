==================
Python library API
==================

This page describes the methods and properties available in the :class:`~hostedpi.picloud.PiCloud`
and :class:`~hostedpi.pi.Pi` classes and are intended as a useful reference to the functionality
provided.

The way to use the module is to import the :class:`~hostedpi.picloud.PiCloud` class, which will
use environment variables to authenticate with the API. This will allow you to provision new Pi
servers with the :meth:`~hostedpi.picloud.PiCloud.create_pi` method or access existing servers
from the :attr:`~hostedpi.picloud.PiCloud.pis` property.

Once you have a connected :class:`~hostedpi.picloud.PiCloud` instance and access to newly or
previously created :class:`~hostedpi.pi.Pi` instances, the following API documentation should prove
useful to show what you can do with the API via the *hostedpi* module.

Usage
=====

Define the specifications for a Raspberry Pi server and SSH key sources, then call
:meth:`~hostedpi.picloud.PiCloud.create_pi` to provision a new Pi server with this spec, and the SSH
keys installed on it:

.. code-block:: python

    from hostedpi import PiCloud, Pi4ServerSpec, SSHKeySources

    # Create a Raspberry Pi 4 server specification
    pi4_spec = Pi4ServerSpec(
        memory_gb=8,
        cpu_speed=2000,
        disk=30,
        os_image="rpi-bookworm-arm64",
    )

    # Collect SSH keys from various sources
    ssh_sources = SSHKeySources(
        ssh_key_path="/home/ben/.ssh/id_rsa.pub",
        github_usernames={"bennuttall", "waveform80"},
        launchpad_usernames={"bennuttall", "waveform80"},
    )

    cloud = PiCloud()
    pi = cloud.create_pi(name="mypi", spec=pi4_spec, ssh_keys=ssh_sources)



Contents
========

.. toctree::
   :maxdepth: 1

   picloud
   pi
   models
   exc
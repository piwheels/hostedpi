================
Python API usage
================

Provision a new Pi
==================

Provision a new Pi 4 with a specific configuration and print some info about it:

.. code-block:: python

    from hostedpi import PiCloud, Pi4ServerSpec

    cloud = PiCloud()

    pi4_spec = Pi4ServerSpec(
        memory_gb=8,
        cpu_speed=2000,
        disk=30,
        os_image="rpi-bookworm-arm64",
    )

    pi = cloud.create_pi(name="mypi", spec=pi4_spec, wait=True)
    print(f"Name: {pi.name}")
    print(f"Model: {pi.model_full}")
    print(f"Memory: {pi.memory_gb}GB")
    print(f"CPU Speed: {pi.cpu_speed}MHz")
    print(f"NIC Speed: {pi.nic_speed}Mbps")
    print(f"Disk size: {pi.disk_size}GB")
    print(f"Status: {pi.status}")
    print(f"SSH keys: {len(pi.ssh_keys)}")
    print(f"SSH command: {pi.ipv4_ssh_command}")

Provision a new Pi with SSH keys
================================

Define the specifications for a Raspberry Pi server and SSH key sources, then call
:meth:`~hostedpi.picloud.PiCloud.create_pi` to provision a new Pi with this spec, and the SSH keys
installed on it:

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

Pi model specifications
=======================

Define a specific Pi 4 configuration:

.. code-block:: python

    from hostedpi import Pi4ServerSpec

    pi4_spec = Pi4ServerSpec(
        memory_gb=8,
        cpu_speed=2000,
        disk=30,
        os_image="rpi-bookworm-arm64",
    )

A Pi 3 is less configurable, so we don't need to define memory or CPU speed as the default values
are sufficient:

.. code-block:: python

    from hostedpi import Pi3ServerSpec

    pi3_spec = Pi3ServerSpec(
        disk=20,
        os_image="rpi-bookworm-armhf",
    )

Pi info access
==============

Retrieve a Pi from the account and print some info about it:

.. code-block:: python

    from hostedpi import PiCloud

    cloud = PiCloud()

    pi = cloud.pis.get("mypi")
    print(f"Name: {pi.name}")
    print(f"Model: {pi.model_full}")
    print(f"Memory: {pi.memory_gb}GB")
    print(f"CPU Speed: {pi.cpu_speed}MHz")
    print(f"NIC Speed: {pi.nic_speed}Mbps")
    print(f"Disk size: {pi.disk_size}GB")
    print(f"Status: {pi.status}")
    print(f"SSH keys: {len(pi.ssh_keys)}")
    print(f"SSH command: {pi.ipv4_ssh_command}")

SSH key sources
===============

Define a single SSH key source, for example, a public SSH key file:

.. code-block:: python

    from hostedpi import SSHKeySources

    ssh_keys = SSHKeySources(ssh_key_path="/home/ben/.ssh/id_rsa.pub")

Or a single GitHub username:

.. code-block:: python

    from hostedpi import SSHKeySources

    ssh_keys = SSHKeySources(github_usernames={"bennuttall"})

Or multiple GitHub and Launchpad usernames:

.. code-block:: python

    from hostedpi import SSHKeySources

    ssh_keys = SSHKeySources(
        github_usernames={"bennuttall", "waveform80"},
        launchpad_usernames={"bennuttall", "waveform80"},
    )

Any combination of SSH key sources can be used:

.. code-block:: python

    from hostedpi import SSHKeySources

    ssh_keys = SSHKeySources(
        ssh_keys={"ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC..."},
        ssh_key_path="/path/to/mykey.pub",
        github_usernames={"bennuttall", "waveform80"},
        launchpad_usernames={"bennuttall", "waveform80"},
    )

SSH key management
==================

SSH keys can be added to a Pi when it is provisioned by passing some SSH key sources to
:meth:`~hostedpi.picloud.PiCloud.create_pi`:

.. code-block:: python

    from hostedpi import PiCloud, Pi4ServerSpec

    cloud = PiCloud()

    pi4_spec = Pi4ServerSpec()

    ssh_keys = SSHKeySources(
        github_usernames={"bennuttall"},
        launchpad_usernames={"bennuttall"},
    )

    pi = cloud.create_pi(name="mypi", spec=pi4_spec, ssh_key_sources=ssh_keys, wait=True)

Alternatively, SSH key sources can be given when the :class:`~hostedpi.picloud.PiCloud` is
constructed, and these will be used for all Pi instances created by that cloud, unless otherwise
specified:

.. code-block:: python

    from hostedpi import PiCloud, Pi4ServerSpec, SSHKeySources

    ssh_keys = SSHKeySources(
        github_usernames={"bennuttall"},
        launchpad_usernames={"bennuttall"},
    )

    cloud = PiCloud(ssh_key_sources=ssh_keys)

    pi4_spec = Pi4ServerSpec()

    pi = cloud.create_pi(name="mypi", spec=pi4_spec, wait=True)

SSH keys can be added to an existing Pi by calling :meth:`~hostedpi.pi.Pi.add_ssh_keys`:

.. code-block:: python

    from hostedpi import PiCloud, SSHKeySources

    cloud = PiCloud()

    pi = cloud.pis.get("mypi")

    ssh_keys = SSHKeySources(
        github_usernames={"bennuttall"},
        launchpad_usernames={"bennuttall"},
    )

    pi.add_ssh_keys(ssh_keys)

Alternatively, you can set the :attr:`~hostedpi.models.pis.Pi.ssh_keys` attribute directly:

.. code-block:: python

    from hostedpi import PiCloud

    cloud = PiCloud()
    pi = cloud.pis.get("mypi")

    ssh_keys = fetch_keys_from_somewhere()
    pi.ssh_keys = ssh_keys

.. warning::

    Setting :attr:`~hostedpi.models.pis.Pi.ssh_keys` will overwrite any existing SSH keys on the Pi.
    If you want to add keys without removing existing ones, use ``|=`` instead of ``=`` or use
    :meth:`~hostedpi.pi.Pi.add_ssh_keys`.
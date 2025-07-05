=======
PiCloud
=======

.. autoclass:: hostedpi.picloud.PiCloud
    :members:

Usage
=====

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
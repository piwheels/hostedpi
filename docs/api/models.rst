======
Models
======

The **hostedpi** module uses `Pydantic`_ models to validate and serialize data structures. The
models provided give a simple way to specify the requirements for a Raspberry Pi server, including
the specifications of the Raspberry Pi, and sources the SSH keys to be added to the server.

.. _Pydantic: https://docs.pydantic.dev/latest/

Models are provided at the root of the module and can be imported as follows:

.. code-block:: python

    from hostedpi import Pi3ServerSpec, Pi4ServerSpec, SSHKeySources

They can be constructed using keyword arguments:

.. code-block:: python

    pi4_spec = Pi4ServerSpec(
        memory_gb=8,
        cpu_speed=2000,
        disk=30,
        os_image="rpi-bookworm-arm64",
    )

Alternatively, they can be constructed from a dictionary using ``model_validate``:

.. code-block:: python

    from hostedpi import Pi4ServerSpec

    mypi = {
        "memory_gb": 8,
        "cpu_speed": 2000,
        "disk": 30,
        "os_image": "rpi-bookworm-arm64",
    }

    pi4_spec = Pi4ServerSpec.model_validate(mypi)

Raspberry Pi specifications
===========================

.. autoclass:: hostedpi.models.specs.Pi3ServerSpec
    :members: memory_gb, cpu_speed, disk, os_image
    :undoc-members:

.. autoclass:: hostedpi.models.specs.Pi4ServerSpec
    :members: memory_gb, cpu_speed, disk, os_image
    :undoc-members:

SSH Key management
==================

.. autoclass:: hostedpi.models.sshkeys.SSHKeySources
    :members: ssh_keys, ssh_key_path, github_usernames, launchpad_usernames, collect
    :undoc-members:

Pi info
=======

.. autoclass:: hostedpi.models.mythic.responses.PiInfo()
    :members: boot_progress, disk_size, initialised_keys, ipv6_address, ipv6_network, is_booting, location, model_full, nic_speed, power, ssh_port
    :undoc-members:
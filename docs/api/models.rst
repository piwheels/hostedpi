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
    :members: ssh_keys, ssh_key_path, github_usernames, launchpad_usernames
    :undoc-members:

Usage
=====

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
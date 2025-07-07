======
Models
======

The **hostedpi** module uses `Pydantic`_ models to validate and serialize data structures. The
models provided give a simple way to specify the requirements for a Raspberry Pi server, including
the specifications of the Raspberry Pi, and sources the SSH keys to be added to the server.

.. _Pydantic: https://docs.pydantic.dev/latest/

Models are provided at the root of the module and can be imported as follows:

.. code-block:: python

    from hostedpi import Pi3ServerSpec, Pi4ServerSpec, SSHKeySources, PiInfo, PiInfoBasic, Settings

They can be constructed using keyword arguments:

.. code-block:: python

    pi4_spec = Pi4ServerSpec(
        memory_gb=8,
        cpu_speed=2000,
        disk=30,
        os_image="rpi-bookworm-arm64",
    )

Alternatively, they can be constructed from a dictionary using
`model_validate`_ (or similar):

.. _model_validate: https://docs.pydantic.dev/latest/api/base_model/#pydantic.BaseModel.model_validate

.. code-block:: python

    mypi = {
        "memory_gb": 8,
        "cpu_speed": 2000,
        "disk": 30,
        "os_image": "rpi-bookworm-arm64",
    }

    pi4_spec = Pi4ServerSpec.model_validate(mypi)

Default values are provided for most fields, so these can be omitted.

When using the models, you can access the attributes directly using dot notation:

.. code-block:: python

    print(pi.info.boot_progress)

Raspberry Pi specifications
===========================

.. autoclass:: hostedpi.models.specs.Pi3ServerSpec()
    :members: memory_gb, cpu_speed, disk, os_image
    :undoc-members:

.. autoclass:: hostedpi.models.specs.Pi4ServerSpec()
    :members: memory_gb, cpu_speed, disk, os_image
    :undoc-members:

SSH Key management
==================

.. autoclass:: hostedpi.models.sshkeys.SSHKeySources()
    :members: ssh_keys, ssh_key_path, github_usernames, launchpad_usernames, collect
    :undoc-members:

Pi info
=======

.. autoclass:: hostedpi.models.mythic.responses.PiInfo()
    :members: boot_progress, disk_size, initialised_keys, ipv6_address, ipv6_network, is_booting, location, model_full, nic_speed, power, ssh_port, model, memory, cpu_speed, provision_status
    :undoc-members:

.. autoclass:: hostedpi.models.mythic.responses.PiInfoBasic()
    :members: model, memory, cpu_speed
    :undoc-members:

.. autoclass:: hostedpi.models.mythic.responses.ProvisioningServer()
    :members: provision_status
    :undoc-members:

Settings
========

.. warning::
    
    This is for advanced use only. Most users should not need to interact with the settings
    directly, as they are automatically loaded from :doc:`../env`.

.. autoclass:: hostedpi.settings.Settings()
    :members: id, secret, auth_url, api_url
    :undoc-members:
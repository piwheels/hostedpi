==
Pi
==

.. autoclass:: hostedpi.pi.Pi
    :members:

Usage
=====

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
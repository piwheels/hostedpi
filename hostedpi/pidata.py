from ipaddress import IPv6Address, IPv6Network
from typing import Union

from .models.responses import ServerResponse


class PiData:
    def __init__(self, name: str, data: ServerResponse):
        self.name = name
        self.data = data

    @property
    def boot_progress(self) -> str:
        """
        A string representing the Pi's boot progress. Can be ``booted``, ``powered off`` or a
        particular stage of the boot process if currently booting.
        """
        if self.data.boot_progress:
            return self.data.boot_progress
        return "booted" if self.power else "powered off"

    @property
    def disk_size(self) -> Union[int, None]:
        """
        The Pi's disk size in GB
        """
        return self.data.disk_size

    @property
    def initialised_keys(self) -> bool:
        """
        A boolean representing whether or not the Pi has been initialised with SSH keys
        """
        return self.data.initialised_keys

    @property
    def ipv4_ssh_port(self) -> int:
        """
        The SSH port to use when connecting via the IPv4 proxy
        """
        return self.data.ssh_port

    @property
    def ipv6_address(self) -> IPv6Address:
        """
        The Pi's IPv6 address as an :class:`~ipaddress.IPv6Address` object
        """
        return self.data.ipv6_address

    @property
    def ipv6_network(self) -> IPv6Network:
        """
        The Pi's IPv6 network as an :class:`~ipaddress.IPv6Network` object
        """
        return self.data.ipv6_network

    @property
    def is_booting(self) -> bool:
        """
        A boolean representing whether or not the Pi is currently booting
        """
        return self.data.is_booting

    @property
    def location(self) -> str:
        """
        The Pi's physical location (data centre)
        """
        return self.data.location

    @property
    def model(self) -> int:
        """
        The Pi's model (3 or 4)
        """
        return self.data.model

    @property
    def model_full(self) -> Union[str, None]:
        """
        The Pi's model name (3B, 3B+ or 4B)
        """
        return self.data.model_full

    @property
    def power(self) -> bool:
        """
        A boolean representing whether or not the Pi is currently powered on
        """
        return self.data.power

    @property
    def provision_status(self) -> str:
        """
        A string representing the provision status of the Pi. Can be "provisioning", "initialising"
        or "live".
        """
        return self.data.provision_status

    @property
    def ipv4_ssh_command(self) -> str:
        """
        The SSH command required to connect to the Pi over IPv4
        """
        return f"ssh -p {self.ipv4_ssh_port} root@ssh.{self.name}.hostedpi.com"

    @property
    def ipv6_ssh_command(self) -> str:
        """
        The SSH command required to connect to the Pi over IPv6
        """
        return f"ssh root@[{self.ipv6_address}]"

    @property
    def ipv4_ssh_config(self) -> str:
        """
        A string containing the IPv4 SSH config for the Pi. The contents could be added to an SSH
        config file for easy access to the Pi.
        """
        return f"""Host {self.name}
    user root
    port {self.ipv4_ssh_port}
    hostname ssh.{self.name}.hostedpi.com
        """.strip()

    @property
    def ipv6_ssh_config(self) -> str:
        """
        A string containing the IPv6 SSH config for the Pi. The contents could be added to an SSH
        config file for easy access to the Pi.
        """
        return f"""Host {self.name}
    user root
    hostname {self.ipv6_address}
        """.strip()

    @property
    def url(self) -> str:
        """
        The http version of the hostedpi.com URL of the Pi.

        .. note::
            Note that a web server must be installed on the Pi for the URL to be resolvable.
        """
        return f"http://www.{self.name}.hostedpi.com"

    @property
    def url_ssl(self) -> str:
        """
        The https version of the hostedpi.com URL of the Pi.

        .. note::
            Note that a web server must be installed on the Pi for the URL to be resolvable, and an
            SSL certificate must be created.

            See https://letsencrypt.org/
        """
        return f"https://www.{self.name}.hostedpi.com"

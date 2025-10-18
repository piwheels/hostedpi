=========
Changelog
=========

.. warning::

    Note that the library is currently in beta. The API and CLI are not yet stable and may change.
    Once the library reaches v1.0, it will be considered stable. Please consider giving feedback to
    help stabilise the API.

Release 0.4.6 (2025-10-18)
==========================

- Allowed ``user`` to be ``None`` in :meth:`~hostedpi.pi.Pi.get_ipv4_ssh_command()`,
  :meth:`~hostedpi.pi.Pi.get_ipv6_ssh_command()`, :meth:`~hostedpi.pi.Pi.get_ipv4_ssh_config()` and
  :meth:`~hostedpi.pi.Pi.get_ipv6_ssh_config()` methods to :class:`~hostedpi.pi.Pi`
- Allowed ``user`` to be ``None`` in :meth:`~hostedpi.picloud.PiCloud.get_ipv4_ssh_config()` and
  :meth:`~hostedpi.picloud.PiCloud.get_ipv6_ssh_config()` method to
  :class:`~hostedpi.picloud.PiCloud`
- Removed ``--full`` option from :doc:`cli/create` command, and simplified the output to a single
  table

Release 0.4.5 (2025-10-11)
==========================

- Fixup release

Release 0.4.4 (2025-10-10)
==========================

- Added :meth:`~hostedpi.pi.Pi.get_ipv4_ssh_command()`,
  :meth:`~hostedpi.pi.Pi.get_ipv6_ssh_command()`, :meth:`~hostedpi.pi.Pi.get_ipv4_ssh_config()` and
  :meth:`~hostedpi.pi.Pi.get_ipv6_ssh_config()` methods to :class:`~hostedpi.pi.Pi`
- Added :meth:`~hostedpi.picloud.PiCloud.get_ipv4_ssh_config()` and
  :meth:`~hostedpi.picloud.PiCloud.get_ipv6_ssh_config()` method to
  :class:`~hostedpi.picloud.PiCloud`

Release 0.4.3 (2025-07-25)
==========================

- Added :attr:`~hostedpi.pi.Pi.ipv6_ssh_hostname` and :attr:`~hostedpi.pi.Pi.hostname` properties to
  :class:`~hostedpi.pi.Pi`
- Changed :attr:`~hostedpi.pi.Pi.ipv6_ssh_command` and :attr:`~hostedpi.pi.Pi.ipv6_ssh_config` to
  use the hostname rather than the IPv6 address

Release 0.4.2 (2025-07-19)
==========================

- Fixed bug in adding SSH keys from file on the command line with :doc:`cli/ssh/keys/add`
- Added :attr:`~hostedpi.pi.Pi.ipv4_ssh_hostname` property to :class:`~hostedpi.pi.Pi`

Release 0.4.1 (2025-07-08)
==========================

- New codebase making use of `Pydantic`_ models
- New command line interface using `Typer`_
- Added test suite

.. _Pydantic: https://docs.pydantic.dev/
.. _Typer: https://typer.tiangolo.com/
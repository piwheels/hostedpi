=========
Changelog
=========

.. warning::

    Note that the library is currently in beta. The API and CLI are not yet stable and may change.
    Once the library reaches v1.0, it will be considered stable. Please consider giving feedback to
    help stabilise the API.

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
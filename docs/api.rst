===
API
===

.. module:: hostedpi

.. currentmodule:: hostedpi

This page describes the methods and properties available in the
:class:`~hostedpi.picloud.PiCloud` and :class:`~hostedpi.pi.Pi` classes and are
intended as a useful reference to the functionality provided.

The way to use the module is to import the :class:`~hostedpi.picloud.PiCloud`
class and initialise it with your API keys. This will allow you to provision
new Pi services with the :meth:`~hostedpi.picloud.PiCloud.create_pi` method or
access existing services from the :attr:`~hostedpi.picloud.PiCloud.pis` property.

Once you have a connected :class:`~hostedpi.picloud.PiCloud` instance and access
to newly or previously created :class:`~hostedpi.pi.Pi` instances, the following
API documentation should prove useful to show what you can do with the API via
the *hostedpi* module.

You can authenticate by passing your API ID and secret as arguments to the
:class:`~hostedpi.picloud.PiCloud` constructor:

.. code-block:: pycon

    >>> from hostedpi import PiCloud
    >>> cloud = PiCloud('YOUR ID', 'YOUR SECRET')

or set them in environment variables instead:

.. code-block:: console

    $ export HOSTEDPI_ID='YOUR ID'
    $ export HOSTEDPI_SECRET='YOUR SECRET'

.. code-block:: pycon

    >>> from hostedpi import PiCloud
    >>> cloud = PiCloud()

PiCloud
=======

.. autoclass:: hostedpi.picloud.PiCloud
    :members:

Pi
==

.. autoclass:: hostedpi.pi.Pi()
    :members:

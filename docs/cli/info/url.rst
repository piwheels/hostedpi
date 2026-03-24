=================
hostedpi info url
=================

.. program:: hostedpi-info-url

Get the URL of a Raspberry Pi server

.. code-block:: text

    Usage: hostedpi info url [OPTIONS] NAME

Arguments
=========

.. option:: name [str]

    Name of the Raspberry Pi server

Options
=======

.. option:: --ssl

    Show the URL with HTTPS instead of HTTP

.. option:: --help

    Show this message and exit

Usage
=====

Get the HTTP URL of a Pi:

.. code-block:: console

    $ hostedpi info url mypi
    http://www.mypi.hostedpi.com

Get the HTTPS URL of a Pi:

.. code-block:: console

    $ hostedpi info url mypi --ssl
    https://www.mypi.hostedpi.com

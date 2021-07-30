=============
hostedpi keys
=============

Show the SSH keys currently on a Pi

Synopsis
========

.. code-block:: text

    hostedpi hostedpi keys [-h] name

Description
===========

.. program:: hostedpi-keys

.. option:: name

    The name of the Pi to show keys for

.. option:: -h, --help

    Show this help message and exit

Usage
=====

Show the SSH keys currently on a Pi:

.. code-block:: console

    $ hostedpi keys mypi
    ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDSkT3A1j89RT/540ghIMHXIVwNlAEM3WtmqVG7YN/wYwtsJ8iCszg4/lXQsfLFxYmEVe8L9atgtMGCi5QdYPl4X/c+5YxFfm88Yjfx+2xEgUdOr864eaI22yaNMQ0AlyilmK+PcSyxKP4dzkf6B5Nsw8lhfB5n9F5md6GHLLjOGuBbHYlesKJKnt2cMzzS90BdRk73qW6wJ+MCUWo+cyBFZVGOzrjJGEcHewOCbVs+IJWBFSi6w1enbKGc+RY9KrnzeDKWWqzYnNofiHGVFAuMxrmZOasqlTIKiC2UK3RmLxZicWiQmPnpnjJRo7pL0oYM9r/sIWzD6i2S9szDy6aZ alice@gonzo

Save the output into a file:

.. code-block:: console

    $ hostedpi keys mypi > keys.txt

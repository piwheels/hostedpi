======================
Command line interface
======================

hostedpi
========

The ``hostedpi`` command is a multi-purpose utility for common actions
interacting with the API.

This program requires API keys to be provided using environment variables
``HOSTEDPI_ID`` and ``HOSTEDPI_SECRET``.

The following commands are available:

:doc:`cli_test`
    Test a connection to the Mythic Beasts API

:doc:`cli_images`
    Retrieve the list of operating system images available for the given Pi
    model

:doc:`cli_list`
    List all Pis in the account

:doc:`cli_show`
    Show the information about a Pi in the account

:doc:`cli_create`
    Provision a new Pi server in the account

:doc:`cli_reboot`
    Reboot a Pi in the account

:doc:`cli_on`
    Power on a Pi in the account

:doc:`cli_off`
    Power off a Pi in the account

:doc:`cli_cancel`
    Cancel a Pi server in the account

:doc:`cli_keys`
    Show the SSH keys currently on the Pi

:doc:`cli_add_key`
    Add an SSH key to the Pi

:doc:`cli_copy_keys`
    Copy all SSH keys from one Pi to another

:doc:`cli_remove_keys`
    Remove all SSH keys from the Pi

:doc:`cli_import_keys_gh`
    Import SSH keys from GitHub and add them to the Pi

:doc:`cli_import_keys_lp`
    Import SSH keys from Launchpad and add them to the Pi

======================
Command line interface
======================

The ``hostedpi`` command provides a command line interface to provision and manage Raspberry Pi
servers in a Mythic Beasts account.

This program requires API keys to be provided using environment variables ``HOSTEDPI_ID`` and
``HOSTEDPI_SECRET``. See :doc:`getting_started` for more information on how to obtain and configure
these.

Run ``hostedpi`` or ``hostedpi --help`` to see a list of available commands and options:

.. code-block:: console

    $ hostedpi         
                                                                                                
    Usage: hostedpi [OPTIONS] COMMAND [ARGS]...                                                
                                                                                                
    ╭─ Options ────────────────────────────────────────────────────────────────────────────────╮
    │ --install-completion          Install completion for the current shell.                  │
    │ --show-completion             Show completion for the current shell, to copy it or       │
    │                               customize the installation.                                │
    │ --help                        Show this message and exit.                                │
    ╰──────────────────────────────────────────────────────────────────────────────────────────╯
    ╭─ Commands ───────────────────────────────────────────────────────────────────────────────╮
    │ test     Test a connection to the Mythic Beasts API                                      │
    │ images   List operating system images available for Raspberry Pi servers                 │
    │ list     List Raspberry Pi servers                                                       │
    │ table    List Raspberry Pi server information in a table                                 │
    │ create   Provision one or more new Raspberry Pi servers                                  │
    │ status   Get the current status of one or more Raspberry Pi servers                      │
    │ on       Power on one or more Raspberry Pi servers                                       │
    │ off      Power off one or more Raspberry Pi servers                                      │
    │ reboot   Reboot one or more Raspberry Pi servers                                         │
    │ cancel   Unprovision one or more Raspberry Pi servers                                    │
    │ ssh      SSH access management commands                                                  │
    ╰──────────────────────────────────────────────────────────────────────────────────────────╯

Commands
========

.. toctree::
    :maxdepth: 1

    cli_test
    cli_images
    cli_list
    cli_table
    cli_create
    cli_status
    cli_on
    cli_off
    cli_reboot
    cli_cancel
    cli_ssh

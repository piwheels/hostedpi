===============
hostedpi create
===============                                                                                                                                                                                                           
                                                                                                                                                                                                                                                           
Provision one or more new Raspberry Pi servers

.. code-block:: text

    Usage: hostedpi create [OPTIONS] [NAMES]...

.. program:: hostedpi-create

Arguments
=========

.. option:: names [list[str]] = None

    Names of the Raspberry Pi servers to provision

    If no names are provided, a generated name will be generated. Use in combination with
    :option:`--number` to create multiple servers with generated names.

Options
=======

.. option:: --model [int] [required]

    Raspberry Pi Model

    Available models are 3 and 4

.. option:: --number [int] = None

    Number of Raspberry Pi servers to create

    Can be provided when no :option:`names` are provided. If :option:`names` are provided, the
    number of names will determine the number of servers to create.

.. option:: --disk [int] = 10

    Disk size in GB. Must be a multiple of 10.

.. option:: --memory [int] = None

    Memory in MB. Valid options depend on the model chosen. Default is the lowest available for the
    model.

.. option:: --cpu-speed [int] = None

    CPU speed in MHz. Valid options depend on the model chosen. Default is the lowest available for
    the model.

.. option:: --os-image [str] = None

    Operating system image. Default is determined by Mythic Beasts.

.. option:: --wait [bool] = False

    Wait and poll for status to be available before returning

    Supply with :option:`--full` to show the full table of Raspberry Pi server info when the server
    is provisioned

.. option:: --ssh-key-path [path] = None

    Path to the SSH key to install on the Raspberry Pi server

.. option:: --ssh-import-github [str] = None

    Usernames to import SSH keys from GitHub

    Can be provided multiple times

.. option:: --ssh-import-launchpad [str] = None

    Usernames to import SSH keys from Launchpad

    Can be provided multiple times

.. option:: --full [bool] = False

    Show full table of Raspberry Pi server info when the server is provisioned

    Can only provided along with :option:`--wait`

.. option:: --help

    Show this message and exit

Usage
=====

Provision a new Pi 3 using the default Pi 3 spec, and wait for it to be provisioned:

.. code-block:: console

    $ hostedpi create mypi --model 3 --wait
    Server provisioned
    ┏━━━━━━━┳━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━┓
    ┃ Name  ┃ Model ┃ Memory ┃ CPU Speed ┃
    ┡━━━━━━━╇━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━┩
    │ mypi  │ 3     │ 1 GB   │ 1.2 GHz   │
    └───────┴───────┴────────┴───────────┘

Provision two new Pi 4 servers with generated names, using the default Pi 4 spec:

.. code-block:: console

    $ hostedpi create --model 4 --number 2 --wait
    Server provisioned
    ┏━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━┓
    ┃ Name      ┃ Model ┃ Memory ┃ CPU Speed ┃
    ┡━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━┩
    │ c8046pxjf │ 4     │ 4 GB   │ 1.5 GHz   │
    └───────────┴───────┴────────┴───────────┘
    Server provisioned
    ┏━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━┓
    ┃ Name      ┃ Model ┃ Memory ┃ CPU Speed ┃
    ┡━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━┩
    │ c8046pg5e │ 4     │ 4 GB   │ 1.5 GHz   │
    └───────────┴───────┴────────┴───────────┘

.. warning::
    If no :option:`names` are provided, and :option:`--wait` is not provided, the command will return
    immediately without the name of the provisioned Pi server.

Provision a new Pi 4 using custom settings:

.. code-block:: console

    $ hostedpi create mypi4 --model 4 --memory 8192 --cpu-speed 2000 --disk 60 --os-image rpi-jammy-arm64 --ssh-key-path ~/.ssh/id_rsa.pub --wait
    Server provisioned
    ┏━━━━━━━┳━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━┓
    ┃ Name  ┃ Model ┃ Memory ┃ CPU Speed ┃
    ┡━━━━━━━╇━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━┩
    │ mypi4 │ 4     │ 8 GB   │ 2.0 GHz   │
    └───────┴───────┴────────┴───────────┘

.. note::
    Use the :doc:`cli_images` command to retrieve the available operating system images for each Pi
    model.
    
Provision a new Pi with SSH keys imported from multiple users on GitHub and Launchpad:

.. code-block:: console

    $ hostedpi create mypi --model 4 --ssh-import-github user1 --ssh-import-github user2 --ssh-import-launchpad user3


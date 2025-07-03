===============
Getting started
===============

This page contains a simple tutorial to help you get started by creating a Mythic Beasts account,
create an API key, use the command line interface and the Python module.

Create a Mythic Beasts account
==============================

Sign up: https://www.mythic-beasts.com/user/login

Create an API key
=================

1. Log in to your Mythic Beasts account: https://www.mythic-beasts.com/user/login

2. Open the API Keys page: https://www.mythic-beasts.com/customer/api-users

3. Enter a descriptive name for your API key, for your own reference

4. Check the *Raspberry Pi Provisioning* box

5. Click the *Create API key* button

6. Make a note of the API ID and Secret. You'll need them to use this Python module, and you can't
retrieve them after this screen is gone.

.. note::
    If you lose your keys, you can simply reset them or create a new API key.

Install the hostedpi module
===========================

For a system-wide installation of the CLI only, we recommend you use ``pipx``. See the `pipx docs`_
for more information.

.. _pipx docs: https://github.com/pypa/pipx?tab=readme-ov-file#install-pipx

To install the Python library, you can install into an activated virtual environment:

.. code-block:: console

    $ pip install hostedpi

Set your environment variables
==============================

You can either set your API ID and secret in your shell's config file (e.g. ``~/.bashrc`` or
``~/.zshrc``), or you can create a ``.env`` file in your working directory.

Shell config
------------

Add the following lines to your shell's config file (e.g. ``~/.bashrc`` or ``~/.zshrc``):

.. code-block:: console

    export HOSTEDPI_ID='YOUR ID'
    export HOSTEDPI_SECRET='YOUR SECRET'

Be sure to restart your terminal after setting these.

.env file
---------

Alternatively, you can create a ``.env`` file in your working directory with the following:

.. code-block:: console

    HOSTEDPI_ID='YOUR ID'
    HOSTEDPI_SECRET='YOUR SECRET'

Test your API keys
==================

To test your API connection, try running the following command in a terminal:

.. code-block:: console

    $ hostedpi test
    Connected to the Mythic Beasts API

This message means your API credentials were found and a successful connection was made.

You may prefer to test by setting your API ID and secret within the test command line:

.. code-block:: console

    $ HOSTEDPI_ID='YOUR ID' HOSTEDPI_SECRET='YOUR SECRET' hostedpi test
    Connected to the Mythic Beasts API

If you already have Pis in your account, you can list them with:

.. code-block:: console

    $ hostedpi list
    pi123
    pi234
    pi345
    pi456

You can provision a new Pi with the following command:

.. code-block:: console

    $ hostedpi create mypi --model 3 --wait

More
====

* See the :doc:`cli` page for details of the possibilities provided by ready-made scripts
* See the API documentation for :class:`~hostedpi.picloud.PiCloud` and :class:`~hostedpi.pi.Pi` for
  details of the Python module API
* See the :doc:`recipes` page for ideas of what you can do with this module

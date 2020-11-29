===============
hostedpi cancel
===============

.. program:: hostedpi-cancel

Cancel one or more Pis in the account

.. code-block:: text

    positional arguments:
      names       The names of the Pis to cancel

    optional arguments:
      -h, --help  show this help message and exit
      -y, --yes   Proceed without confirmation

Usage
=====

Cancel a Pi:

.. code-block:: console

    $ hostedpi cancel mypi
    Cancelling 1 Pi. Proceed? [Y/n]
    mypi cancelled

.. note::
    You can cancel by entering ``n`` or interrupting with ``Ctrl + C``.

.. note::
    Unlike other commands, there is no implicit targeting of all Pis. Pis must
    be listed explicitly to be cancelled.

Cancel multiple Pis:

.. code-block:: console

    $ hostedpi cancel mypi mypi2
    Cancelling 2 Pis. Proceed? [Y/n]
    mypi cancelled
    mypi2 cancelled

Cancel a Pi without the confirmation step:

.. code-block:: console

    $ hostedpi cancel mypi -y
    mypi cancelled

.. warning::
    Be careful!

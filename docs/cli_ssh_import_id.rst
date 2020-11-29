======================
hostedpi ssh-import-id
======================

.. program:: hostedpi-ssh-import-id

Import SSH keys from GitHub or Launchpad and add them to one or more Pis

.. code-block:: text

    positional arguments:
      names                 The names of the Pis to import keys onto

    optional arguments:
      -h, --help            show this help message and exit
      --gh [github username]
                            The GitHub username to import keys from
      --lp [launchpad username]
                            The Launchpad username to import keys from

Usage
=====

Import keys from GitHub onto a Pi:

.. code-block:: console

    $ hostedpi ssh-import-id mypi --gh bennuttall
    4 keys retrieved from GitHub

    4 keys added to mypi

Import keys from GitHub onto multiple Pis:

.. code-block:: console

    $ hostedpi ssh-import-id mypi mypi2 --gh bennuttall
    4 keys retrieved from GitHub

    0 keys added to mypi
    4 keys added to mypi2

.. note::
    If no names of Pis are given, the key count will be shown for all Pis in the
    account

.. note::
    Keys are counted before and after addition, and de-duplicated, so if a key
    is already found on the Pi, it will show as not having been added, as above.

Import keys from GitHub and Launchpad onto a Pi:

.. code-block:: console

    $ hostedpi ssh-import-id mypi --gh bennuttall --lp bennuttall
    4 keys retrieved from GitHub
    1 key retrieved from Launchpad

    1 key added to mypi

.. note::
    Keys are counted before and after addition, and de-duplicated, so if a key
    is already found on the Pi, it will show as not having been added, as above.

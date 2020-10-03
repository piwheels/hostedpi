===========
Development
===========

This page contains reference material for those interested in developing and
contributing to the *hostedpi* module.

The project source code is hosted on GitHub at https://github.com/piwheels/hostedpi
which also includes the `issue tracker`_.

.. _issue tracker: https://github.com/piwheels/hostedpi/issues

Setting up for Development
==========================

1. Clone the repository and enter the directory:

    .. code-block:: console

        $ git clone https://github.com/piwheels/hostedpi
        $ cd hostedpi

2. Create a virtual environment:

    .. code-block:: console

        $ mkvirtualenv -p `which python3` hostedpi

3. Install the project for development:

    .. code-block:: console

        $ make develop

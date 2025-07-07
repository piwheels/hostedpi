===========
Development
===========

This page contains reference material for those interested in developing and contributing to the
**hostedpi** module.

The project source code is hosted on GitHub at https://github.com/piwheels/hostedpi which also
includes the `issue tracker`_ and `CI`_.

.. _issue tracker: https://github.com/piwheels/hostedpi/issues
.. _CI: https://github.com/piwheels/hostedpi/actions

Setting up for Development
==========================

1. Clone the repository and enter the directory:

    .. code-block:: console

        $ git clone https://github.com/piwheels/hostedpi
        $ cd hostedpi

2. Create a virtual environment e.g. using `virtualenvwrapper`_:

    .. code-block:: console

        $ mkvirtualenv hostedpi

    .. _virtualenvwrapper: https://virtualenvwrapper.readthedocs.io/

3. Install the project for development:

    .. code-block:: console

        $ make develop

Run the tests
-------------

Run the tests in your environment with:

    .. code-block:: console

        $ make test

Or you can run the tests directly with `pytest` for more control:

    .. code-block:: console

        $ pytest -vv

Format code
-----------

Format code with ``isort`` and ``black``:

    .. code-block:: console

        $ make format

GitHub Actions
--------------

GitHub Actions are used to run tests and formatter checks on every commit and pull request:
https://github.com/piwheels/hostedpi/actions
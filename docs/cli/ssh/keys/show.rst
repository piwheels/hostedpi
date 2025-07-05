======================
hostedpi ssh keys show
======================

.. program:: hostedpi-ssh-keys-show

List the SSH keys on a Raspberry Pi server as plaintext

.. code-block:: text

    Usage: hostedpi ssh keys show [OPTIONS] NAME

Arguments
=========

.. option:: name [str] [required]

    Name of the Raspberry Pi server to show SSH keys for

Options
=======

.. option:: --help

    Show this message and exit

Usage
=====

List keys on a Pi:

.. code-block:: console

    $ hostedpi ssh keys show mypi
    ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQD4wraoX2TyK4rJtXepAdyVUk89OXbSkD/7CB5BmW1LpLlc9NfZkfmWIx2tMDhpSpbob3MNAsqNkD/vm6Rp71nvSxCJ0UBPgp3Qhx8/QpgNC4nAe9LgLzbqvGNrOv+pq6tjP42mHrXxP4W/QHMlKiIXvh3ZG5s5AxpDG9+oUyhHmK7w0/z51aKXlB4dwQQsPL1LHlhsyaGXoPt1w+ucwJmEo6Fr8FfdI5dPC/Y0HYi8A0HzLxoOdPGUKKQzPdZASJ9cXm0BiLMO4NHr7egJGEKbChDoy4RIIibX5tF60jUV1LkIvSXDIoB9FSEIxM5bh/j/114kgC2C7KI4Da7EuVQckpqIkGSdD8jR43np3b0I/7GZomvwy9bltI1c4L9PAlYNnhGz5h27nQROSkdL80Chwi4leE34W6Yfs9UPojdiX61KI7jjOTW8G7pf7kft8hq0r8CVB2UrbzorkA/jkQavcOMrq3IVm8OlhH7sfyJD9TqJ08ANPV8+nladOFnlBoc= ben@fern
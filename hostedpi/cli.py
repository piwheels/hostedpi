import os
import sys
import argparse

import requests

from .picloud import PiCloud
from .utils import read_ssh_key, ssh_import_id
from .exc import HostedPiException, MythicAuthenticationError
from .__version__ import __version__


class CLI:
    def __init__(self):
        self._args = None
        self._commands = None
        self._config = None
        self._parser = None
        self._output = None
        self._store = None
        self._cloud = None
        self._pis = None

    def __call__(self, args=None):
        self._args = self.parser.parse_args(args)
        try:
            self._args.func()
        except HostedPiException as e:
            print("Error:", str(e).replace(': ', '\n'))
            return 2

    @property
    def cloud(self):
        if self._cloud is None:
            API_ID = os.environ.get('HOSTEDPI_ID')
            API_SECRET = os.environ.get('HOSTEDPI_SECRET')
            if API_ID is None or API_SECRET is None:
                print("HOSTEDPI_ID and HOSTEDPI_SECRET environment variables "
                      "must be set")
            try:
                self._cloud = PiCloud(API_ID, API_SECRET)
            except MythicAuthenticationError as e:
                print("Failed to authenticate:", e)
                return
        return self._cloud

    @property
    def pis(self):
        if self._pis is None:
            self._pis = self.cloud.pis
        return self._pis

    @property
    def parser(self):
        """
        The parser for all the sub-commands that the script accepts. The
        parser's defaults are derived from the configuration obtained from
        :attr:`config`. Returns the newly constructed argument parser.
        """
        if self._parser is None:
            self._parser, self._commands = self._get_parser()
        return self._parser

    @property
    def commands(self):
        """
        A dictionary mapping command names to their sub-parser.
        """
        if self._commands is None:
            self._parser, self._commands = self._get_parser()
        return self._commands

    def _get_parser(self):
        parser = argparse.ArgumentParser(
            description=(
                "hostedpi is a tool for provisioning and managing Raspberry Pis "
                "in the Mythic Beasts Pi Cloud"))
        parser.add_argument(
            '--version', action='version', version=__version__)
        parser.set_defaults(func=self.do_help)
        commands = parser.add_subparsers(title=("commands"))

        help_cmd = commands.add_parser(
            "help", aliases=["h"],
            description=(
                "With no arguments, displays the list of hostedpi "
                "commands. If a command name is given, displays the "
                "description and options for the named command. If a "
                "setting name is given, displays the description and "
                "default value for that setting."),
            help=("Displays help about the specified command or setting"))
        help_cmd.add_argument(
            "cmd", metavar="cmd", nargs='?',
            help=("The name of the command to output help for")
        )
        help_cmd.set_defaults(func=self.do_help)

        test_cmd = commands.add_parser(
            "test", aliases=["connect"],
            description=(
                "Test a connection to the Mythic Beasts API using API ID and "
                "secret in environment variables."),
            help=("Test a connection to the Mythic Beasts API"))
        test_cmd.set_defaults(func=self.do_test)

        get_images_cmd = commands.add_parser(
            "images", aliases=["get-images"],
            description=(
                "Retrieve the list of operating system images available for the "
                "given Pi model."),
            help=("Retrieve the list of operating system images available"))
        get_images_cmd.add_argument(
            "model", metavar="model", nargs='?',
            help=("The Pi model number (3 or 4) to get operating systems for")
        )
        get_images_cmd.set_defaults(func=self.do_get_images)

        list_cmd = commands.add_parser(
            "list", aliases=["ls"],
            description=("List all Pis in the account"),
            help=("List all Pis in the account"))
        list_cmd.set_defaults(func=self.do_list)

        show_cmd = commands.add_parser(
            "show", aliases=["cat"],
            description=("Show the information about a Pi in the account"),
            help=("Show the information about a Pi in the account"))
        show_cmd.add_argument(
            "name", metavar="name", nargs='?',
            help=("The name of the Pi to show information for")
        )
        show_cmd.set_defaults(func=self.do_show)

        create_cmd = commands.add_parser(
            "create",
            description=("Provision a new Pi server in the account"),
            help=("Provision a new Pi server in the account"))
        create_cmd.add_argument(
            "name", metavar="name", nargs='?',
            help=("The name of the new Pi to provision")
        )
        create_cmd.add_argument(
            "model", metavar="model", nargs='?',
            help=("The model of the new Pi to provision (3 or 4)")
        )
        create_cmd.add_argument(
            "ssh_key_path", metavar="ssh_key_path", nargs='?',
            help=("The path to an SSH public key file to add to the Pi")
        )
        create_cmd.set_defaults(func=self.do_create)

        reboot_cmd = commands.add_parser(
            "reboot", aliases=["cycle"],
            description=("Reboot a Pi in the account"),
            help=("Reboot a Pi in the account"))
        reboot_cmd.add_argument(
            "name", metavar="name", nargs='?',
            help=("The name of the Pi to reboot")
        )
        reboot_cmd.set_defaults(func=self.do_reboot)

        power_on_cmd = commands.add_parser(
            "on", aliases=["poweron"],
            description=("Power on a Pi in the account"),
            help=("Power on a Pi in the account"))
        power_on_cmd.add_argument(
            "name", metavar="name", nargs='?',
            help=("The name of the Pi to power on")
        )
        power_on_cmd.set_defaults(func=self.do_power_on)

        power_off_cmd = commands.add_parser(
            "off", aliases=["poweroff"],
            description=("Power off a Pi in the account"),
            help=("Power off a Pi in the account"))
        power_off_cmd.add_argument(
            "name", metavar="name", nargs='?',
            help=("The name of the Pi to power off")
        )
        power_off_cmd.set_defaults(func=self.do_power_off)

        cancel_cmd = commands.add_parser(
            "cancel", aliases=["rm"],
            description=("Cancel a Pi server in the account"),
            help=("Cancel a Pi server in the account"))
        cancel_cmd.add_argument(
            "name", metavar="name", nargs='?',
            help=("The name of the Pi to cancel")
        )
        cancel_cmd.set_defaults(func=self.do_cancel)

        get_keys_cmd = commands.add_parser(
            "keys", aliases=["get-keys", "show-keys"],
            description=("Show the SSH keys currently on the Pi"),
            help=("Show the SSH keys currently on the Pi"))
        get_keys_cmd.add_argument(
            "name", metavar="name", nargs='?',
            help=("The name of the Pi to get keys for")
        )
        get_keys_cmd.set_defaults(func=self.do_get_keys)

        add_key_cmd = commands.add_parser(
            "add-key", aliases=["add-ssh-key"],
            description=("Add an SSH key to the Pi from a public key file"),
            help=("Add an SSH key to the Pi"))
        add_key_cmd.add_argument(
            "name", metavar="name", nargs='?',
            help=("The name of the Pi to get keys for")
        )
        add_key_cmd.add_argument(
            "ssh_key_path", metavar="ssh_key_path", nargs='?',
            help=("The path to an SSH public key file to add to the Pi")
        )
        add_key_cmd.set_defaults(func=self.do_add_key)

        copy_keys_cmd = commands.add_parser(
            "copy-keys", aliases=["cp"],
            description=("Copy all SSH keys from one Pi to another"),
            help=("Copy all SSH keys from one Pi to another"))
        copy_keys_cmd.add_argument(
            "name_src", metavar="name_src", nargs='?',
            help=("The name of the Pi to copy keys from")
        )
        copy_keys_cmd.add_argument(
            "name_dest", metavar="name_dest", nargs='?',
            help=("The name of the Pi to copy keys to")
        )
        copy_keys_cmd.set_defaults(func=self.do_copy_keys)

        remove_keys_cmd = commands.add_parser(
            "remove-keys", aliases=["remove-ssh-keys"],
            description=("Remove all SSH keys from the Pi"),
            help=("Remove all SSH keys from the Pi"))
        remove_keys_cmd.add_argument(
            "name", metavar="name", nargs='?',
            help=("The name of the Pi import keys onto")
        )
        remove_keys_cmd.set_defaults(func=self.do_remove_keys)

        import_keys_gh_cmd = commands.add_parser(
            "import-keys-gh", aliases=["import-ssh-keys-gh"],
            description=("Import SSH keys from GitHub and add them to the Pi"),
            help=("Import SSH keys from GitHub and add them to the Pi"))
        import_keys_gh_cmd.add_argument(
            "name", metavar="name", nargs='?',
            help=("The name of the Pi import keys onto")
        )
        import_keys_gh_cmd.add_argument(
            "username", metavar="username", nargs='?',
            help=("The GitHub username to import keys from")
        )
        import_keys_gh_cmd.set_defaults(func=self.do_import_keys_gh)

        import_keys_lp_cmd = commands.add_parser(
            "import-keys-lp", aliases=["import-ssh-keys-lp"],
            description=("Import SSH keys from Launchpad and add them to the Pi"),
            help=("Import SSH keys from Launchpad and add them to the Pi"))
        import_keys_lp_cmd.add_argument(
            "name", metavar="name", nargs='?',
            help=("The name of the Pi import keys onto")
        )
        import_keys_lp_cmd.add_argument(
            "username", metavar="username", nargs='?',
            help=("The Launchpad username to import keys from")
        )
        import_keys_lp_cmd.set_defaults(func=self.do_import_keys_lp)

        return parser, commands.choices

    def get_pi(self, name):
        try:
            return self.pis[name]
        except KeyError:
            print("Pi {} not found".format(self._args.name))

    def do_help(self):
        print("help")

    def do_test(self):
        if self.cloud:
            print("Connected to Mythic Beasts API")
        return 2

    def do_get_images(self):
        images = self.cloud.get_operating_systems(model=self._args.model)
        for name, label in images.items():
            print('{} ({})'.format(name, label))

    def do_list(self):
        for name in self.pis:
            print(name)

    def do_show(self):
        if self._args.name:
            return self.do_show_one(self._args.name)
        else:
            return self.do_show_all()

    def do_show_one(self, name):
        pi = self.get_pi(self._args.name)
        if not pi:
            return 2
        pi.pprint()

    def do_show_all(self):
        for pi in self.pis.values():
            pi.pprint()
            print()

    def do_create(self):
        name = self._args.name
        model = self._args.model
        ssh_key_path = self._args.ssh_key_path

        if model:
            if ssh_key_path:
                pi = self.cloud.create_pi(name, model=model,
                                          ssh_key_path=ssh_key_path)
            else:
                pi = self.cloud.create_pi(name, model=model)
        elif ssh_key_path:
            pi = self.cloud.create_pi(name, ssh_key_path=ssh_key_path)
        else:
            pi = self.cloud.create_pi(name)

        print("Pi {} provisioned successfully".format(name))
        print()
        pi.pprint()

    def do_reboot(self):
        if self._args.name:
            return self.do_reboot_one(self._args.name)
        else:
            return self.do_reboot_all()

    def do_reboot_one(self, name):
        pi = self.get_pi(self._args.name)
        if not pi:
            return 2
        pi.reboot()
        print("Pi", name, "rebooted")

    def do_reboot_all(self):
        for pi in self.pis.values():
            pi.reboot()

    def do_power_on(self):
        if self._args.name:
            return self.do_power_on_one(self._args.name)
        else:
            return self.do_power_on_all()

    def do_power_on_one(self, name):
        pi = self.get_pi(self._args.name)
        if not pi:
            return 2
        pi.on()
        print("Pi", name, "powered on")

    def do_power_on_all(self):
        for name, pi in self.pis.items():
            pi.on()
            print("Pi", name, "powered on")

    def do_power_off(self):
        if self._args.name:
            return self.do_power_off_one(self._args.name)
        else:
            return self.do_power_off_all()

    def do_power_off_one(self, name):
        pi = self.get_pi(self._args.name)
        if not pi:
            return 2
        pi.off()
        print("Pi", name, "powered off")

    def do_power_off_all(self):
        for name, pi in self.pis.items():
            pi.off()
            print("Pi", name, "powered off")

    def do_cancel(self):
        if self._args.name:
            return self.do_cancel_one(self._args.name)
        else:
            return self.do_cancel_all()

    def do_cancel_one(self, name):
        pi = self.get_pi(self._args.name)
        if not pi:
            return 2
        pi.cancel()
        print("Pi service", name, "cancelled")

    def do_cancel_all(self):
        for pi in self.pis.values():
            pi.cancel()
            print("Pi service", name, "cancelled")

    def do_get_keys(self):
        if self._args.name:
            return self.do_get_keys_one(self._args.name)
        else:
            return self.do_get_keys_all()

    def do_get_keys_one(self, name):
        pi = self.get_pi(self._args.name)
        if not pi:
            return 2
        print(*pi.ssh_keys, sep='\n')

    def do_get_keys_all(self):
        for name, pi in self.pis.items():
            num_keys = len(pi.ssh_keys)
            print(name + ':', num_keys, 'key' if num_keys == 1 else 'keys')

    def do_add_key(self):
        name = self._args.name
        ssh_key = read_ssh_key(self._args.ssh_key_path)

        if name:
            return self.do_add_key_one(name, ssh_key)
        else:
            return self.do_add_key_all(ssh_key)

    def do_add_key_one(self, name, ssh_key):
        pi = self.get_pi(self._args.name)
        if not pi:
            return 2
        pi.ssh_keys |= {ssh_key}

    def do_add_key_all(self, ssh_key):
        for name, pi in self.pis.items():
            pi.ssh_keys |= {ssh_key}

    def do_copy_keys(self):
        src_pi = self.get_pi(self._args.name_src)
        dest_pi = self.get_pi(self._args.name_dest)
        if not (src_pi and dest_pi):
            return 2

        dest_pi.ssh_keys |= src_pi.ssh_keys

    def do_remove_keys(self):
        pi = self.get_pi(self._args.name)
        if not pi:
            return 2

        pi.ssh_keys = set()

    def do_import_keys_gh(self):
        pi = self.get_pi(self._args.name)
        if not pi:
            return 2
        new_keys = pi.ssh_import_id(github={self._args.username})
        print("{} keys added".format(len(new_keys)))

    def do_import_keys_lp(self):
        pi = self.get_pi(self._args.name)
        if not pi:
            return 2
        new_keys = pi.ssh_import_id(launchpad={self._args.username})
        print("{} keys added".format(len(new_keys)))

main = CLI()

import os
import sys
import argparse

from .picloud import PiCloud
from .utils import read_ssh_key, ssh_import_id
from .exc import HostedPiException
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
            return self._args.func()
        except HostedPiException as e:
            sys.stderr.write("hostedpi error: {e}\n".format(e=e))
            return 2
        except KeyboardInterrupt:
            print("Operation cancelled during process")

    @property
    def cloud(self):
        if self._cloud is None:
            API_ID = os.environ.get('HOSTEDPI_ID')
            API_SECRET = os.environ.get('HOSTEDPI_SECRET')
            if API_ID is None or API_SECRET is None:
                print("HOSTEDPI_ID and HOSTEDPI_SECRET environment variables "
                      "must be set")
            self._cloud = PiCloud(API_ID, API_SECRET)
        return self._cloud

    @property
    def pis(self):
        if self._pis is None:
            self._pis = self.cloud.pis
        return self._pis

    @property
    def parser(self):
        """
        The parser for all the sub-commands that the script accepts. Returns the
        newly constructed argument parser.
        """
        if self._parser is None:
            self._parser, self._commands = self._get_parser()
        return self._parser

    @property
    def commands(self):
        "A dictionary mapping command names to their sub-parser."
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
        parser.set_defaults(func=self.do_help, cmd=None)
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
            "images",
            description=("Retrieve the list of operating system images available for the given Pi model."),
            help=("Retrieve the list of operating system images available for the given Pi model"))
        get_images_cmd.add_argument(
            "model", metavar="model", type=int,
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
            description=("Show the information about one or more Pis in the account"),
            help=("Show the information about one or more Pis in the account"))
        show_cmd.add_argument(
            "names", metavar="names", nargs='*',
            help=("The names of the Pis to show information for")
        )
        show_cmd.set_defaults(func=self.do_show_pis)

        create_cmd = commands.add_parser(
            "create",
            description=("Provision a new Pi in the account"),
            help=("Provision a new Pi in the account"))
        create_cmd.add_argument(
            "name", metavar="name",
            help=("The name of the new Pi to provision")
        )
        create_cmd.add_argument(
            "--model", metavar="model", type=int, nargs='?',
            help=("The model of the new Pi to provision (3 or 4)")
        )
        create_cmd.add_argument(
            "--disk", metavar="disk", type=int, nargs='?',
            help=("The disk size in GB")
        )
        create_cmd.add_argument(
            "--image", metavar="image", type=str, nargs='?',
            help=("The operating system image to use")
        )
        create_cmd.add_argument(
            "--ssh-key-path", metavar="ssh_key_path", nargs='?',
            help=("The path to an SSH public key file to add to the Pi")
        )
        create_cmd.set_defaults(func=self.do_create)

        provision_status_cmd = commands.add_parser(
            "status",
            description=("Get the provision status of one or more Pis"),
            help=("Get the provision status of one or more Pis"))
        provision_status_cmd.add_argument(
            "names", metavar="names", nargs='*',
            help=("The names of the Pis to get the provision status for")
        )
        provision_status_cmd.set_defaults(func=self.do_provision_status)

        power_status_cmd = commands.add_parser(
            "power",
            description=("Get the power status for one or more Pis"),
            help=("Get the power status (on/off) for one or more Pis"))
        power_status_cmd.add_argument(
            "names", metavar="names", nargs='*',
            help=("The names of the Pis to get the power status for")
        )
        power_status_cmd.set_defaults(func=self.do_power_status)

        reboot_cmd = commands.add_parser(
            "reboot",
            description=("Reboot one or more Pis in the account"),
            help=("Reboot one or more Pis in the account"))
        reboot_cmd.add_argument(
            "names", metavar="names", nargs='*',
            help=("The name of the Pi to reboot")
        )
        reboot_cmd.set_defaults(func=self.do_reboot)

        power_on_cmd = commands.add_parser(
            "on", aliases=["poweron"],
            description=("Power on one or more Pis in the account"),
            help=("Power on one or more Pis in the account"))
        power_on_cmd.add_argument(
            "names", metavar="names", nargs='*',
            help=("The name of the Pi to power on")
        )
        power_on_cmd.set_defaults(func=self.do_power_on)

        power_off_cmd = commands.add_parser(
            "off", aliases=["poweroff"],
            description=("Power off one or more Pis in the account"),
            help=("Power off one or more Pis in the account"))
        power_off_cmd.add_argument(
            "names", metavar="names", nargs='*',
            help=("The name of the Pi to power off")
        )
        power_off_cmd.set_defaults(func=self.do_power_off)

        cancel_cmd = commands.add_parser(
            "cancel",
            description=("Cancel one or more Pis in the account"),
            help=("Cancel one or more Pis in the account"))
        cancel_cmd.add_argument(
            "names", metavar="names", nargs='+',
            help=("The names of the Pis to cancel")
        )
        cancel_cmd.add_argument(
            "-y", "--yes",
            action="store_true",
            help=("Proceed without confirmation")
        )
        cancel_cmd.set_defaults(func=self.do_cancel)

        count_keys_cmd = commands.add_parser(
            "count-keys", aliases=["num-keys"],
            description=("Show the number of SSH keys currently on one or more Pis"),
            help=("Show the number of SSH keys currently on one or more Pis"))
        count_keys_cmd.add_argument(
            "names", metavar="names", nargs='*',
            help=("The names of the Pis to get keys for")
        )
        count_keys_cmd.set_defaults(func=self.do_count_keys)

        show_keys_cmd = commands.add_parser(
            "keys",
            description=("Show the SSH keys currently on a Pi"),
            help=("Show the SSH keys currently on a Pi"))
        show_keys_cmd.add_argument(
            "name", metavar="name",
            help=("The name of the Pi to get keys for")
        )
        show_keys_cmd.set_defaults(func=self.do_show_keys)

        add_key_cmd = commands.add_parser(
            "add-key",
            description=("Add an SSH key from a public key file to one or more Pis"),
            help=("Add an SSH key from a public key file to one or more Pis"))
        add_key_cmd.add_argument(
            "ssh_key_path", metavar="ssh_key_path", nargs='?',
            help=("The path to an SSH public key file to add to the Pi")
        )
        add_key_cmd.add_argument(
            "names", metavar="names", nargs='*',
            help=("The name of the Pis to add keys to")
        )
        add_key_cmd.set_defaults(func=self.do_add_key)

        copy_keys_cmd = commands.add_parser(
            "copy-keys", aliases=["cp"],
            description=("Copy all SSH keys from one Pi to one or more others"),
            help=("Copy all SSH keys from one Pi to one or more others"))
        copy_keys_cmd.add_argument(
            "name_src", metavar="name_src",
            help=("The name of the Pi to copy keys from")
        )
        copy_keys_cmd.add_argument(
            "names_dest", metavar="names_dest", nargs='*',
            help=("The name of the Pis to copy keys to")
        )
        copy_keys_cmd.set_defaults(func=self.do_copy_keys)

        remove_keys_cmd = commands.add_parser(
            "remove-keys",
            description=("Remove all SSH keys from one or more Pis"),
            help=("Remove all SSH keys from one or more Pis"))
        remove_keys_cmd.add_argument(
            "names", metavar="names", nargs='+',
            help=("The names of the Pis to remove keys from")
        )
        remove_keys_cmd.set_defaults(func=self.do_remove_keys)

        ssh_import_id_cmd = commands.add_parser(
            "ssh-import-id",
            description=("Import SSH keys from GitHub or Launchpad and add them to one or more Pis"),
            help=("Import SSH keys from GitHub or Launchpad and add them to one or more Pis"))
        ssh_import_id_cmd.add_argument(
            "names", metavar="names", nargs='*',
            help=("The names of the Pis to import keys onto")
        )
        ssh_import_id_cmd.add_argument(
            "--gh", metavar="github username", nargs='?',
            help=("The GitHub username to import keys from")
        )
        ssh_import_id_cmd.add_argument(
            "--lp", metavar="launchpad username", nargs='?',
            help=("The Launchpad username to import keys from")
        )
        ssh_import_id_cmd.set_defaults(func=self.do_ssh_import_id)

        ssh_command_cmd = commands.add_parser(
            "ssh-command",
            description=("Output the SSH command for one or more Pis in the account"),
            help=("Output the (IPv4 or IPv6) SSH command for one or more Pis in the account"))
        ssh_command_cmd.add_argument(
            "names", metavar="names", nargs='*',
            help=("The names of the Pis to get SSH commands for")
        )
        ssh_command_cmd.add_argument(
            "--ipv6",
            action="store_true",
            help=("Show IPv6 command")
        )
        ssh_command_cmd.set_defaults(func=self.do_ssh_command)

        ssh_config_cmd = commands.add_parser(
            "ssh-config",
            description=("Output the SSH config for one or more Pis in the account"),
            help=("Output the (IPv4 or IPv6) SSH config for one or more Pis in the account"))
        ssh_config_cmd.add_argument(
            "names", metavar="names", nargs='*',
            help=("The names of the Pis to get SSH config for")
        )
        ssh_config_cmd.add_argument(
            "--ipv6",
            action="store_true",
            help=("Show IPv6 command")
        )
        ssh_config_cmd.set_defaults(func=self.do_ssh_config)

        return parser, commands.choices

    def get_pi(self, name):
        pi = self.pis.get(name)
        if not pi:
            self.print_not_found(name)
            return
        return pi

    def get_pis(self, names):
        if not names:
            return self.pis.items()
        return {name: self.pis.get(name) for name in names}.items()

    def print_not_found(self, name):
        sys.stderr.write("{name} not found\n".format(name=name))

    def do_help(self):
        if self._args.cmd:
            self.parser.parse_args([self._args.cmd, '-h'])
        else:
            self.parser.parse_args(['-h'])

    def do_test(self):
        if self.cloud:
            print("Connected to the Mythic Beasts API")
            return
        return 2

    def do_get_images(self):
        images = self.cloud.get_operating_systems(model=self._args.model)
        col_width = max(len(name) for name in images.values()) + 1
        for id, name in images.items():
            print("{name:{col_width}}: {id}".format(name=name, id=id, col_width=col_width))

    def do_list(self):
        for name in self.pis:
            print(name)

    def do_show_pis(self):
        for name, pi in self.get_pis(self._args.names):
            if pi:
                print(pi, end='\n\n')
            else:
                self.print_not_found(name)

    def do_create(self):
        name = self._args.name
        model = self._args.model
        disk_size = self._args.disk
        ssh_key_path = self._args.ssh_key_path
        os_image = self._args.os_image
        args = {
            'model': model,
            'disk_size': disk_size,
            'ssh_key_path': ssh_key_path,
            'os_image': os_image,
        }

        kwargs = {k: v for k, v in args.items() if v is not None}
        pi = self.cloud.create_pi(name, **kwargs)

        print("Pi {} provisioned successfully".format(name))
        print()
        print(pi)

    def do_reboot(self):
        for name, pi in self.get_pis(self._args.names):
            if pi:
                pi.reboot()
                print("{name} rebooted".format(name=name))
            else:
                self.print_not_found(name)

    def do_power_on(self):
        for name, pi in self.get_pis(self._args.names):
            if pi:
                pi.on()
                print("{name} powered on".format(name=name))
            else:
                self.print_not_found(name)

    def do_power_off(self):
        for name, pi in self.get_pis(self._args.names):
            if pi:
                pi.off()
                print("{name} powered off".format(name=name))
            else:
                self.print_not_found(name)

    def do_cancel(self):
        if not self._args.yes:
            num_pis = len(self._args.names)
            try:
                s = '' if num_pis == 1 else 's'
                y = input("Cancelling {n} Pi{s}. Proceed? [Y/n]".format(n=num_pis, s=s))
            except KeyboardInterrupt:
                print()
                print("Not cancelled")
                return
            if y.lower() not in 'y':
                print("Not cancelled")
                return
        for name, pi in self.get_pis(self._args.names):
            if pi:
                pi.cancel()
                print("{name} cancelled".format(name=name))
            else:
                self.print_not_found(name)

    def do_show_keys(self):
        pi = self.get_pi(self._args.name)
        if not pi:
            return 2
        print(*pi.ssh_keys, sep='\n')

    def do_count_keys(self):
        for name, pi in self.get_pis(self._args.names):
            num_keys = len(pi.ssh_keys)
            s = '' if num_keys == 1 else 's'
            print("{name}: {n} key{s}".format(name=name, n=num_keys, s=s))

    def do_add_key(self):
        ssh_key = read_ssh_key(self._args.ssh_key_path)

        for name, pi in self.get_pis(self._args.names):
            keys_before = len(pi.ssh_keys)
            pi.ssh_keys |= {ssh_key}
            keys_after = len(pi.ssh_keys)
            num_keys = keys_after - keys_before
            s = '' if num_keys == 1 else ''
            print("{n} key{s} added to {name}".format(n=num_keys, name=name, s=s))

    def do_copy_keys(self):
        src_pi = self.get_pi(self._args.name_src)
        if not src_pi:
            return 2
        ssh_keys = src_pi.ssh_keys

        for name, pi in self.get_pis(self._args.names_dest):
            if pi:
                keys_before = len(pi.ssh_keys)
                pi.ssh_keys |= ssh_keys
                keys_after = len(pi.ssh_keys)
                num_keys = keys_after - keys_before
                s = '' if num_keys == 1 else 's'
                print("{n} key{s} added to {name}".format(n=num_keys, name=name, s=s))

    def do_remove_keys(self):
        for name, pi in self.get_pis(self._args.names):
            if pi:
                num_keys = len(pi.ssh_keys)
                pi.ssh_keys = set()
                s = '' if num_keys == 1 else 's'
                print("{n} key{s} removed from {name}".format(n=num_keys, name=name, s=s))
            else:
                self.print_not_found(name)

    def do_ssh_import_id(self):
        github = self._args.gh
        launchpad = self._args.lp
        github_keys = set()
        launchpad_keys = set()

        if github:
            github_keys |= ssh_import_id(github=github)
            s = '' if len(github_keys) == 1 else 's'
            print("{n} key{s} retrieved from GitHub".format(n=len(github_keys), s=s))
        if launchpad:
            launchpad_keys |= ssh_import_id(launchpad=launchpad)
            s = '' if len(launchpad_keys) == 1 else 's'
            print("{n} key{s} retrieved from Launchpad".format(n=len(launchpad_keys), s=s))

        print()
        new_keys = github_keys | launchpad_keys
        if len(new_keys) < (len(github_keys) + len(launchpad_keys)):
            s = '' if len(new_keys) == 1 else 's'
            print("{n} key{s} to add".format(n=len(new_keys), s=s))

        if new_keys:
            for name, pi in self.get_pis(self._args.names):
                if pi:
                    keys_before = len(pi.ssh_keys)
                    pi.ssh_keys |= new_keys
                    keys_after = len(pi.ssh_keys)
                    num_keys = keys_after - keys_before
                    s = '' if num_keys == 1 else 's'
                    print("{n} key{s} added to {name}".format(n=num_keys, name=name, s=s))
                else:
                    self.print_not_found(name)
        else:
            print("No keys to add")

    def do_ssh_command(self):
        for name, pi in self.get_pis(self._args.names):
            if pi:
                if self._args.ipv6:
                    print(pi.ipv6_ssh_command)
                else:
                    print(pi.ipv4_ssh_command)
            else:
                self.print_not_found(name)

    def do_ssh_config(self):
        for name, pi in self.get_pis(self._args.names):
            if pi:
                if self._args.ipv6:
                    print(pi.ipv6_ssh_config)
                else:
                    print(pi.ipv4_ssh_config)
            else:
                self.print_not_found(name)

    def do_provision_status(self):
        for name, pi in self.get_pis(self._args.names):
            if pi:
                print("{pi.name}: {pi.provision_status}".format(pi=pi))
            else:
                self.print_not_found(name)

    def do_power_status(self):
        for name, pi in self.get_pis(self._args.names):
            if pi:
                on_off = "on" if pi.power else "off"
                print("{name}: powered {on_off}".format(name=name, on_off=on_off))
            else:
                self.print_not_found(name)

main = CLI()

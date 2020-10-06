"""
hostedpi command line interface

Usage: hostedpi [cmd] [args]

$ hostedpi test
  Test your connection to the API

$ hostedpi list
  List all Pis in the account

$ hostedpi show [name]
  Show info about the Pi called *name*
$ hostedpi show all
  Show info about the all Pis within the account

$ hostedpi create [name] [model] [ssh_key_path]
  Provision a new Pi service with name *name*, optionally specify model number
  and SSH key path

$ hostedpi reboot [name]
  Reboot the Pi called *name*
$ hostedpi reboot all
  Reboot all Pis in the account

$ hostedpi cancel [name]
  Cancel the Pi called *name*
$ hostedpi cancel all
  Cancel all Pis in the account

$ hostedpi get-keys [name]
  Retrieve the SSH keys from the Pi called *name*
$ hostedpi get-keys all
  Show the number of SSH keys on each Pi in the account

$ hostedpi add-key [name] [ssh_key_path]
  Add the SSH key in *ssh_key_path* to the Pi called *name*
$ hostedpi add-key all [ssh_key_path]
  Add the SSH key in *ssh_key_path* to all Pis in the account

$ hostedpi copy-keys [name_src] [name_dest]
  Copy the keys from the Pi *name_src* to the Pi called *name_dest*
$ hostedpi copy-keys [name_src] all
  Copy the keys from the Pi *name_src* to all Pis in the account

$ hostedpi import-keys-gh [name] [username]
  Add the keys from GitHub user *username* to the Pi called *name*
$ hostedpi import-keys-gh all [username]
  Add the keys from GitHub user *username* to all Pis in the account

$ hostedpi import-keys-lp [name] [username]
  Add the keys from Launchpad user *username* to the Pi called *name*
$ hostedpi import-keys-lp all [username]
  Add the keys from Launchpad user *username* to all Pis in the account

$ hostedpi help
  show this help
"""

import os
import sys

import requests

from .picloud import PiCloud
from .utils import read_ssh_key, ssh_import_id
from .exc import HostedPiException


class CLI:
    def __init__(self):
        self.commands = {
            'help': self.do_help,
            'test': self.do_test,
            'list': self.do_list,
            'show': self.do_show,
            'create': self.do_create,
            'reboot': self.do_reboot,
            'cancel': self.do_cancel,
            'get-keys': self.do_get_keys,
            'add-key': self.do_add_key,
            'copy-keys': self.do_copy_keys,
            'import-keys-gh': self.do_import_keys_gh,
            'import-keys-lp': self.do_import_keys_lp,
        }

    def __call__(self):
        try:
            self.connect()
        except HostedPiException as e:
            print(str(e).replace(' or passed as arguments', ''))
            return 2

        args = sys.argv
        if len(args) == 1:
            return self.do_help()

        cmd = args[1]
        fn = self.commands.get(cmd)
        return fn(*args[2:])

    def connect(self):
        API_ID = os.environ.get('HOSTEDPI_ID')
        API_SECRET = os.environ.get('HOSTEDPI_SECRET')
        self.cloud = PiCloud(API_ID, API_SECRET)
        self.pis = self.cloud.pis

    def do_help(self, *args):
        print(__doc__)
        return 0

    def do_test(self, *args):
        print("Connected to Mythic Beasts API")
        return 0

    def do_list(self, *args):
        for name in self.pis:
            print(name)
        return 0

    def do_show(self, *args):
        if len(args) == 0:
            print('Usage: hostedpi show NAME')
            return 2
        name = args[0]
        if name == 'all':
            return self.do_show_all()
        else:
            return self.do_show_one(name)

    def do_show_one(self, name):
        pi = self.pis.get(name)
        if pi:
            pi.pprint()
            return 0
        else:
            print("No pi found by the name", name)
            return 2

    def do_show_all(self):
        for pi in self.pis.values():
            pi.pprint()
            print()
        return 0

    def do_create(self, *args):
        if len(args) == 0:
            print("Usage: hostedpi create NAME")
            return 2

        name = args[0]
        if len(args) == 1:
            pi = self.cloud.create_pi(name)
        elif len(args) == 2:
            pi = self.cloud.create_pi(name, model=model)
        elif len(args) == 3:
            pi = self.cloud.create_pi(name, model=model, ssh_key_path=ssh_key_path)
        else:
            print("")
        pi.pprint()
        return 0

    def do_reboot(self, *args):
        if len(args) == 0:
            print('Usage: hostedpi reboot NAME')
            return 2
        name = args[0]
        if name == 'all':
            return self.do_reboot_all()
        else:
            return self.do_reboot_one(name)

    def do_reboot_one(self, name):
        pi = self.pis.get(name)
        if pi:
            pi.reboot()
            print("Pi", name, "rebooted")
        else:
            print("No pi found by the name:", name)
            return 2

    def do_reboot_all(self):
        for pi in self.pis.values():
            pi.reboot()
        return 0

    def do_cancel(self, *args):
        if len(args) == 0:
            print('Usage: hostedpi cancel NAME')
            return 2
        name = args[0]
        if name == 'all':
            return self.do_cancel_all()
        else:
            return self.do_cancel_one(name)

    def do_cancel_one(self, name):
        pi = self.pis.get(name)
        if pi:
            pi.cancel()
            print("Pi service", name, "cancelled")
            return 0
        else:
            print("No pi found by the name", name)
            return 2

    def do_cancel_all(self):
        for pi in self.pis.values():
            pi.cancel()
            print("Pi service", name, "cancelled")
        return 0

    def do_get_keys(self, *args):
        if len(args) == 0:
            print('Usage: hostedpi get-keys NAME')
            return 2
        name = args[0]
        if name == 'all':
            return self.do_get_keys_all()
        else:
            return self.do_get_keys_one(name)

    def do_get_keys_one(self, name):
        pi = self.pis.get(name)
        print(*pi.ssh_keys, sep='\n')
        return 0

    def do_get_keys_all(self):
        for name, pi in self.pis.items():
            num_keys = len(pi.ssh_keys)
            print(name + ':', num_keys, 'key' if num_keys == 1 else 'keys')
        return 0

    def do_add_key(self, *args):
        if len(args) != 2:
            print('Usage: hostedpi add-key NAME PATH')
        name, ssh_key_path = args
        ssh_key = read_ssh_key(ssh_key_path)

        if name == 'all':
            return self.do_add_key_all(ssh_key)
        else:
            return self.do_add_key_one(name, ssh_key)

    def do_add_key_one(self, name, ssh_key):
        pi = self.pis.get(name)
        pi.ssh_keys += [ssh_key]
        return 0

    def do_add_key_all(self, ssh_key):
        for name, pi in self.pis.items():
            pi.ssh_keys += [ssh_key]
        return 0

    def do_copy_keys(self, *args):
        if len(args) != 2:
            print('Usage: hostedpi copy-keys SRC DEST')
        src, dest = args
        src_pi = self.pis.get(src)
        dest_pi = self.pis.get(dest)
        dest_pi.ssh_keys += src_pi.ssh_keys

    def do_import_keys_gh(self, *args):
        if len(args) != 2:
            print('Usage: hostedpi import-keys-gh NAME USERNAME')
        name, username = args
        pi = self.pis.get(name)
        pi.ssh_import_id(github=username)

    def do_import_keys_lp(self, *args):
        if len(args) != 2:
            print('Usage: hostedpi import-keys-lp NAME USERNAME')
        name, username = args
        pi = self.pis.get(name)
        pi.ssh_import_id(launchpad=username)

main = CLI()

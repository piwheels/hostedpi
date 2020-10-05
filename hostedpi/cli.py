"hostedpi command line interface"

import os
import sys

from .picloud import PiCloud
from .exc import HostedPiException


class CLI:
    def __init__(self):
        self.commands = {
            'test': self.do_test,
            'list': self.do_list,
            'show': self.do_show,
            'create': self.do_create,
            'reboot': self.do_reboot,
            'keys': self.do_keys,
            'cancel': self.do_cancel,
        }
        self.help = __doc__

    def _connect(self):
        API_ID = os.environ.get('HOSTEDPI_ID')
        API_SECRET = os.environ.get('HOSTEDPI_SECRET')
        self.cloud = PiCloud(API_ID, API_SECRET)
        self.pis = self.cloud.pis

    def __call__(self):
        try:
            self._connect()
        except HostedPiException as e:
            print(str(e).replace(' or passed as arguments', ''))
            return 2

        args = sys.argv
        if len(args) == 1:
            print(self.help)
            return 2

        cmd = args[1]
        fn = self.commands.get(cmd)
        return fn(*args[2:])

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

    def do_keys(self, *args):
        pass


main = CLI()

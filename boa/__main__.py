"""
Usage:
    boa install [--root=<path>] [PACKAGES ...]
    boa update [--root=<path>]
    boa uninstall [--root=<path>] [--all] [PACKAGES ...]
    boa list [--root=<path>] [--versions]
    boa sync [--root=<path>]
    boa shell [--root=<path>]
    boa version

Options:
    --root=<path>          Boa root directory
    --versions             Print package versions
    --all                  Apply to all tracked packages
"""

import os
import docopt

from . import PackageManager
from . import __version__

class Boa(PackageManager):
    def __init__(self, opts):
        PackageManager.__init__(self,
                                os.path.expanduser(opts['--root'] or '~/.boa'))
        self.load_config()
        self.run(opts)

    def cmd_install(self, packages):
        self.install(*packages)

    def cmd_uninstall(self, packages, all):
        self.uninstall(*packages, all=all)

    def cmd_list(self, versions=False):
        if versions:
            for k, v in self.package_versions.items():
                print(k, v)
        else:
            for pkg in self._packages:
                print(pkg)

    def cmd_update(self):
        self.update()

    def cmd_sync(self):
        self.sync()

    def run(self, opts):
        if opts['install']:
            self.cmd_install(opts['PACKAGES'])
        elif opts['list']:
            self.cmd_list(opts['--versions'])
        elif opts['uninstall']:
            self.cmd_uninstall(opts['PACKAGES'], opts['--all'])
        elif opts['update']:
            self.cmd_update()
        elif opts['sync']:
            self.cmd_sync()
        elif opts['shell']:
            self.shell()
        elif opts['version']:
            print(__version__)

def main(args=None):
    boa = Boa(docopt.docopt(__doc__))

if __name__ == '__main__':
    main()

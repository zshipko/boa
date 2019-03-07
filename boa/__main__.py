"""
Usage:
    boa install [--root=<path>] [-e] [-r] [PACKAGES ...]
    boa update [--root=<path>]
    boa uninstall [--root=<path>] [--all] [PACKAGES ...]
    boa remove [--root=<path>] [--all] [PACKAGES ...]
    boa list [--root=<path>] [--versions]
    boa sync [--root=<path>]
    boa shell [--root=<path>]
    boa env [--root=<path>] [--python=<path>] [--fetch=<version>] [PATH]
    boa version

Options:
    --root=<path>          Boa root directory
    --python=<path>        Python interpreter
    --fetch=<version>      Fetch a specific Python release
    --versions             Print package versions
    --all                  Apply to all tracked packages
    -e                     Editable packages
    -r                     Install packages from requirements.txt file
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

    def cmd_install(self, packages, editable, requirements):
        self.install(*packages, editable=editable, requirements=requirements)

    def cmd_uninstall(self, packages, all):
        self.uninstall(*packages, all=all)

    def cmd_remove(self, packages, all):
        self.remove_packages(*packages, all=all)

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
        self.sync(save=True)

    def run(self, opts):
        if opts['install']:
            self.cmd_install(opts['PACKAGES'], editable=opts['-e'], requirements=opts['-r'])
        elif opts['list']:
            self.cmd_list(opts['--versions'])
        elif opts['uninstall']:
            self.cmd_uninstall(opts['PACKAGES'], opts['--all'])
        elif opts['remove']:
            self.cmd_remove(opts['PACKAGES'], opts['--all'])
        elif opts['update']:
            self.cmd_update()
        elif opts['sync']:
            self.cmd_sync()
        elif opts['shell']:
            self.shell()
        elif opts['version']:
            print(__version__)
        elif opts['env']:
            self.env(python=opts['--python'], fetch=opts['--fetch'], path=opts['PATH'])

def main(args=None):
    boa = Boa(docopt.docopt(__doc__))

if __name__ == '__main__':
    main()

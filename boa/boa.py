import pip
import os
import toml

_DEFAULT_DIR = os.path.join(os.path.expanduser("~"), ".boa")

class PackageManager:
    def __init__(self,
                 root=_DEFAULT_DIR,
                 load=True,
                 config_file='config',
                 package_file='packages'):
        os.makedirs(root, exist_ok=True)
        self.root = root

        self.config_file = config_file
        self.package_file = package_file
        self._packages = []
        self._config = {}

        if load:
            self.load_fs()

    def load_fs(self):
        self.load_config()
        self.load_packages()

    def save_fs(self):
        self.save_config()
        self.save_packages()

    def make_path(self, *parts):
        return os.path.join(self.root, *parts)

    def save_config(self):
        with open(self.make_path(self.config_file), 'w') as f:
            toml.dump(self.config, f)

    def load_config(self):
        try:
            with open(self.make_path(self.config_file), 'r') as f:
                self.config = toml.load(f)

        except FileNotFoundError:
            pass

    def get_config(self, key, default=None):
        return self.config.get(key, default)

    def set_config(self, key, value):
        self.config[key] = value
        self.save_config()

    def _merge_packages(self, other):
        self._packages = sorted(list(set(self._packages + other)))

    def load_packages(self):
        try:
            with open(self.make_path(self.package_file), 'r') as f:
                self._merge_packages([n.strip() for n in f.readlines()])
        except FileNotFoundError:
            self._packages = []

    def save_packages(self):
        with open(self.make_path(self.package_file), 'w') as f:
            f.write('\n'.join(self._packages))

    def append_package(self, name, save=False):
        self._packages.append(name)

        if save:
            self.save_packages()

    def append_packages(self, *names, save=True):
        for name in names:
            self.append_package(name)

        if save:
            self.save_packages()

    def install(self, *packages, update=True):
        args = ["install", "--user"]

        if update:
            args.append('-U')

        packages = list(packages)

        if len(packages) == 0:
            return

        args = args + packages
        pip.main(args)
        self.append_packages(*packages)

    @property
    def package_versions(self):
        return {pkg.key: pkg.version for pkg in pip.get_installed_distributions() if pkg.key in self._packages}

    def update(self):
        self.install(update=True, *self._packages)

    def uninstall(self, *packages, all=False):
        if all:
            packages = self._packages
        else:
            packages = list(packages)

        if len(packages) == 0:
            return

        args = ["uninstall"] + packages
        pip.main(args)
        self._packages = (list(filter(lambda name: name not in packages,
                        self._packages)))

    def sync(self, save=False):
        packages = [pkg.key for pkg in
                    pip.get_installed_distributions(user_only=True)]
        self.append_packages(*packages, save=save)

    def shell(self):
        import IPython
        IPython.embed()





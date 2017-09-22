import pip
import os
import toml

_DEFAULT_DIR = os.path.join(os.path.expanduser("~"), ".boa")

class PackageManager:
    def __init__(self, root=_DEFAULT_DIR, load=True, **config):
        os.makedirs(root, exist_ok=True)
        self.root = root
        self.config = config

    def path(self, *parts):
        return os.path.join(self.root, *parts)

    def save_config(self, config='config'):
        with open(self.path(config), 'w') as f:
            toml.dump(self.config, f)

    def load_config(self, config='config'):
        with open(self.path(config), 'r') as f:
            self.config = toml.load(f)

    def get_config(self, key, default=None):
        return self.config.get(key, default)

    def set_config(self, key, value):
        self.config[key] = value
        self.save_config()

    def install(self, *packages, update=True):
        args = ["install", "--user"]

        if update:
            args.append('-U')

        packages = list(packages)

        if len(packages) == 0:
            return

        args = args + packages
        pip.main(args)
        self.set_config('packages', list(set(self.packages + packages)))

    @property
    def packages(self):
        return self.get_config('packages', [])

    @property
    def package_versions(self):
        return {pkg.key: pkg.version for pkg in pip.get_installed_distributions() if pkg.key in self.packages}

    def update(self):
        self.install(update=True, *self.packages)

    def uninstall(self, *packages, all=False):
        if all:
            packages = self.packages
        else:
            packages = list(packages)

        if len(packages) == 0:
            return

        args = ["uninstall"] + packages
        pip.main(args)
        self.set_config('packages', list(filter(lambda name: name not in packages,
                        self.packages)))





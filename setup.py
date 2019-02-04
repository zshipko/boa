from setuptools import setup

setup(name='boa',
      version='0.2.0',
      description='meta package manager',
      packages=['boa'],
      entry_points={
        'console_scripts': [
            'boa = boa.__main__:main'
        ]
      },
      install_requires=[
        'pip',
        'virtualenv',
        'toml',
        'docopt'
      ])

from setuptools import setup

setup(name='boa',
      version='0.1.0',
      packages=['boa'],
      entry_points={
        'console_scripts': [
            'boa = boa.__main__:main'
        ]
      })

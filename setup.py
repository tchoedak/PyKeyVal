from setuptools import setup, find_packages

import pykeyval
pkgs = ['pykeyval.%s' %s for s in find_packages('./pykeyval')]
pkgs.append('pykeyval')


with open('requirements.txt', 'r') as f:
    requirements = f.read().splitlines()

setup(
    name='pykeyval',
    version='0.0.1',
    packages=pkgs,
    description='',
    author='tchoedak@gmail.com',
    install_requires=['redis>=3.3.11', 'SQLAlchemy>=1.3.3', 'snowflake-sqlalchemy>=1.1.16'],
    tests_require=['pytest'],
    test_suite="tests",
)

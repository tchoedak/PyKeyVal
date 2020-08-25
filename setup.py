import pathlib
from setuptools import setup, find_packages


pkgs = ['pykeyval.%s' %s for s in find_packages('./pykeyval')]
pkgs.append('pykeyval')

with open('requirements.txt', 'r') as f:
    requirements = f.read().splitlines()

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name='pykeyval',
    version='0.0.1',
    packages=pkgs,
    description='PyKeyVal is a key-value store that you can pack in a bag and take with you.',
    long_description=README,
    long_description_content_type="text/markdown",
    author='tchoedak@gmail.com',
    install_requires=requirements,
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite="test",
)

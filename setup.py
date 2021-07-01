__version__ = '1.0.0'
# NOTE: This package only supports installation in dev-mode (-e) due to the way config is read.
from setuptools import setup, find_packages

setup(
    name='char-sheets',
    version=__version__,
    packages=find_packages(),
    description="aka. Para's insane.",
    install_requires=[
        'configcrunch >= 0.3.5',
    ],
)

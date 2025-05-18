__version__ = '1.0.0'
from setuptools import setup, find_packages
import os

def recursive_pkg_files_in(xpath):
    directory = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'char_sheets', xpath)
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.relpath(os.path.join('..', path, filename), os.path.join(os.path.abspath(os.path.dirname(__file__)), 'char_sheets')))
    return paths

setup(
    name='char-sheets',
    version=__version__,
    packages=find_packages(),
    description="aka. Para's insane.",
    install_requires=[
        'configcrunch >= 1.0.0',
        'tornado >= 6.5',
        'pdfrw >= 0.4'
    ],
    entry_points = {
        'console_scripts': ['characters=char_sheets.main:main'],
    },
    package_data={'char_sheets': recursive_pkg_files_in('web/')},

)

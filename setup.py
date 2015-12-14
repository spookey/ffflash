#!/usr/bin/env python3
'''
|info_cname| is available as package, you can find the newest version here:

:pypy: |info_pkg_url|

Most requirements are not necessary for normal operations, only for developing.
The most notable exception is **PyYAML**.

.. literalinclude:: ../requirements.txt
    :linenos:

:meth:`find_requirements` figures out what dependencies are required.

To install/update latest version of |info_name|::

    sudo pip3 install -U ffflash

To install all requirements from a local clone for developing::

    sudo pip3 install -U -r requirements.txt

'''
from os import path
from sys import argv

from setuptools import setup

from ffflash.info import info
from ffflash.lib.files import read_file


def local_file(name):
    '''
        :param name: filename to read relative from current directory
        :returns str: content of ``name`` or empty string on failure
    '''
    return read_file(path.join(
        path.dirname(path.abspath(__file__)), name
    ), fallback='')


long_description = '{}\n{}'.format(info.description, local_file('README.rst'))
requirements = [r for r in local_file('requirements.txt').split('\n') if r]


def find_requirements(*names):
    '''
        :param names: one or more required package names
        :returns list: package lines from ``requirements.txt`` whose lowercased
            name is in ``names``
    '''
    return [req for name in names for req in [
        r for r in requirements if r.lower().startswith(name)
    ]]


setup_requires = (
    find_requirements('pytest') if
    {'pytest', 'test', 'ptr'}.intersection(argv) else []
) + (
    find_requirements('sphinx') if
    {'build_sphinx', 'upload_docs'}.intersection(argv) else []
)

setup_params = dict(
    name=info.name,
    version=info.release,
    url=info.url,
    download_url=info.download_url,
    license='BSD',
    author=info.author,
    author_email=info.author_email,
    description=info.description,
    long_description=long_description,
    packages=['ffflash', 'ffflash.lib', 'ffflash.inc'],
    include_package_data=True,
    platforms='posix',
    scripts=['ffflash.py'],
    provides=[info.name],
    install_requires=find_requirements('pyyaml'),
    setup_requires=setup_requires,
    tests_require=find_requirements('pytest', 'python_dateutil', 'pyyaml'),
    zip_safe=True,
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Telecommunications Industry',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Topic :: System :: Networking',
        'Topic :: System :: Systems Administration',
    ]
)

if __name__ == '__main__':
    setup(**setup_params)

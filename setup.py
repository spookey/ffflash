'''
FreiFunk File nodeList And Sidecar Helper
'''
from os import path
from sys import argv

from setuptools import setup

from ffflash.info import info
from ffflash.lib.files import read_file

long_description = '{}\n{}'.format(
    __doc__,
    read_file(path.join(path.dirname(path.abspath(__file__)), 'README.rst'))
)
setup_requires = (
    ['pytest-runner'] if {'pytest', 'test', 'ptr'}.intersection(argv) else []
)

setup_params = dict(
    name=info.name,
    version=info.release,
    url=info.url,
    download_url='{}/archive/{}.tar.gz'.format(info.url, info.release),
    license='BSD',
    author=info.author,
    author_email=info.author_email,
    description=__doc__,
    long_description=long_description,
    packages=[
        'ffflash', 'ffflash.lib'
    ],
    include_package_data=True,
    platforms='posix',
    scripts=[
        'ffflash.py'
    ],
    provides=[info.name],
    install_requires=[
        'PyYAML'
    ],
    setup_requires=setup_requires,
    tests_require=[
        'pytest', 'python_dateutil', 'PyYAML'
    ],
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

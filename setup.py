'''
FreiFunk File nodeList And Sidecar Helper
'''
from os import path
from sys import argv

from setuptools import setup

from ffflash.info import info
from ffflash.lib.files import read_file


def local_file(name):
    return read_file(path.join(
        path.dirname(path.abspath(__file__)), name
    ), fallback='')


long_description = '{}\n{}'.format(__doc__, local_file('README.rst'))
requirements = [r for r in local_file('requirements.txt').split('\n') if r]


def find_req(*names):
    return [req for name in names for req in [
        r for r in requirements if r.lower().startswith(name)
    ]]


setup_requires = (
    find_req('pytest') if
    {'pytest', 'test', 'ptr'}.intersection(argv) else []
) + (
    find_req('sphinx') if
    {'build_sphinx', 'upload_docs'}.intersection(argv) else []
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
    install_requires=find_req('pyyaml'),
    setup_requires=setup_requires,
    tests_require=find_req('pytest', 'python_dateutil', 'pyyaml'),
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

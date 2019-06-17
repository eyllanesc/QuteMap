#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('docs/readme.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
	'Click>=7.0', 
	'Jinja2>=2.10.1',
]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="Edwin Christian Yllanes Cucho",
    author_email='e.yllanescucho@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Maps using Qt WebEngine and Qt WebChannel using PyQt5/PySide2",
    entry_points={
        'console_scripts': [
            'QuteMap=QuteMap.cli:main',
        ],
    },
    install_requires=requirements,
    extras_require={
        ':python_version == "3.6"': [
            'dataclasses',
        ],
    },
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='QuteMap',
    name='QuteMap',
    packages=find_packages(include=['QuteMap']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/eyllanesc/QuteMap',
    version='0.0.1',
    zip_safe=False,
)

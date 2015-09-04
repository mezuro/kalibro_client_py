#!/usr/bin/env python
"""
KalibroClient
===================

A http client for the Kalibro services.
"""
from setuptools import setup, find_packages

install_requires = [
    'requests>=2.7.0',
    'wheel>=0.24.0',
    'inflection>=0.3.1',
    'recordtype>=1.1',
    'python-dateutil>=2.4.2',
    'enum34>=1.0',
]

tests_require = [
    'factory_boy>=2.5.2',
    'nose>=1.3.7',
    'nose-progressive>=1.5.1',
    'coverage>=3.7.1',
    'mock>=1.0.1',
    'behave>=1.2.5',
]


setup(
    name="kalibro_client",
    version='1.3.0.1',
    author='Rafael Reggiani Manzo',
    author_email='rr.manzo@gmail.com',
    url='https://github.com/mezuro/kalibro_client_py',
    description='A http client for the Kalibro services.',
    long_description=__doc__,
    license='LGPLv3',
    packages=find_packages(),
    zip_safe=False,
    install_requires=install_requires,
    test_suite="nose.collector",
    tests_require=tests_require,
    extras_require={'test': tests_require},
    include_package_data=True,
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development'
    ],
)

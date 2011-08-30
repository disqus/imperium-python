#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='impermium',
    version='0.3',
    author='David Cramer',
    author_email='dcramer@gmail.com',
    url='http://github.com/disqus/impermium-python',
    description = 'Impermium API bindings for Python',
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        'simplejson',
    ],
    tests_require=[
        'mock',
        'unittest2',
    ],
    test_suite='unittest2.collector',
    include_package_data=True,
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)
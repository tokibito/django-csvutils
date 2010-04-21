#!/usr/bin/env python
#:coding=utf-8:

from setuptools import setup, find_packages
 
setup (
    name='django-csvutils',
    version='0.1',
    description='CSV utilities for Django',
    author='Shinya Okano',
    author_email='tokibito@beproud.jp',
    url='http://bitbucket.org/beproud/django-csvutils/',
    classifiers=[
      'Development Status :: 3 - Alpha',
      'Environment :: Plugins',
      'Framework :: Django',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: BSD License',
      'Programming Language :: Python',
      'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=["csvutils"],
    #test_suite='tests.main',
)

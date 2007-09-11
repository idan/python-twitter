#!/usr/bin/python
#
# Copyright 2007 Google Inc. All Rights Reserved.

'''The setup and build script for the python-twitter library.'''

__author__ = 'dewitt@google.com'
__version__ = '0.5'


# The base package metadata to be used by both distutils and setuptools
metadata = dict(
  name = "python-twitter",
  version = __version__,
  py_modules = ['twitter'],
  author='DeWitt Clinton',
  author_email='dewitt@google.com',
  description='A python wrapper around the Twitter API',
  long_description='A python wrapper around the Twitter API',
  license='Apache License 2.0',
  url='http://code.google.com/p/python-twitter/',
  keywords='twitter api',
)

# Extra package metadata to be used only if setuptools is installed
setuptools_metadata = dict(
#  data_files = [('.', ['README'])],
  install_requires = 'setuptools',
  include_package_data = True,
#  zip_safe=False,
  classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Apache Software License',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Communications :: Chat',
    'Topic :: Internet',
  ],
  test_suite = 'twitter_test.suite',
)

# Use setuptools if available, otherwise fallback and use distutils
try:
  import setuptools
  metadata.update(setuptools_metadata)
  setuptools.setup(**metadata)
except ImportError:
  import distutils.core
  distutils.core.setup(**metadata)

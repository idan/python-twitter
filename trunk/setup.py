from ez_setup import use_setuptools
use_setuptools()

import glob
import os
import setuptools

setuptools.setup(
  name = "python-twitter",
  version = "0.2",
  py_modules = ['twitter'],
  author='DeWitt Clinton',
  author_email='dewitt@google.com',
  description='A python wrapper around the Twitter API',
  long_description='A python wrapper around the Twitter API',
  license='Apache License 2.0',
  url='http://code.google.com/p/python-twitter',
  keywords='twitter api',
  install_requires = [ 'simplejson >= 1.5' ],
  test_suite = 'twitter_test.suite',
  zip_safe = True,
  )


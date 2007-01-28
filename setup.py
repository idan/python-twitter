from ez_setup import use_setuptools
use_setuptools()

import setuptools
import unittest

setuptools.setup(
  name = "python-twitter",
  version = "0.1",
  packages = setuptools.find_packages(),
  author='DeWitt Clinton',
  author_email='dewitt@google.com',
  description='A python wrapper around the Twitter API',
  license='Apache License 2.0',
  url='http://code.google.com/p/python-twitter',
  keywords='twitter api',
  install_requires = [ 'simplejson >= 1.4' ],
  test_suite = 'twitter_test.suite'
  )

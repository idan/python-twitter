from ez_setup import use_setuptools
use_setuptools()

import setuptools

setuptools.setup(
  name = "python-twitter",
  version = "0.1",
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
  data_files = [['doc', ['doc/twitter.html']]]
  )


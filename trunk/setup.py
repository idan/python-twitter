import distutils.core

distutils.core.setup(
  name = "python-twitter",
  version = "0.4",
  py_modules = ['twitter'],
  author='DeWitt Clinton',
  author_email='dewitt@google.com',
  description='A python wrapper around the Twitter API',
  long_description='A python wrapper around the Twitter API',
  license='Apache License 2.0',
  url='http://code.google.com/p/python-twitter/',
  keywords='twitter api')

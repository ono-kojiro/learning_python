from setuptools import setup

setup(
  name='search',
  version='0.0.1',
  py_modules=['search'],
  entry_points = {
    'console_scripts': [
      'search=search:main',
    ],
  },
)


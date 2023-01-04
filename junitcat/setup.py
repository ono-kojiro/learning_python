from setuptools import setup

setup(
  name='junitcat',
  version='0.0.1',
  py_modules=['junitcat'],
  entry_points={
    'console_scripts':[
      'junitcat = junitcat:main',
    ]
  },
)


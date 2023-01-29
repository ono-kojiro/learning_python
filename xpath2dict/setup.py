from setuptools import setup

setup(
  name='xpath2dict',
  version='0.0.1',
  py_modules=['xpath2dict'],
  entry_points={
    'console_scripts':[
      'xpath2dict = xpath2dict:main',
    ]
  },
)


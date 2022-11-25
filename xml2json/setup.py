from setuptools import setup
import distutils.command.build

class BuildCommand(distutils.command.build.build) :
	def initialize_options(self) :
		distutils.command.build.build.initialize_options(self)
		self.build_base = '_build'

setup(
  name='xml2jsonl',
  version='0.0.1',
  py_modules=['xml2jsonl', 'xml2json'],
  entry_points={
    'console_scripts':[
      'xml2jsonl = xml2jsonl:main',
      'xml2json  = xml2json:main',
    ]
  },
  cmdclass={"build": BuildCommand},
)


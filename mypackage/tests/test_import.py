#!/usr/bin/python

import sys

from mypackage.mymodule import *

print(type(myfunc))

myfunc()

sys.stderr.write('stderr output')


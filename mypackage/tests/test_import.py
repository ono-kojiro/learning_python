#!/usr/bin/python

import sys

from mypackage import mymodule

def test_import() :
    print(type(mymodule.myfunc))

    mymodule.myfunc()

    sys.stderr.write('stderr output')


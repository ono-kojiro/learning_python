#!/usr/bin/env python3

from .mymodule import myfunc, return_zero, return_one

from .simple import simple

def main() :
    print("This is mypackage.")

    myfunc()
    simple()

if __name__ == "__main__" :
    main()


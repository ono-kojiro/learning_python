#!/usr/bin/python

import sys
import os

import re

import getopt

import subprocess
from pprint import pprint

def get_lines(cmd):
    proc = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding='utf-8'
        )

    while True :
        line = proc.stdout.readline()
        if line :
            line = re.sub(r'\r?\n?$', '', line)
            yield line

        if not line and proc.poll() is not None :
            break

def usage(options, userdata):
    print('usage : {0} <target>'.format(sys.argv[0]))

def build(options, userdata) :
    print('build')

def clean(options, userdata):
    print('clean')

def ls(options, userdata) :
    cmd = 'ls -l'
    print(cmd)
    for line in get_lines(cmd) :
        pprint(line)
        print(line)

def df(options, userdata) :
    cmd = 'df'
    print(cmd)
    for line in get_lines(cmd) :
        print(line)

def main():
    ret = 0

    try:
        options, args = getopt.getopt(
            sys.argv[1:],
            "hvo:",
            [
                "help",
                "version",
                "output="
            ]
        )
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)
    
    output = None
    
    for o, a in options:
        if o in ("-v", "-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-o", "--output"):
            output = a
        else:
            assert False, "unknown option"
    
    #if output == None :
    #   print("no output option")
    #   ret += 1

    if ret != 0:
        sys.exit(1)
    
    #print('__name__ is {0}'.format(__name__))
    #print(sys.modules[__name__])
    #print(dir(__name__))
    #print(locals())
    #print(globals())
    
    #for key in globals() :
    #    val = globals()[key]
    #    print('{0} => {1}'.format(key, val))
    
    this_function_name = sys._getframe().f_code.co_name
    #print(this_function_name)

    userdata = {}

    for name in args :
        if name == this_function_name :
            print('WARNING : can not call function recursively')
            continue
        
        if name in globals() :
            func = globals()[name]
            if callable(func) :
                #print('callable')
                func(options, userdata)
            else :
                print('not callable')
        else :
            print("no such function, '{0}'".format(name))
            
    return ret

if __name__ == "__main__" :
    main()


#!/usr/bin/env python3

import sys
import getopt

from jinja2 import Template, Environment, FileSystemLoader

import json
import copy

import yaml
from pprint import pprint

def read_json(filepath) :
    fp = open(filepath, mode='r', encoding='utf-8')
    data = json.load(fp)
    fp.close()
    return data

def read_yaml(filepath):
   fp = open(filepath, mode="r", encoding="utf-8")
   tmp = yaml.load(fp, Loader=SafeLoader)
   data = copy.depcopy(tmp)
   fp.close()
   return data

def read_text(filepath):
    fp = open(filepath, mode='r', encoding='utf-8')
    lines = fp.read()
    fp.close()
    return lines


def render_recursively(env, template, context) :
    current = template
    while True:
        result = env.from_string(current).render(context)
        if result == current :
            break
        current = result
    return current

def main() :
    ret = 0

    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "hvdo:",
            [
                "help",
                "version",
                "debug",
                "output=",
            ]
        )
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)

    debug = False
    output = None

    for o, a in opts:
        if o == "-v":
            usage()
            sys.exit(0)
        elif o in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-d", "--debug"):
            debug = True
        elif o in ("-o", "--output"):
            output = a
        else:
            assert False, "unknown option"

    if output is not None :
        fp = open(output, mode='w', encoding='utf-8')
    else :
        fp = sys.stdout

    if ret != 0:
        sys.exit(1)

    searchpath = [
        '.',           # first
        './templates', # second
    ]

    context = {}

    loader = FileSystemLoader(searchpath=searchpath)
    env = Environment(loader=loader)

    lines = read_text('variables.yml')
    if debug :
        print('=== LINES BEGIN ===')
        print(lines)
        print('=== LINES END   ===')

    while True :
        context = yaml.safe_load(lines)
        #print('=== CONTEXT BEGIN ===')
        #print(context)
        #print('=== CONTEXT END   ===')

        template = env.from_string(lines)
        output = template.render(**context)
        if debug :
            print('=== OUTPUT BEGIN ===')
            print(output)
            print('=== OUTPUT END   ===')

        if output == lines :
            if debug :
                print('SAME')
            break
        
        lines = output

    #sys.exit(0)

    for filepath in args :
        lines = read_text(filepath)
        template = env.from_string(lines)
        #template = env.get_template(filepath)
        fp.write(template.render(**context))

    if output is not None :
        fp.close()


if __name__ == '__main__' :
    main()



    

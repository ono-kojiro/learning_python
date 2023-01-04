#!/usr/bin/python3
import os
import re
import sys

import getopt

from pathlib import Path

import subprocess
import shlex
import shutil

import tempfile

from lxml import etree

from pprint import pprint

debug = False

def usage():
    print("Usage : {0} [OPTIONS] [FILE] [DIR] [DIR ...]".format(sys.argv[0]))

    msg = '''
find junit xmlfiles from directories, and concatenate them

  -o, --output             output junit xml string to file
  -x, --xsd XSDFILE        use xsdfile (default: ./junit-10.xsd)
'''

    print(msg)

def find_xmlfiles(dirlist) :
    items = []

    for dirpath in dirlist :
        if os.path.isfile(dirpath) :
            items.append(dirpath)
            continue

        for path in Path(dirpath).rglob('*.xml') :
            if debug :
                print("DEBUG : found {0}".format(str(path)))
            items.append(str(path))

    return items

def validate_junit_xml(xsdfile, filepath) :
    ret = 0

    cmd = "xmllint --noout --schema {0} {1}".format(xsdfile, filepath)
    if debug :
        fd = subprocess.STDOUT
    else :
        fd = subprocess.DEVNULL

    try :
        res = subprocess.run(
            shlex.split(cmd),
            check=True,
            stderr=fd
        )
        ret = res.returncode
    except subprocess.CalledProcessError as e:
        ret = 1

    return ret

def main():
    ret = 0

    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "hvo:x:d",
            [
                "help",
                "version",
                "output=",
                "xsd=",
                "debug",
            ],
        )
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)

    output = None
    debug  = None
    xsdfile = None

    for o, a in opts:
        if o == "-v":
            usage()
            sys.exit(0)
        elif o in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-o", "--output"):
            output = a
        elif o in ("-d", "--debug"):
            debug = True
        elif o in ("-x", "--xsd"):
            xsdfile = a

    if debug :
        print("DEBUG : debut on")

    if xsdfile is None :
        xsdfile = '/usr/share/xunit-plugin/resources/types/model/xsd/junit-10.xsd'
        #print('no xsd option')
        #ret += 1
    
    if ret != 0:
        sys.exit(1)

    if not os.path.exists(xsdfile) :
        print('no xsd file, {0}'.format(xsdfile))
        sys.exit(1)

    if output is not None:
        fp = open(output, mode="w", encoding="utf8")
    else:
        fp = sys.stdout

    if len(args) == 0 :
        usage()
        sys.exit(1)

    xmlfiles = find_xmlfiles(args)

    if debug :
        print("DEBUG : found {0} xmlfiles".format(len(xmlfiles)))
   
    junit_xmls = []
    for filepath in xmlfiles :
        if debug :
            print("DEBUG : validate {0}".format(filepath))
        ret = validate_junit_xml(xsdfile, filepath)
        if ret == 0 :
            junit_xmls.append(filepath)

    new_root = None

    testsuites = []
        
    print("found {0} junit xmlfiles".format(len(junit_xmls)))

    for filepath in junit_xmls :
        tree = etree.parse(filepath)
        root = tree.getroot()

        if new_root is None :
            new_root = root
            continue

        for testsuite in root.findall('testsuite') :
            new_root.append(testsuite)

    if new_root is not None:
        etree.indent(new_root, space="    ")
        fp.write(etree.tostring(new_root, pretty_print=True).decode())

    if output is not None:
        print("output: {0}".format(output))
        fp.close()

if __name__ == "__main__":
    main()


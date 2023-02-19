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

import json

#from lxml import etree
import xml.etree.ElementTree as ET

import xmltodict

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
            "hvo:",
            [
                "help",
                "version",
                "output=",
            ],
        )
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)

    output = None

    for o, a in opts:
        if o == "-v":
            usage()
            sys.exit(0)
        elif o in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-o", "--output"):
            output = a

    if ret != 0:
        sys.exit(1)

    if output is not None:
        fp = open(output, mode="w", encoding="utf8")
    else:
        fp = sys.stdout

    if len(args) == 0 :
        usage()
        sys.exit(1)

    for filepath in args :
        print('input: {0}'.format(filepath))
        tree = ET.parse(filepath)
        root = tree.getroot()
        #pprint(root.findall("."))

        for ts in root.findall('./testsuite[@name]') :
            name = ts.attrib['name']
            #print(name)

            #for tc in ts.findall('./testcase[@name]') :
            #    testcase = tc.attrib['name']
            #    id = "{0}::{1}".format(testsuite, testcase)

            fp.write(
                json.dumps(
                    {
                        "index" : {
                            "_id" : name
                        }
                    },
                    ensure_ascii=False,
                )
            )
            fp.write("\n");

            #data = xmltodict.parse(
            #    ET.tostring(ts),
            #    attr_prefix='',   # remove '@'
            #    cdata_key=''      # remove '#text'
            #    )
            data = xmltodict.parse(
                ET.tostring(ts)
                )
            fp.write(
                json.dumps(
                    data,
                    ensure_ascii=False,
                )
            )
            fp.write("\n");



    if output is not None:
        print("output: {0}".format(output))
        fp.close()

if __name__ == "__main__":
    main()


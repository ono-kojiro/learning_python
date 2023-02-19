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

def read_lines(filepath) :
    fp = open(filepath, mode="r", encoding="utf-8")
    lines = ""

    is_testsuites = 0

    while 1:
        line = fp.readline()
        if not line :
            break

        line = re.sub(r'\r?\n?$', '', line)

        if is_testsuites == 0 :
            m = re.search(r'^<testsuites>', line)
            if m :
                is_testsuites = 1
        
        if is_testsuites :
            lines += line + '\n'
            
    fp.close()

    return lines

def main():
    ret = 0

    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "hvo:m:",
            [
                "help",
                "version",
                "output=",
                "module=",
            ],
        )
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)

    output = None
    module = None

    for o, a in opts:
        if o == "-v":
            usage()
            sys.exit(0)
        elif o in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-o", "--output"):
            output = a
        elif o in ("-m", "--module"):
            module = a

    if module is None :
        print('ERROR : no module option', file=sys.stderr)

    if ret != 0:
        sys.exit(1)

    if output is not None:
        fp = open(output, mode="w", encoding="utf8")
    else:
        fp = sys.stdout

    if len(args) == 0 :
        usage()
        sys.exit(1)

    num_testsuites = 0

    for filepath in args :
        #print('input: {0}'.format(filepath))

        #tree = ET.parse(filepath)
        #root = tree.getroot()
        
        lines = read_lines(filepath)
        root = ET.fromstring(lines)

        for ts in root.findall('./testsuite[@name]') :
            name = ts.attrib['name']

            fp.write(
                json.dumps(
                    {
                        "index" : {
                            "_id" : module + "-" + name
                        }
                    },
                    ensure_ascii=False,
                )
            )
            fp.write("\n");

            data = xmltodict.parse(
                ET.tostring(ts)
                )
            data["testsuite"]["module"] = module

            for param in ( '@tests', '@failures', '@errors' ) :
                if param in data["testsuite"] :
                    val = data["testsuite"][param]
                    data["testsuite"][param] = int(val)

            fp.write(
                json.dumps(
                    data,
                    ensure_ascii=False,
                )
            )
            fp.write("\n");

            num_testsuites += 1

    print('num_testsuites : {0}'.format(num_testsuites))
    if output is not None:
        #print("output: {0}".format(output))
        fp.close()

if __name__ == "__main__":
    main()


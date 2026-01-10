#!/usr/bin/env python3

import sys

import getopt

import re
import requests
from getpass import getpass
from bs4 import BeautifulSoup

from pprint import pprint

def read_lines(filepath) :
    fp = open(filepath, mode='r', encoding='utf-8')
    lines = fp.read()
    fp.close()

    return lines

def main() :
    ret = 0

    try:
        options, args = getopt.getopt(
            sys.argv[1:],
            "hvo:",
            [
              "help",
              "version",
              "output=",
            ]
        )
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)

    output = None

    for option, arg in options:
        if option in ("-v", "-h", "--help"):
            usage()
            sys.exit(0)
        elif option in ("-o", "--output"):
            output = arg
        else:
            assert False, "unknown option"

    #if username is None :
    #    print('no username option')
    #    ret += 1

    if output is not None:
        fp = open(output, mode="w", encoding='utf-8')
    else :
        fp = sys.stdout
    
    if ret != 0:
        sys.exit(1)

    for filepath in args :
        lines = read_lines(filepath)
        lines = re.sub(r'</?strong>', '', lines)
        lines = re.sub(r'</?em>', '', lines)
        lines = re.sub(r'\u200d', '', lines)
        #soup = BeautifulSoup(lines, 'html.parser')
        soup = BeautifulSoup(lines, 'lxml')
        #all_text = soup.get_text(strip=False, separator="\n")
        all_text = soup.get_text(strip=True, separator="\n")
        fp.write(all_text)
        #fp.write(soup.prettify())
        fp.write('\n')

    if output is not None:
        fp.close()

if __name__ == "__main__":
    main()

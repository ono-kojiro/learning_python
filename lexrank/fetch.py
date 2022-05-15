#!/usr/bin/env python3

import os
import sys

import getopt
import re

import requests
import shutil

def usage():
    print("Usage : {0} <URL>".format(sys.argv[0]))

def main():
    ret = 0

    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "hvo:",
            [
                "help",
                "version",
                "output-dir="
            ]
        )
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)
    
    output_dir = None
    
    for o, a in opts:
        if o == "-v":
            usage()
            sys.exit(0)
        elif o in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-o", "--output-dir"):
            output_dir = a
    
    if ret != 0:
        sys.exit(1)
    
    for url in args:
    	filename = os.path.basename(url)
    	if output_dir is not None :
    		filepath = output_dir + '/' + filename
    	else :
    		filepath = filename
    	
    	data = requests.get(url).content
    	
    	fp = open(filepath, 'wb')
    	fp.write(data)
    	fp.close()
    	
    	shutil.unpack_archive(filepath, 'out')

if __name__ == "__main__":
    main()

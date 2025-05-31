#!/usr/bin/env python3

import os
import sys

import getopt

import re
import tempfile
import shutil

import jaconv

def usage():
    print("Usage : {0}".format(sys.argv[0]))

def main():
    ret = 0
    
    try:
        opts, args = getopt.getopt(
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
    
    for o, a in opts:
        if o == "-v":
            usage()
            sys.exit(0)
        elif o in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-o", "--output"):
            output = a
        else:
            assert False, "unknown option"
    
    if output is not None :
        fd, path = tempfile.mkstemp()
        fp = os.fdopen(fd, 'w')
    else :
        fp = sys.stdout

    if ret != 0:
        sys.exit(1)

    for filepath in args:
        fp_in = open(filepath, mode="r", encoding="utf-8")
        while True:
            line = fp_in.readline()
            if not line:
                break
            
            line = re.sub(r'\r?\n?$', '', line)

            line = jaconv.z2h(line, kana=False, digit=True,  ascii=True)
            line = jaconv.h2z(line, kana=True,  digit=False, ascii=False)
            
            # ファイルに書き出すときはdecodeしない
            fp.write(line + '\n')
        fp_in.close()
        
    if output is not None :
        fp.flush()
        shutil.move(path, output)
        fp.close()
        if os.path.exists(path):
            os.remove(path)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import sys

import getopt
import re
import jaconv

def usage():
    print("Usage : {0}".format(sys.argv[0]))

def main():
    ret = 0

    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "hvo:e:",
            [
                "help",
                "version",
                "output=",
                "encode=",
            ]
        )
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)
    
    output = None
    encode = 'utf-8'
    
    for o, a in opts:
        if o == "-v":
            usage()
            sys.exit(0)
        elif o in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-o", "--output"):
            output = a
        elif o in ("-e", "--encode"):
            encode = a
    
    if ret != 0:
        sys.exit(1)
    
    if output is not None :
        fp_out = open(output, mode='w', encoding='utf-8')
    else :
        fp_out = sys.stdout
    

    for filepath in args:
        fp_in = open(filepath, mode='r', encoding=encode)
        while 1:
            line = fp_in.readline()
            if not line:
                break
            
            line = line.rstrip()

            # 半角カナを全角に変換            
            line = jaconv.h2z(line, kana=True, ascii=False, digit=False)

            # 全角ASCIIと数字を半角に変換
            line = jaconv.z2h(line, kana=False, ascii=True, digit=True)
            
            # ルビを除去
            line = re.sub(r'《[^》]+》', '', line)

            if output is not None :
                fp_out.write(line + '\n')
            else :
                print(line)
            
        fp_in.close()
        
    if output is not None :
        fp_out.close()

if __name__ == "__main__":
    main()

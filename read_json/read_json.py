#!/usr/bin/python

import sys

import getopt
import json

def usage():
    print("Usage : {0}".format(sys.argv[0]))

def main():
    ret = 0

    try:
        opts, args = getopt.getopt(
            sys.argv[1:], "hvo:", ["help", "version", "output="])
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
	
    if output == None :
        print("no output option")
        ret += 1
	
    if ret != 0:
        sys.exit(1)
    

    fp = open(output, mode='w', encoding='utf-8')
	
    fp.write("json test\n")	
    for input in args:
        print("arg : {0}".format(input))
        fp_in = open(input, mode='r', encoding='utf-8')
        data = json.load(fp_in)
        fp_in.close()

        print(
            json.dumps(
                data,
	        indent=4,
                ensure_ascii=False
            )
        )
        fp.write("version : {0}\n".format(data['version']))
        fp.write("data['sample']['aaa'][2] is {0}\n".format(data['sample']['aaa'][2]))
	
    fp.close()
	
if __name__ == "__main__":
	main()

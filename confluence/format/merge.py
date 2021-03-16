#!/usr/bin/python3

import sys

import getopt
import json
import re

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
                "output=",
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
	
    if output == None :
        print("no output option")
        ret += 1
	
    if ret != 0:
        sys.exit(1)
    
    fp = open(output, mode='w', encoding='utf-8')
    
    b_first = 1
    
    for filename in args :
        fp_in = open(filename, mode='r', encoding='utf-8')
        
        is_body = 0
        

        while 1 :
        	line = fp_in.readline()
        	if not line :
        		break
        	
        	line = re.sub('\r?\n?$', '', line)

        	m = re.search('^</body>', line)
        	if m :
        		is_body = 0
        	
        	if is_body :
        		fp.write(line + '\n')

        	m = re.search('^<body>', line)
        	if m :
        		is_body = 1
        	
        	
        	
        fp_in.close()
        
        fp.write("\n")
        #fp.write("<p class=MsoNormal align=left style='text-align:left;mso-pagination:widow-orphan'><span lang=EN-US><o:p>&nbsp;</o:p></span></p>\n")
        #fp.write("<p class=MsoNormal><span lang=EN-US><o:p>&nbsp;</o:p></span></p>\n")
        fp.write("<br clear=all style='mso-special-character:line-break;page-break-before:always'>\n")
        fp.write("\n")
    fp.close()
	
if __name__ == "__main__":
	main()

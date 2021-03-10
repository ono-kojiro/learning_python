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
    
    chapter = 0
    section = 0
    subsection = 0
    
    line = ''
    
    for filename in args :
        fp_in = open(filename, mode='r', encoding='utf-8')
        while 1 :
        	tmp = fp_in.readline()
        	if tmp :
	        	tmp = re.sub('\r?\n?$', '', tmp)
        		if len(tmp) == 76 and tmp[-1] == '=' :
        			tmp = tmp[0:75]
	        		line = line + tmp
        			continue
        		else :
        			line = line + tmp
        	elif line == '' :
        		break
        	
        	line = re.sub('\r?\n?$', '', line)
        	
        	if len(line) == 76 and line[-1] == '=' :
        		continue
        	else :
        		pass
        	
        	m = re.search('(\s*)margin: 1.0in;(\s*)', line)
        	if m :
        		line = m.group(1) + 'margin: 0.5in;' + m.group(2)
        	
        	m = re.search('(.*)<h1([^>]*)?>(.*)</h1>(.*)', line)
        	if m :
        		prefix = m.group(1)
        		attr   = m.group(2)
        		content = m.group(3)
        		suffix = m.group(4)
        		
        		chapter += 1
        		#line = prefix + "<h1 style='margin-left:21.0pt;text-indent:-21.0pt;mso-list:l0 level1 lfo2'><span style='mso-list:Ignore'>1." + content + "</span></h1>" + suffix
        		line = prefix + "<h1{0}>{1}. ".format(attr, chapter) + content + "</h1>" + suffix
        		
        		section = 0

        	m = re.search('(.*)<h2([^>]*)?>(.*)</h2>(.*)', line)
        	if m :
        		prefix = m.group(1)
        		attr   = m.group(2)
        		content = m.group(3)
        		suffix = m.group(4)
        		
        		section += 1
        		line = prefix + "<h2{0}>{1}.{2}. ".format(attr, chapter, section) + content + "</h2>" + suffix
        		
        		subsection = 0

        	m = re.search('(.*)<h3([^>]*)?>(.*)</h3>(.*)', line)
        	if m :
        		prefix = m.group(1)
        		attr   = m.group(2)
        		content = m.group(3)
        		suffix = m.group(4)
        		
        		subsection += 1
        		line = prefix + "<h3{0}>{1}.{2}.{3}. ".format(attr, chapter, section, subsection) + content + "</h3>" + suffix
        		
        	fp.write(line + '\n')
        	
        	line = ''
        	
        fp_in.close()
    
    fp.close()
	
if __name__ == "__main__":
	main()

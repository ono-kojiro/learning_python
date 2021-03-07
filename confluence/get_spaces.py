#!/usr/bin/python3

import sys

import getopt
import json
import re

#from atlassian import Jira
from atlassian import Confluence

from pprint import pprint

def usage():
    print("Usage : {0}".format(sys.argv[0]))

def main():
    ret = 0

    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "hvo:u:",
            [
                "help",
                "version",
                "output=",
                "url=",
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
        elif o in ("-u", "--url"):
            url = a
        else:
            assert False, "unknown option"
	
    if output == None :
        print("no output option")
        ret += 1
	
    if ret != 0:
        sys.exit(1)
    

    fp = open(output, mode='w', encoding='utf-8')

    confluence = Confluence(
        url=url,
        username='',
        password=''
    )

    spaces = confluence.get_all_spaces(start=0, limit=500, expand=None)
    
    #projects = jira.projects(included_archived=None)
    #pprint(projects)

    #project = jira.project('SVN')
    #pprint(project)

    #jql = 'project = SVN AND status IN ("OPEN", "REOPENED") ' + \
    #jql = 'project = SVN AND status IN ("REOPENED") ' + \
    #    'ORDER BY issuekey'
    #records = jira.jql(jql)

    #print(spaces);

    #print(data)
    fp.write(
        json.dumps(
            spaces,
            indent=4,
            ensure_ascii=False
        )
    )
	
    fp.close()
	
if __name__ == "__main__":
	main()

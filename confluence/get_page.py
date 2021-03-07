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

def get_children(confluence, page_id, depth):

  child_pages = confluence.get_page_child_by_type(page_id,
    type='page', start=None, limit=None)

  for page in child_pages :
    indent = ''.ljust(depth)
    print('{0}id {1}, title {2}'.format(indent, page['id'], page['title']))
    get_children(confluence, page['id'], depth + 1)

  pass

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

    #spaces = confluence.get_all_spaces(start=0, limit=500, expand=None)

    space_key = 'SVN'
    space = confluence.get_space(space_key,
      expand='description.plain,homepage')

    #content = confluence.get_space_content(space_key,
    #  depth="all", start=0, limit=500,
    #  content_type=None, expand="body.storage")

    #all_pages = confluence.get_all_pages_from_space(space_key,
    #  start=0, limit=100, status=None,
    #  expand=None, content_type='page')

    #page_id = '80450415' # top
    #page_id = '80450718' # HowTo
    page_id = '85476558' # Managing the Subversion Project

    #confluence.get_page_by_id(confluence, page_id,
    page = confluence.get_page_by_id(page_id, expand=None, status=None, version=None)

    depth = 0
    print('{0}id {1}, title {2}'.format(indent, page['id'], page['title']))
    
    get_children(confluence, page_id, 1)

    #child_pages = confluence.get_page_child_by_type(page_id,
    #  type='page', start=None, limit=None)

    #for page in child_pages :
    #    print('id {0}, title {1}'.format(page['id'], page['title']))

    fp.write(
        json.dumps(
            page,
            indent=4,
            ensure_ascii=False
        )
    )
	
    fp.close()
	
if __name__ == "__main__":
	main()

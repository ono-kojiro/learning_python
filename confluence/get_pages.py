#!/usr/bin/python3

import sys

import getopt
import json
import re

#from atlassian import Jira
from atlassian import Confluence

from pprint import pprint

import io
# 3.6 =< 3.x
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def usage():
    print("Usage : {0}".format(sys.argv[0]))

def get_children(confluence, page_id, depth, count):
  page = confluence.get_page_by_id(page_id,
      expand='body.storage', status=None, version=None)
  
  indent = ''.ljust(depth)
  print('{0}id {1}, title {2}'.format(indent, page['id'], page['title']),
    file=sys.stderr
  )
 
  value = page.get('body').get('storage').get('value')

  #pprint(value)

  pdf_b_str = confluence.export_page(page_id)

  output = '{0:0=2}-{1}.pdf'.format(count, page['title'])
  output = re.sub(r"[' \"]", '_', output)
  
  print('export {0}'.format(output), file=sys.stderr)

  fp = open(output, mode='wb')
  # errors='ignore')
  fp.write(pdf_b_str)
  fp.close()
  count += 1

  child_pages = confluence.get_page_child_by_type(page_id,
    type='page', start=None, limit=None)

  for page in child_pages :
    count = get_children(confluence, page['id'], depth + 1, count)

  return count

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
    #page = confluence.get_page_by_id(page_id, expand=None, status=None, version=None)

    depth = 0
    #print('{0}id {1}, title {2}'.format(indent, page['id'], page['title']))
    count = 0
    get_children(confluence, page_id, depth, count)

    #child_pages = confluence.get_page_child_by_type(page_id,
    #  type='page', start=None, limit=None)

    #for page in child_pages :
    #    print('id {0}, title {1}'.format(page['id'], page['title']))

    #fp.write(
    #    json.dumps(
    #        page,
    #        indent=4,
    #        ensure_ascii=False
    #    )
    #)
	
    fp.close()
	
if __name__ == "__main__":
	main()

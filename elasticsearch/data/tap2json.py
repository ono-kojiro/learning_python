#!/usr/bin/python3

import sys

import getopt
import json

from tap.parser import Parser
from tap.line   import Result
from tap.line   import Plan

from pprint import pprint

def main() :
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
    fp = open(output, mode='w', encoding='utf-8')
  else :
    fp = sys.stdout

  records = []
  
  for arg in args :
    parser = Parser()

    filepath = arg

    objs = parser.parse_file(filepath)
    for obj in objs :
      if type(obj) is Result :
        is_ok = obj.ok
        num   = obj.number
      
        record = {
          'ok' : obj.ok,
          'num' : obj.number,
          'desc' : obj.description,
          'skip' : obj.skip,
          'todo' : obj.todo
        }      

        records.append(record)
        print(str(obj), file=sys.stderr)
      elif type(obj) is Plan :
        expected_tests = obj.expected_tests
        print("expected tests : {0}".format(expected_tests), file=sys.stderr)

  
  fp.write(
    json.dumps(
      records,
      indent=4,
      ensure_ascii=False
    )
  )
  
  if output is not None :
    fp.close()

if __name__ == "__main__" :
  main()


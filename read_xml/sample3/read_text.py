#!/usr/bin/python
# coding: utf-8

import sys

import getopt
import codecs

import re

import json
from pprint import pprint

from dicttoxml import dicttoxml
#from bs4 import BeautifulSoup
from xml.dom.minidom import parseString

STATE_INIT = 0
STATE_LABEL = 1
STATE_RECORD = 2

def usage():
	print("Usage : {0}".format(sys.argv[0]))

def change_state(state, row, col, val, userdata):
  if state == STATE_INIT :
    if not re.match(r'^\s*$', val):
        state = STATE_LABEL
        print('state changed : STATE_LABEL, "{0}"'.format(val))
    pass
  elif state == STATE_LABEL :
    if col == 0 :
      state = STATE_RECORD
      pprint(userdata['columns'])
      print('state changed : STATE_RECORD')

    pass
  elif state == STATE_RECORD :
    pass

  return state

def proc_value(state, row, col, val, userdata):
  if state == STATE_INIT :
    pass
  elif state == STATE_LABEL :
    userdata['columns'][col] = val
    print('column {0} : {1}'.format(col, val))
    pass
  elif state == STATE_RECORD :
    if col in userdata['columns'] :
      #print('register record, "{0}"'.format(val))
      key = userdata['columns'][col]
      userdata['record'][key] = val
    pass

  return state

def post_proc(state, row, col, val, userdata):
  if state == STATE_INIT :
    pass
  elif state == STATE_LABEL :
    pass
  elif state == STATE_RECORD :
    pass

  return state

def main():
  print('sys.getdefaultencoding: ' + sys.getdefaultencoding())
	
  try:
    opts, args = getopt.getopt(
      sys.argv[1:],
      "hvo:",
      [
        "help", "version", "output="
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
	
  ret = 0
	
  if output == None :
    print("no output option")
    ret += 1
	
  if ret != 0:
    sys.exit(1)
	
  fp_out = codecs.open(output, "w", 'utf-8')

  records = []

  for input in args:
    fp_in = codecs.open(input, "r", 'utf-8')

    state = STATE_INIT
    row = 0

    userdata = {
      'columns' : {},
      'record' : {}
    }

    while 1:
      line = fp_in.readline()
      if not line:
        break

      line = re.sub('\r?\n?$', '', line)

      # remove comment
      line = re.sub('#.*', '', line)
      tokens = re.split('\t', line)

      # parse tokens
      for col in range(len(tokens)) :
        token = tokens[col]
        state = change_state(state, row, col, token, userdata)
        state = proc_value(state, row, col, token, userdata)
        state = post_proc(state, row, col, token, userdata)

      if state == STATE_RECORD :
        # append if record is not empty
        if userdata['record'] :
          records.append(userdata['record'])

        # clear record
        userdata['record'] = {}

      row += 1
    fp_in.close()


  #fp_out.write(
  #  json.dumps(
  #    records,
  #    indent=2,
  #    ensure_ascii=False
  #  )
  #)

  # convert dict to xml
  xml_bin = dicttoxml(records, attr_type=False, custom_root='items')
  xml = xml_bin.decode('utf-8')

  dom = parseString(xml)
  xml = dom.toprettyxml(indent='  ')

  fp_out.write(xml)
  
  #soup = BeautifulSoup(xml_utf8, "xml")
  #fp_out.write(soup.prettify())


  fp_out.close()


if __name__ == "__main__":
  main()


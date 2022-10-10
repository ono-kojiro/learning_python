#!/usr/bin/env python3

import sys
import os
import re

import getopt

from pprint import pprint

from netrc import netrc
import json
import ast

from urllib.parse import urlparse

from elasticsearch import Elasticsearch

def dump_response(res) :
  data = ast.literal_eval(str(res))
  
  print(
    json.dumps(
      data,
      indent=4,
      ensure_ascii=False
    )
  )

def main() :
  ret = 0

  try :
    options, args = getopt.getopt(
      sys.argv[1:],
      "hvo:u:n:",
      [
        "help",
        "version",
        "output=",
        "netrc=",
      ]
    )
  except getopt.GetoptError as err:
      print(str(err))
      sys.exit(2)  

  url = None
  netrcfile = None

  for key, value in options :
    if key in ("-o", "--output") :
      output = value
    elif key in ("-n", "--netrc") :
      netrcfile = value
    else :
      assert False, "unknown option"
      

  if url is None :
    url = "https://192.168.0.98:9200"
  
  if ret != 0 :
    sys.exit(ret)

  if len(args) == 0 :
    print('ERROR : no argument')
    sys.exit(1)

  netrcfile = '../.netrc'
  auths = netrc(netrcfile)

  # remove port number
  netloc = re.sub(r':.+', '', urlparse(url)[1])
  #netloc = urlparse(url)[1]

  #pprint(urlparse(url))
  
  auth = auths.authenticators(netloc)

  if auth is None :
    print('no authentication for {0}'.format(netloc))
    sys.exit(1)

  username = auth[0]
  password = auth[2]

  #print('username is {0}'.format(username))
  
  es = Elasticsearch(
    url,
    basic_auth=(username, password),
    verify_certs=True,
  )

  for index in args :
    res = es.indices.delete(index=index)
    dump_response(res)

  es.close()

if __name__ == "__main__" :
  main()

  


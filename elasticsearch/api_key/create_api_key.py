#!/usr/bin/env python3

import sys
import os

import getopt

from pprint import pprint

from netrc import netrc
import json
import ast

from elasticsearch import Elasticsearch
from elasticsearch.client import SecurityClient

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
  
  if netrcfile is None :
    netrcfile = "../.netrc"

  if ret != 0 :
    sys.exit(ret)

  host = '192.168.0.98'

  auths = netrc(netrcfile)
  
  #pprint(auths)

  auth = auths.authenticators(host)
  #pprint(auth)

  if auth is None :
    print('no authentication in {0}'.format(netrcfile))
    sys.exit(1)

  username = auth[0]
  password = auth[2]
  
  es = Elasticsearch(
    url,
    basic_auth=(username, password),
    verify_certs=False,
  )

  data_dict = ast.literal_eval(str(es.info()))

  #print(
  #  json.dumps(
  #    data_dict,
  #    indent=4,
  #    ensure_ascii=False
  #  )
  #)

  sc = SecurityClient(es)
  res = sc.create_api_key(
    name = 'my-api-key'
  )

  dump_response(res)

  res = sc.get_api_key()
  dump_response(res)


  es.close()

if __name__ == "__main__" :
  main()

  


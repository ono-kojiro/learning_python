#!/usr/bin/env python3

import sys
import os

import getopt

from pprint import pprint

import json
import ast

from elasticsearch import Elasticsearch

def main() :
  ret = 0

  try :
    options, args = getopt.getopt(
      sys.argv[1:],
      "hvo:u:",
      [
        "help",
        "version",
        "output=",
      ]
    )
  except getopt.GetoptError as err:
      print(str(err))
      sys.exit(2)  

  url = None

  for key, value in options :
    if key in ("-o", "--output") :
      output = value
    else :
      assert False, "unknown option"
      
  if url is None :
    url = "https://192.168.0.98:9200"
  
  if ret != 0 :
    sys.exit(ret)

  api_key_id = '6NhyCIMBA7q850jRIvKQ'
  api_key = 'CvzskylSQCaZT4moZcAJHA'
  
  es = Elasticsearch(
    url,
    api_key=(api_key_id, api_key),
    verify_certs=True,
  )

  data_dict = ast.literal_eval(str(es.info()))
  
  print(
    json.dumps(
      data_dict,
      indent=4,
      ensure_ascii=False
    )
  )
  
  es.close()

if __name__ == "__main__" :
  main()

  

